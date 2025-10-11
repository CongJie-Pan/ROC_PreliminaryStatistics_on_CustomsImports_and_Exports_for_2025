"""
Data Validation and Quality Assurance Module

This module provides comprehensive data validation including:
- Value range checks
- Data type validation
- Consistency checks (business rules)
- Completeness checks
- Validation reporting

Author: Claude AI & 潘驄杰
Date: 2025-10-11
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """
    Container for validation results.
    """
    table_id: str
    passed: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    row_count: int = 0
    column_count: int = 0

    def add_error(self, message: str):
        """Add an error message."""
        self.errors.append(message)
        self.passed = False

    def add_warning(self, message: str):
        """Add a warning message."""
        self.warnings.append(message)

    def summary(self) -> str:
        """Generate summary report."""
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        return f"""
Validation Result for {self.table_id}:
Status: {status}
Rows: {self.row_count}, Columns: {self.column_count}
Errors: {len(self.errors)}
Warnings: {len(self.warnings)}
"""


class DataValidator:
    """
    Data validator for Taiwan customs trade statistics.

    Performs comprehensive data quality checks.
    """

    def __init__(self):
        """Initialize data validator."""
        pass

    def check_value_ranges(
        self,
        df: pd.DataFrame,
        column: str,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None
    ) -> List[str]:
        """
        Check if values are within expected range.

        Args:
            df: Input dataframe
            column: Column name to check
            min_val: Minimum expected value (None = no check)
            max_val: Maximum expected value (None = no check)

        Returns:
            List of error messages (empty if all valid)
        """
        errors = []

        if column not in df.columns:
            errors.append(f"Column '{column}' not found")
            return errors

        # Check minimum value
        if min_val is not None:
            below_min = df[column] < min_val
            if below_min.any():
                count = below_min.sum()
                errors.append(f"Column '{column}': {count} values below minimum ({min_val})")

        # Check maximum value
        if max_val is not None:
            above_max = df[column] > max_val
            if above_max.any():
                count = above_max.sum()
                errors.append(f"Column '{column}': {count} values above maximum ({max_val})")

        return errors

    def check_missing_values(
        self,
        df: pd.DataFrame,
        required_columns: List[str]
    ) -> List[str]:
        """
        Check for missing values in required columns.

        Args:
            df: Input dataframe
            required_columns: List of columns that should not have NaN values

        Returns:
            List of error messages
        """
        errors = []

        for col in required_columns:
            if col not in df.columns:
                errors.append(f"Required column '{col}' not found")
                continue

            null_count = df[col].isna().sum()
            if null_count > 0:
                errors.append(f"Column '{col}': {null_count} missing values found")

        return errors

    def check_data_types(
        self,
        df: pd.DataFrame,
        expected_types: Dict[str, str]
    ) -> List[str]:
        """
        Check if columns have expected data types.

        Args:
            df: Input dataframe
            expected_types: Dictionary mapping column names to expected types

        Returns:
            List of error messages
        """
        errors = []

        for col, expected_type in expected_types.items():
            if col not in df.columns:
                errors.append(f"Column '{col}' not found")
                continue

            actual_type = str(df[col].dtype)

            # Flexible type matching
            type_matches = {
                'float64': ['float64', 'float32', 'int64', 'int32'],
                'int64': ['int64', 'int32'],
                'string': ['object', 'string'],
                'object': ['object', 'string'],
            }

            if expected_type in type_matches:
                if actual_type not in type_matches[expected_type]:
                    errors.append(f"Column '{col}': expected {expected_type}, got {actual_type}")
            elif actual_type != expected_type:
                errors.append(f"Column '{col}': expected {expected_type}, got {actual_type}")

        return errors

    def check_year_month_format(
        self,
        df: pd.DataFrame,
        column: str = 'year_month'
    ) -> List[str]:
        """
        Validate year/month column format.

        Args:
            df: Input dataframe
            column: Year/month column name

        Returns:
            List of error messages
        """
        errors = []

        if column not in df.columns:
            errors.append(f"Column '{column}' not found")
            return errors

        # Check format (should be like "104", "105", "114-08", etc.)
        invalid_formats = []
        for idx, val in df[column].items():
            if pd.isna(val):
                continue

            val_str = str(val)
            # Valid formats: "104" (year only) or "114-08" (year-month)
            if not (val_str.isdigit() or '-' in val_str):
                invalid_formats.append((idx, val_str))

        if invalid_formats:
            count = len(invalid_formats)
            errors.append(f"Column '{column}': {count} invalid format values")

        return errors

    def validate_dataframe(
        self,
        df: pd.DataFrame,
        table_id: str,
        rules: Optional[Dict] = None
    ) -> ValidationResult:
        """
        Perform comprehensive validation on dataframe.

        Args:
            df: Input dataframe to validate
            table_id: Table identifier
            rules: Optional custom validation rules

        Returns:
            ValidationResult object containing validation status and messages
        """
        logger.info(f"Validating dataframe for {table_id}")

        result = ValidationResult(
            table_id=table_id,
            passed=True,
            row_count=len(df),
            column_count=len(df.columns)
        )

        # Basic checks
        if df.empty:
            result.add_error("Dataframe is empty")
            return result

        # Check for year_month column
        year_month_cols = [col for col in df.columns if 'year' in col.lower() or col == 'year_month']
        if not year_month_cols:
            result.add_warning("No year/month column found")
        else:
            errors = self.check_year_month_format(df, year_month_cols[0])
            for error in errors:
                result.add_error(error)

        # Check for negative values in value columns (where inappropriate)
        value_columns = [col for col in df.columns if 'value' in col.lower()]
        for col in value_columns:
            if df[col].dtype in ['float64', 'int64']:
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    result.add_warning(f"Column '{col}': {negative_count} negative values (may be valid for losses)")

        # Check for extreme growth rates (> 1000% or < -100%)
        growth_columns = [col for col in df.columns if 'growth' in col.lower() or 'rate' in col.lower()]
        for col in growth_columns:
            if df[col].dtype in ['float64', 'int64']:
                extreme_high = (df[col] > 1000).sum()
                extreme_low = (df[col] < -100).sum()
                if extreme_high > 0:
                    result.add_warning(f"Column '{col}': {extreme_high} values > 1000%")
                if extreme_low > 0:
                    result.add_warning(f"Column '{col}': {extreme_low} values < -100%")

        logger.info(f"Validation for {table_id}: {'PASSED' if result.passed else 'FAILED'}")
        return result


# Convenience function
def validate_dataframe(
    df: pd.DataFrame,
    table_id: str,
    rules: Optional[Dict] = None
) -> ValidationResult:
    """
    Convenience function to validate a dataframe.

    Args:
        df: Input dataframe
        table_id: Table identifier
        rules: Optional validation rules

    Returns:
        ValidationResult object
    """
    validator = DataValidator()
    return validator.validate_dataframe(df, table_id, rules)
