"""
Parquet Data Loader Module

This module provides efficient data loading from Parquet files with
Streamlit caching for optimal performance.

Performance targets:
- Load time: <500ms per table
- Cache TTL: 1 hour (configurable)
- Memory usage: <500MB for all cached data
"""

import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

from streamlit_app.config.settings import (
    PARQUET_DIR,
    TABLE_MAPPING,
    get_data_path,
    SETTINGS
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_data(ttl=SETTINGS["cache_ttl"], show_spinner="Loading data...")
def load_parquet_data(
    table_name: str,
    columns: Optional[List[str]] = None,
    filters: Optional[Dict[str, Any]] = None
) -> pd.DataFrame:
    """
    Load data from a Parquet file with caching.

    This function loads data from the specified Parquet file and caches
    the result for improved performance on subsequent loads.

    Args:
        table_name: Name of the table to load (e.g., 'table08', 'export_by_country')
        columns: Optional list of columns to load (None = load all columns)
        filters: Optional dictionary of filters to apply (e.g., {'year_month': '114年1-8月'})

    Returns:
        DataFrame containing the loaded data

    Raises:
        FileNotFoundError: If the Parquet file doesn't exist
        ValueError: If the table name is invalid

    Examples:
        >>> df = load_parquet_data('table08')
        >>> df_filtered = load_parquet_data('table08', columns=['year_month', 'export_value'])
        >>> df_recent = load_parquet_data('table08', filters={'year_month': '114年1-8月'})
    """
    try:
        # Get file path
        file_path = get_data_path(table_name, format="parquet")

        # Validate file exists
        if not file_path.exists():
            raise FileNotFoundError(
                f"Parquet file not found: {file_path}\n"
                f"Please ensure data processing pipeline has been run."
            )

        # Load data
        logger.info(f"Loading data from {file_path}")
        df = pd.read_parquet(file_path, columns=columns)

        # Apply filters if provided
        if filters:
            for column, value in filters.items():
                if column in df.columns:
                    df = df[df[column] == value]
                else:
                    logger.warning(f"Filter column '{column}' not found in DataFrame")

        logger.info(f"Successfully loaded {len(df)} rows from {table_name}")
        return df

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        st.error(f"❌ Data file not found: {table_name}\n\nPlease run the data processing pipeline first.")
        raise

    except Exception as e:
        logger.error(f"Error loading data from {table_name}: {e}")
        st.error(f"❌ Error loading data: {str(e)}")
        raise


@st.cache_data(ttl=SETTINGS["cache_ttl"])
def load_multiple_tables(table_names: List[str]) -> Dict[str, pd.DataFrame]:
    """
    Load multiple Parquet files at once.

    Args:
        table_names: List of table names to load

    Returns:
        Dictionary mapping table names to DataFrames

    Examples:
        >>> tables = load_multiple_tables(['table08', 'table11'])
        >>> export_df = tables['table08']
        >>> china_df = tables['table11']
    """
    result = {}
    for table_name in table_names:
        try:
            result[table_name] = load_parquet_data(table_name)
        except Exception as e:
            logger.error(f"Failed to load {table_name}: {e}")
            continue

    return result


@st.cache_data(ttl=SETTINGS["cache_ttl"])
def get_table_info(table_name: str) -> Dict[str, Any]:
    """
    Get metadata information about a table without loading all data.

    Args:
        table_name: Name of the table

    Returns:
        Dictionary containing table metadata (rows, columns, size, etc.)

    Examples:
        >>> info = get_table_info('table08')
        >>> print(f"Rows: {info['rows']}, Columns: {info['columns']}")
    """
    try:
        file_path = get_data_path(table_name, format="parquet")

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read only the first row to get column info
        df_sample = pd.read_parquet(file_path, nrows=1)

        # Get file size
        file_size_mb = file_path.stat().st_size / (1024 * 1024)

        # Full row count (read metadata only)
        df_full = pd.read_parquet(file_path)
        row_count = len(df_full)

        return {
            "table_name": table_name,
            "file_path": str(file_path),
            "rows": row_count,
            "columns": len(df_sample.columns),
            "column_names": df_sample.columns.tolist(),
            "file_size_mb": round(file_size_mb, 2),
            "dtypes": df_sample.dtypes.to_dict()
        }

    except Exception as e:
        logger.error(f"Error getting table info for {table_name}: {e}")
        return {"error": str(e)}


def get_available_tables() -> List[str]:
    """
    Get list of available Parquet tables.

    Returns:
        List of table names that are available

    Examples:
        >>> tables = get_available_tables()
        >>> print(f"Found {len(tables)} tables")
    """
    available_tables = []

    for table_id in TABLE_MAPPING.keys():
        file_path = get_data_path(table_id, format="parquet")
        if file_path.exists():
            available_tables.append(table_id)

    return available_tables


def clear_cache():
    """
    Clear all cached data.

    This function should be called when data is updated or when
    manual cache refresh is needed.

    Examples:
        >>> clear_cache()
        >>> st.success("Cache cleared successfully!")
    """
    st.cache_data.clear()
    logger.info("Cache cleared successfully")


def get_cache_stats() -> Dict[str, Any]:
    """
    Get statistics about cached data.

    Returns:
        Dictionary containing cache statistics

    Examples:
        >>> stats = get_cache_stats()
        >>> print(f"Cached tables: {stats['cached_tables']}")
    """
    available_tables = get_available_tables()

    return {
        "total_tables": len(TABLE_MAPPING),
        "available_tables": len(available_tables),
        "cache_ttl_seconds": SETTINGS["cache_ttl"],
        "cache_ttl_minutes": SETTINGS["cache_ttl"] / 60,
        "available_table_list": available_tables
    }


# Convenience functions for commonly used tables

@st.cache_data(ttl=SETTINGS["cache_ttl"])
def load_overall_trade() -> pd.DataFrame:
    """Load overall trade statistics (table01)."""
    return load_parquet_data('table01')


@st.cache_data(ttl=SETTINGS["cache_ttl"])
def load_export_commodities() -> pd.DataFrame:
    """Load export commodity classifications (table02)."""
    return load_parquet_data('table02')


@st.cache_data(ttl=SETTINGS["cache_ttl"])
def load_export_by_country() -> pd.DataFrame:
    """Load export values by country/region (table08)."""
    return load_parquet_data('table08')


@st.cache_data(ttl=SETTINGS["cache_ttl"])
def load_import_by_country() -> pd.DataFrame:
    """Load import values by country/region (table09)."""
    return load_parquet_data('table09')


@st.cache_data(ttl=SETTINGS["cache_ttl"])
def load_trade_balance_by_country() -> pd.DataFrame:
    """Load trade balance by country/region (table10)."""
    return load_parquet_data('table10')


@st.cache_data(ttl=SETTINGS["cache_ttl"])
def load_export_to_china_hk() -> pd.DataFrame:
    """Load export data to China/Hong Kong (table11)."""
    return load_parquet_data('table11')
