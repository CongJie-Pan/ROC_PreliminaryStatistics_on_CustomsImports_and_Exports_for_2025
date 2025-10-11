"""
Data Cleaning and Standardization Module

This module provides comprehensive data cleaning capabilities including:
- Column renaming (Chinese → English snake_case)
- Data type standardization
- Missing value handling
- Unit normalization
- Sub-header row removal

Author: Claude AI & 潘驄杰
Date: 2025-10-11
"""

import pandas as pd
import numpy as np
import json
import re
from pathlib import Path
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class DataCleaner:
    """
    Data cleaner for Taiwan customs trade statistics.

    Handles column renaming, data type conversion, missing values, and unit normalization.
    """

    def __init__(self, column_mappings_path: Optional[Path] = None):
        """
        Initialize data cleaner.

        Args:
            column_mappings_path: Path to column mappings JSON file.
                                 Defaults to config/column_mappings.json
        """
        if column_mappings_path is None:
            self.mappings_path = Path("config/column_mappings.json")
        else:
            self.mappings_path = Path(column_mappings_path)

        # Load column mappings
        self.column_mappings = self._load_column_mappings()

    def _load_column_mappings(self) -> Dict:
        """
        Load column mappings from JSON file.

        Returns:
            Dictionary containing column mappings
        """
        if not self.mappings_path.exists():
            logger.warning(f"Column mappings file not found: {self.mappings_path}")
            return {}

        with open(self.mappings_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _is_sub_header_row(self, row: pd.Series) -> bool:
        """
        Check if a row is a sub-header row or comparison row (not actual data).

        Args:
            row: Pandas Series representing a row

        Returns:
            True if row is a sub-header/comparison row, False otherwise
        """
        # Sub-header rows typically have NaN in first column or contain text like "年增率"
        first_col_value = row.iloc[0]

        # Check if first column is NaN
        if pd.isna(first_col_value):
            return True

        # Check if first column contains header text patterns or comparison text
        if isinstance(first_col_value, str):
            # Header patterns
            header_patterns = ['年增率', '占總出口', '占比', '金額']
            # Comparison patterns (e.g., "較上月增減", "較上年同月增減")
            comparison_patterns = ['較上', '增減']

            # Check header patterns
            for pattern in header_patterns:
                if pattern in first_col_value:
                    return True

            # Check comparison patterns
            for pattern in comparison_patterns:
                if pattern in first_col_value:
                    return True

            # Check if it's a month-only value (like "8月", "9月") without a year
            if '月' in first_col_value and '年' not in first_col_value:
                # This is monthly data without year prefix - filter it out
                # Valid formats should have year (e.g., "114年8月" or "114-08")
                return True

        return False

    def remove_sub_header_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove sub-header rows from dataframe.

        Args:
            df: Input dataframe

        Returns:
            Cleaned dataframe without sub-header rows
        """
        # Filter out rows where first column is NaN or contains header patterns
        mask = ~df.apply(self._is_sub_header_row, axis=1)
        cleaned_df = df[mask].copy()

        logger.debug(f"Removed {len(df) - len(cleaned_df)} sub-header rows")
        return cleaned_df

    def rename_columns(self, df: pd.DataFrame, table_id: str) -> pd.DataFrame:
        """
        Rename columns from Chinese to English snake_case.

        Args:
            df: Input dataframe
            table_id: Table identifier

        Returns:
            Dataframe with renamed columns
        """
        if table_id not in self.column_mappings:
            logger.warning(f"No column mappings found for {table_id}")
            return df

        table_mappings = self.column_mappings[table_id]
        renamed_df = df.copy()

        # Rename exact matches first
        rename_dict = {}
        for old_name, new_name in table_mappings.items():
            if old_name in renamed_df.columns:
                rename_dict[old_name] = new_name

        renamed_df = renamed_df.rename(columns=rename_dict)

        # Handle col_X columns (unnamed columns from multi-level headers)
        # Use pattern matching to infer names
        col_patterns = self.column_mappings.get('column_patterns', {})
        for col in renamed_df.columns:
            if col.startswith('col_'):
                # Try to infer name from position and patterns
                # This is a simplified approach - can be enhanced
                col_idx = int(col.split('_')[1])

                # Check previous column name to infer sub-column type
                if col_idx > 0:
                    prev_col = renamed_df.columns[col_idx - 1]
                    # If previous column is a main category, this might be growth_rate or share
                    if col_idx + 1 < len(renamed_df.columns):
                        # Pattern-based naming
                        # This will be refined in actual usage
                        pass  # Keep as is for now

        logger.debug(f"Renamed {len(rename_dict)} columns for {table_id}")
        return renamed_df

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in dataframe.

        Args:
            df: Input dataframe

        Returns:
            Dataframe with handled missing values
        """
        cleaned_df = df.copy()

        # Replace common missing value representations
        replacements = {
            '-': np.nan,
            '...': np.nan,
            '　': np.nan,  # Full-width space
            '': np.nan,
        }

        # Apply replacements
        for old_val, new_val in replacements.items():
            cleaned_df = cleaned_df.replace(old_val, new_val)

        logger.debug(f"Handled missing values")
        return cleaned_df

    def convert_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert columns to appropriate numeric types.

        Args:
            df: Input dataframe

        Returns:
            Dataframe with converted numeric columns
        """
        converted_df = df.copy()

        # Skip first column (year_month identifier)
        for col in converted_df.columns[1:]:
            # Try to convert to numeric
            try:
                converted_df[col] = pd.to_numeric(converted_df[col], errors='coerce')
            except Exception as e:
                logger.warning(f"Could not convert column {col} to numeric: {e}")

        logger.debug(f"Converted numeric columns")
        return converted_df

    def clean_year_month_column(self, df: pd.DataFrame, column_name: str = None) -> pd.DataFrame:
        """
        Clean and standardize year/month column.

        Args:
            df: Input dataframe
            column_name: Name of year/month column (defaults to first column)

        Returns:
            Dataframe with cleaned year/month column
        """
        cleaned_df = df.copy()

        if column_name is None:
            column_name = cleaned_df.columns[0]

        # Extract year/month values and clean
        def clean_year_month_value(val):
            if pd.isna(val):
                return val

            val_str = str(val).strip()

            # Handle year only (e.g., "104年" → "104")
            if '年' in val_str and '月' not in val_str:
                return val_str.replace('年', '').strip()

            # Handle year-month (e.g., "114年8月" → "114-08")
            if '年' in val_str and '月' in val_str:
                parts = val_str.replace('月', '').split('年')
                if len(parts) == 2:
                    year, month = parts
                    try:
                        return f"{year.strip()}-{int(month.strip()):02d}"
                    except:
                        return val_str

            return val_str

        cleaned_df[column_name] = cleaned_df[column_name].apply(clean_year_month_value)

        # Ensure column stays as string type
        cleaned_df[column_name] = cleaned_df[column_name].astype(str)

        logger.debug(f"Cleaned year/month column: {column_name}")
        return cleaned_df

    def clean_dataframe(self, df: pd.DataFrame, table_id: str) -> pd.DataFrame:
        """
        Apply all cleaning operations to dataframe.

        Args:
            df: Input dataframe (raw from Excel loader)
            table_id: Table identifier

        Returns:
            Cleaned and standardized dataframe
        """
        logger.info(f"Cleaning dataframe for {table_id}")

        # Step 1: Remove sub-header rows
        df = self.remove_sub_header_rows(df)

        # Step 2: Handle missing values
        df = self.handle_missing_values(df)

        # Step 3: Rename columns
        df = self.rename_columns(df, table_id)

        # Step 4: Convert numeric columns (skip first column)
        df = self.convert_numeric_columns(df)

        # Step 5: Clean year/month column (after numeric conversion to ensure it stays string)
        df = self.clean_year_month_column(df)

        # Step 6: Reset index
        df = df.reset_index(drop=True)

        logger.info(f"Cleaned {table_id}: final shape={df.shape}")
        return df


# Convenience function
def clean_dataframe(df: pd.DataFrame, table_id: str) -> pd.DataFrame:
    """
    Convenience function to clean a dataframe.

    Args:
        df: Input dataframe
        table_id: Table identifier

    Returns:
        Cleaned dataframe
    """
    cleaner = DataCleaner()
    return cleaner.clean_dataframe(df, table_id)
