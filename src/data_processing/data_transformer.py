"""
Data Transformation and Enrichment Module

This module provides data transformation capabilities including:
- Calculated fields (growth rates, market shares, trade balances)
- Metadata enrichment
- Aggregations and summaries
- Data linking and relationships

Author: Claude AI & 潘驄杰
Date: 2025-10-11
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class DataTransformer:
    """
    Data transformer for Taiwan customs trade statistics.

    Handles calculations, enrichment, and aggregations.
    """

    def __init__(self):
        """Initialize data transformer."""
        pass

    def calculate_growth_rate(
        self,
        df: pd.DataFrame,
        value_column: str,
        group_by_column: Optional[str] = None
    ) -> pd.Series:
        """
        Calculate year-over-year growth rate.

        Args:
            df: Input dataframe
            value_column: Column containing values to calculate growth from
            group_by_column: Optional column to group by (for regional calculations)

        Returns:
            Pandas Series with calculated growth rates
        """
        if value_column not in df.columns:
            logger.warning(f"Column {value_column} not found in dataframe")
            return pd.Series([np.nan] * len(df))

        # Shift values by 1 to get previous year
        prev_values = df[value_column].shift(1)

        # Calculate growth rate: (current - previous) / previous * 100
        growth_rate = ((df[value_column] - prev_values) / prev_values) * 100

        return growth_rate

    def calculate_market_share(
        self,
        df: pd.DataFrame,
        value_column: str,
        total_column: str
    ) -> pd.Series:
        """
        Calculate market share percentage.

        Args:
            df: Input dataframe
            value_column: Column containing regional/category value
            total_column: Column containing total value

        Returns:
            Pandas Series with calculated market shares
        """
        if value_column not in df.columns or total_column not in df.columns:
            logger.warning(f"Required columns not found in dataframe")
            return pd.Series([np.nan] * len(df))

        # Calculate share: (value / total) * 100
        market_share = (df[value_column] / df[total_column]) * 100

        return market_share

    def calculate_cumulative_sum(
        self,
        df: pd.DataFrame,
        value_column: str,
        reset_column: Optional[str] = None
    ) -> pd.Series:
        """
        Calculate cumulative sum, optionally resetting by group.

        Args:
            df: Input dataframe
            value_column: Column to calculate cumulative sum for
            reset_column: Optional column to reset cumsum by (e.g., year)

        Returns:
            Pandas Series with cumulative sums
        """
        if value_column not in df.columns:
            logger.warning(f"Column {value_column} not found")
            return pd.Series([np.nan] * len(df))

        if reset_column is None:
            # Simple cumulative sum
            return df[value_column].cumsum()
        else:
            # Cumulative sum reset by group
            return df.groupby(reset_column)[value_column].cumsum()

    def add_metadata_columns(
        self,
        df: pd.DataFrame,
        table_id: str,
        source_file: Optional[str] = None,
        data_month: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Add metadata columns to dataframe.

        Args:
            df: Input dataframe
            table_id: Table identifier
            source_file: Optional source file name
            data_month: Optional data month identifier

        Returns:
            Dataframe with added metadata columns
        """
        enriched_df = df.copy()

        # Add source table
        enriched_df['source_table'] = table_id

        # Add processing date
        enriched_df['processing_date'] = datetime.now().strftime('%Y-%m-%d')

        # Add source file if provided
        if source_file:
            enriched_df['source_file'] = source_file

        # Add data month if provided
        if data_month:
            enriched_df['data_month'] = data_month

        logger.debug(f"Added metadata columns to {table_id}")
        return enriched_df

    def convert_units_to_billions(
        self,
        df: pd.DataFrame,
        columns: List[str],
        from_unit: str = 'million'
    ) -> pd.DataFrame:
        """
        Convert monetary values to billions.

        Args:
            df: Input dataframe
            columns: List of column names to convert
            from_unit: Source unit ('million', 'thousand')

        Returns:
            Dataframe with converted units
        """
        converted_df = df.copy()

        conversion_factors = {
            'million': 1000,      # millions → billions: divide by 1000
            'thousand': 1000000,  # thousands → billions: divide by 1,000,000
        }

        if from_unit not in conversion_factors:
            logger.warning(f"Unknown unit: {from_unit}")
            return converted_df

        factor = conversion_factors[from_unit]

        for col in columns:
            if col in converted_df.columns:
                converted_df[col] = converted_df[col] / factor
                # Update column name to reflect billions
                new_name = col.replace('_million', '_billion').replace('_thousand', '_billion')
                if new_name != col:
                    converted_df = converted_df.rename(columns={col: new_name})

        logger.debug(f"Converted {len(columns)} columns to billions")
        return converted_df

    def create_quarterly_aggregation(
        self,
        df: pd.DataFrame,
        date_column: str,
        value_columns: List[str]
    ) -> pd.DataFrame:
        """
        Create quarterly aggregation from monthly data.

        Args:
            df: Input dataframe (must have monthly data)
            date_column: Column containing date/period
            value_columns: Columns to aggregate

        Returns:
            Dataframe with quarterly aggregations
        """
        # This is a simplified implementation
        # Real implementation would need proper quarter identification
        quarterly_df = df.copy()

        # Parse year-month to quarters
        # Example: "114-01" → "114-Q1"
        def to_quarter(year_month):
            if pd.isna(year_month):
                return np.nan
            if '-' in str(year_month):
                year, month = str(year_month).split('-')
                month_int = int(month)
                quarter = (month_int - 1) // 3 + 1
                return f"{year}-Q{quarter}"
            return year_month

        quarterly_df['quarter'] = quarterly_df[date_column].apply(to_quarter)

        # Aggregate by quarter
        agg_dict = {col: 'sum' for col in value_columns if col in quarterly_df.columns}

        if agg_dict:
            quarterly_agg = quarterly_df.groupby('quarter').agg(agg_dict).reset_index()
            logger.debug(f"Created quarterly aggregation: {len(quarterly_agg)} quarters")
            return quarterly_agg
        else:
            logger.warning("No valid value columns for aggregation")
            return quarterly_df

    def transform_dataframe(
        self,
        df: pd.DataFrame,
        table_id: str,
        operations: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Apply transformation operations to dataframe.

        Args:
            df: Input dataframe (cleaned)
            table_id: Table identifier
            operations: List of operations to apply (None = all standard operations)

        Returns:
            Transformed and enriched dataframe
        """
        logger.info(f"Transforming dataframe for {table_id}")

        transformed_df = df.copy()

        # Default operations
        if operations is None:
            operations = ['metadata', 'units']

        # Apply operations
        if 'metadata' in operations:
            transformed_df = self.add_metadata_columns(
                transformed_df,
                table_id=table_id
            )

        # Table-specific transformations
        if table_id == 'table08':
            # For export by country table, no unit conversion needed (already in millions)
            pass

        logger.info(f"Transformed {table_id}: final shape={transformed_df.shape}")
        return transformed_df


# Convenience function
def transform_dataframe(
    df: pd.DataFrame,
    table_id: str,
    operations: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Convenience function to transform a dataframe.

    Args:
        df: Input dataframe
        table_id: Table identifier
        operations: Optional list of operations to apply

    Returns:
        Transformed dataframe
    """
    transformer = DataTransformer()
    return transformer.transform_dataframe(df, table_id, operations)
