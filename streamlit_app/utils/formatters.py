"""
Data Formatting Utilities

This module provides formatting functions for consistent display of
numbers, currencies, dates, and other data types.
"""

from typing import Union, Optional
from datetime import datetime
import pandas as pd


def format_number(
    value: Union[int, float],
    decimals: int = 0,
    prefix: str = "",
    suffix: str = "",
    thousands_separator: str = ","
) -> str:
    """
    Format a number with thousands separators and optional prefix/suffix.

    Args:
        value: Number to format
        decimals: Number of decimal places
        prefix: Prefix string (e.g., '$', '€')
        suffix: Suffix string (e.g., '%', 'K', 'M')
        thousands_separator: Thousands separator character

    Returns:
        Formatted string

    Examples:
        >>> format_number(1234567.89, decimals=2)
        '1,234,567.89'
        >>> format_number(1500, prefix='$', suffix='M')
        '$1,500M'
    """
    if pd.isna(value):
        return "N/A"

    # Format with specified decimals
    format_str = f"{{:,.{decimals}f}}"
    formatted = format_str.format(value)

    # Custom thousands separator if needed
    if thousands_separator != ",":
        formatted = formatted.replace(",", thousands_separator)

    return f"{prefix}{formatted}{suffix}"


def format_currency(
    value: Union[int, float],
    currency: str = "USD",
    decimals: int = 2,
    scale: Optional[str] = None
) -> str:
    """
    Format a value as currency.

    Args:
        value: Value to format
        currency: Currency code ('USD', 'EUR', 'TWD', etc.)
        decimals: Number of decimal places
        scale: Scale factor ('K', 'M', 'B', 'T', or None for auto)

    Returns:
        Formatted currency string

    Examples:
        >>> format_currency(1234567, scale='M')
        '$1.23M'
        >>> format_currency(1500000000, scale='B')
        '$1.50B'
    """
    if pd.isna(value):
        return "N/A"

    # Currency symbols
    symbols = {
        'USD': '$',
        'EUR': '€',
        'TWD': 'NT$',
        'JPY': '¥',
        'GBP': '£',
        'CNY': '¥'
    }

    symbol = symbols.get(currency, currency + ' ')

    # Auto-scale if not specified
    if scale is None:
        if abs(value) >= 1e12:
            scale = 'T'
        elif abs(value) >= 1e9:
            scale = 'B'
        elif abs(value) >= 1e6:
            scale = 'M'
        elif abs(value) >= 1e3:
            scale = 'K'
        else:
            scale = ''

    # Apply scaling
    scale_factors = {
        'T': 1e12,
        'B': 1e9,
        'M': 1e6,
        'K': 1e3,
        '': 1
    }

    scaled_value = value / scale_factors.get(scale, 1)

    return format_number(scaled_value, decimals=decimals, prefix=symbol, suffix=scale)


def format_percentage(
    value: Union[int, float],
    decimals: int = 1,
    include_sign: bool = False
) -> str:
    """
    Format a value as percentage.

    Args:
        value: Value to format (e.g., 0.15 or 15 for 15%)
        decimals: Number of decimal places
        include_sign: Include '+' sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(15.5)
        '15.5%'
        >>> format_percentage(10.2, include_sign=True)
        '+10.2%'
    """
    if pd.isna(value):
        return "N/A"

    sign = '+' if include_sign and value > 0 else ''

    return f"{sign}{value:.{decimals}f}%"


def format_change(
    value: Union[int, float],
    as_percentage: bool = True,
    decimals: int = 1,
    show_sign: bool = True,
    show_arrow: bool = False
) -> str:
    """
    Format a change value with optional sign and arrow.

    Args:
        value: Change value
        as_percentage: Format as percentage
        decimals: Number of decimal places
        show_sign: Show '+' or '-' sign
        show_arrow: Show arrow indicator (↑↓)

    Returns:
        Formatted change string

    Examples:
        >>> format_change(15.5)
        '+15.5%'
        >>> format_change(-10.2, show_arrow=True)
        '↓ -10.2%'
    """
    if pd.isna(value):
        return "N/A"

    # Determine sign and arrow
    sign = ''
    arrow = ''

    if value > 0:
        sign = '+' if show_sign else ''
        arrow = '↑ ' if show_arrow else ''
    elif value < 0:
        sign = '' if show_sign else ''  # Negative sign is automatic
        arrow = '↓ ' if show_arrow else ''
    else:
        arrow = '→ ' if show_arrow else ''

    # Format value
    if as_percentage:
        formatted = f"{sign}{value:.{decimals}f}%"
    else:
        formatted = format_number(value, decimals=decimals, prefix=sign)

    return f"{arrow}{formatted}"


def format_large_number(
    value: Union[int, float],
    decimals: int = 1
) -> str:
    """
    Format large numbers with appropriate scale (K, M, B, T).

    Args:
        value: Number to format
        decimals: Number of decimal places

    Returns:
        Formatted string with scale

    Examples:
        >>> format_large_number(1500)
        '1.5K'
        >>> format_large_number(2500000)
        '2.5M'
        >>> format_large_number(1500000000)
        '1.5B'
    """
    if pd.isna(value):
        return "N/A"

    abs_value = abs(value)
    sign = '-' if value < 0 else ''

    if abs_value >= 1e12:
        return f"{sign}{abs_value/1e12:.{decimals}f}T"
    elif abs_value >= 1e9:
        return f"{sign}{abs_value/1e9:.{decimals}f}B"
    elif abs_value >= 1e6:
        return f"{sign}{abs_value/1e6:.{decimals}f}M"
    elif abs_value >= 1e3:
        return f"{sign}{abs_value/1e3:.{decimals}f}K"
    else:
        return f"{sign}{abs_value:.{decimals}f}"


def format_date(
    date: Union[str, datetime, pd.Timestamp],
    format: str = "%Y-%m-%d"
) -> str:
    """
    Format a date value.

    Args:
        date: Date to format
        format: Date format string

    Returns:
        Formatted date string

    Examples:
        >>> format_date("2025-10-11")
        '2025-10-11'
        >>> format_date("2025-10-11", format="%B %d, %Y")
        'October 11, 2025'
    """
    if pd.isna(date):
        return "N/A"

    # Convert to datetime if string
    if isinstance(date, str):
        try:
            date = pd.to_datetime(date)
        except:
            return date

    # Format
    try:
        return date.strftime(format)
    except:
        return str(date)


def format_year_month(
    year_month: str,
    format: str = "short"
) -> str:
    """
    Format Taiwan year-month notation (e.g., '114年1-8月').

    Args:
        year_month: Year-month string
        format: Output format ('short', 'long', 'english')

    Returns:
        Formatted string

    Examples:
        >>> format_year_month('114年1-8月', 'english')
        '2025-01 to 2025-08'
    """
    if pd.isna(year_month):
        return "N/A"

    # Parse Taiwan year format
    try:
        if '年' in str(year_month):
            # Extract year and month parts
            parts = str(year_month).replace('年', '-').replace('月', '').split('-')

            if len(parts) >= 2:
                tw_year = int(parts[0])
                gregorian_year = tw_year + 1911

                if format == 'english':
                    if len(parts) == 3:  # Range like '1-8'
                        return f"{gregorian_year}-{parts[1]:0>2} to {gregorian_year}-{parts[2]:0>2}"
                    else:
                        return f"{gregorian_year}-{parts[1]:0>2}"
                elif format == 'long':
                    return f"Year {tw_year}, Month {parts[1]}"
                else:  # short
                    return str(year_month)

        return str(year_month)

    except:
        return str(year_month)


def format_table_cell(
    value: any,
    value_type: str = "auto",
    decimals: int = 2
) -> str:
    """
    Format a table cell value based on its type.

    Args:
        value: Value to format
        value_type: Type hint ('number', 'currency', 'percentage', 'date', or 'auto')
        decimals: Number of decimal places

    Returns:
        Formatted string

    Examples:
        >>> format_table_cell(1234.567, 'number')
        '1,234.57'
        >>> format_table_cell(15.5, 'percentage')
        '15.50%'
    """
    if pd.isna(value):
        return "—"

    if value_type == "auto":
        # Auto-detect type
        if isinstance(value, (int, float)):
            value_type = "number"
        elif isinstance(value, (datetime, pd.Timestamp)):
            value_type = "date"
        else:
            return str(value)

    if value_type == "number":
        return format_number(value, decimals=decimals)
    elif value_type == "currency":
        return format_currency(value, decimals=decimals)
    elif value_type == "percentage":
        return format_percentage(value, decimals=decimals)
    elif value_type == "date":
        return format_date(value)
    else:
        return str(value)


def format_comparison(
    value1: Union[int, float],
    value2: Union[int, float],
    label1: str = "Current",
    label2: str = "Previous"
) -> str:
    """
    Format a comparison between two values.

    Args:
        value1: First value
        value2: Second value
        label1: Label for first value
        label2: Label for second value

    Returns:
        Formatted comparison string

    Examples:
        >>> format_comparison(110, 100)
        'Current: 110 vs Previous: 100 (+10.0%)'
    """
    change = calculate_growth_rate(value1, value2)

    return (f"{label1}: {format_number(value1)} vs "
            f"{label2}: {format_number(value2)} "
            f"({format_change(change)})")


def calculate_growth_rate(current: float, previous: float) -> float:
    """Helper function for growth rate calculation."""
    if previous == 0:
        return 0.0
    return (current - previous) / previous * 100


def truncate_text(
    text: str,
    max_length: int = 50,
    suffix: str = "..."
) -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated

    Returns:
        Truncated text

    Examples:
        >>> truncate_text("This is a very long text", max_length=10)
        'This is a...'
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix
