"""
Business Logic and Calculation Utilities

This module provides calculation functions for trade statistics analysis,
including growth rates, market shares, and statistical computations.
"""

import pandas as pd
import numpy as np
from typing import Union, Optional, List, Tuple


def calculate_growth_rate(
    current_value: Union[float, int],
    previous_value: Union[float, int],
    as_percentage: bool = True
) -> float:
    """
    Calculate year-over-year growth rate.

    Args:
        current_value: Current period value
        previous_value: Previous period value
        as_percentage: Return as percentage (True) or decimal (False)

    Returns:
        Growth rate

    Examples:
        >>> calculate_growth_rate(110, 100)
        10.0
        >>> calculate_growth_rate(110, 100, as_percentage=False)
        0.1
    """
    if previous_value == 0:
        return 0.0

    growth = (current_value - previous_value) / previous_value

    return growth * 100 if as_percentage else growth


def calculate_cagr(
    start_value: Union[float, int],
    end_value: Union[float, int],
    periods: int,
    as_percentage: bool = True
) -> float:
    """
    Calculate Compound Annual Growth Rate (CAGR).

    Args:
        start_value: Starting value
        end_value: Ending value
        periods: Number of periods
        as_percentage: Return as percentage (True) or decimal (False)

    Returns:
        CAGR value

    Examples:
        >>> calculate_cagr(100, 150, 3)
        14.47
    """
    if start_value <= 0 or periods <= 0:
        return 0.0

    cagr = (end_value / start_value) ** (1 / periods) - 1

    return cagr * 100 if as_percentage else cagr


def calculate_market_share(
    value: Union[float, int],
    total: Union[float, int],
    as_percentage: bool = True
) -> float:
    """
    Calculate market share.

    Args:
        value: Individual value
        total: Total market value
        as_percentage: Return as percentage (True) or decimal (False)

    Returns:
        Market share

    Examples:
        >>> calculate_market_share(30, 100)
        30.0
    """
    if total == 0:
        return 0.0

    share = value / total

    return share * 100 if as_percentage else share


def calculate_trade_balance(
    export_value: Union[float, int],
    import_value: Union[float, int]
) -> float:
    """
    Calculate trade balance (exports - imports).

    Args:
        export_value: Export value
        import_value: Import value

    Returns:
        Trade balance (positive = surplus, negative = deficit)

    Examples:
        >>> calculate_trade_balance(150, 100)
        50.0
    """
    return export_value - import_value


def calculate_trade_ratio(
    export_value: Union[float, int],
    import_value: Union[float, int]
) -> float:
    """
    Calculate export/import ratio.

    Args:
        export_value: Export value
        import_value: Import value

    Returns:
        Trade ratio

    Examples:
        >>> calculate_trade_ratio(150, 100)
        1.5
    """
    if import_value == 0:
        return float('inf')

    return export_value / import_value


def calculate_moving_average(
    data: pd.Series,
    window: int = 3,
    center: bool = False
) -> pd.Series:
    """
    Calculate moving average.

    Args:
        data: Time series data
        window: Window size
        center: Whether to center the window

    Returns:
        Moving average series

    Examples:
        >>> data = pd.Series([100, 110, 120, 130, 140])
        >>> calculate_moving_average(data, window=3)
    """
    return data.rolling(window=window, center=center).mean()


def calculate_cumulative_sum(data: pd.Series) -> pd.Series:
    """
    Calculate cumulative sum.

    Args:
        data: Series data

    Returns:
        Cumulative sum series

    Examples:
        >>> data = pd.Series([10, 20, 30])
        >>> calculate_cumulative_sum(data)
        0    10
        1    30
        2    60
    """
    return data.cumsum()


def calculate_percentage_distribution(
    df: pd.DataFrame,
    value_column: str,
    category_column: str
) -> pd.DataFrame:
    """
    Calculate percentage distribution across categories.

    Args:
        df: DataFrame containing data
        value_column: Column with values
        category_column: Column with categories

    Returns:
        DataFrame with percentage distribution

    Examples:
        >>> df = pd.DataFrame({
        ...     'country': ['US', 'China', 'Japan'],
        ...     'export': [100, 80, 50]
        ... })
        >>> result = calculate_percentage_distribution(df, 'export', 'country')
    """
    total = df[value_column].sum()

    result = df.copy()
    result['percentage'] = (result[value_column] / total * 100).round(2)
    result['cumulative_percentage'] = result['percentage'].cumsum().round(2)

    return result


def calculate_yoy_change(
    df: pd.DataFrame,
    value_column: str,
    date_column: str,
    as_percentage: bool = True
) -> pd.DataFrame:
    """
    Calculate year-over-year changes for time series data.

    Args:
        df: DataFrame containing time series
        value_column: Column with values
        date_column: Column with dates/periods
        as_percentage: Return as percentage (True) or absolute (False)

    Returns:
        DataFrame with YoY change column added

    Examples:
        >>> df = pd.DataFrame({
        ...     'year': [2021, 2022, 2023],
        ...     'value': [100, 110, 125]
        ... })
        >>> result = calculate_yoy_change(df, 'value', 'year')
    """
    result = df.copy()

    result = result.sort_values(date_column)

    if as_percentage:
        result['yoy_change'] = result[value_column].pct_change() * 100
    else:
        result['yoy_change'] = result[value_column].diff()

    return result


def calculate_correlation(
    series1: pd.Series,
    series2: pd.Series,
    method: str = 'pearson'
) -> float:
    """
    Calculate correlation between two series.

    Args:
        series1: First data series
        series2: Second data series
        method: Correlation method ('pearson', 'spearman', 'kendall')

    Returns:
        Correlation coefficient

    Examples:
        >>> s1 = pd.Series([1, 2, 3, 4, 5])
        >>> s2 = pd.Series([2, 4, 6, 8, 10])
        >>> calculate_correlation(s1, s2)
        1.0
    """
    return series1.corr(series2, method=method)


def calculate_volatility(
    data: pd.Series,
    window: Optional[int] = None
) -> Union[float, pd.Series]:
    """
    Calculate volatility (standard deviation).

    Args:
        data: Time series data
        window: Rolling window size (None = overall volatility)

    Returns:
        Volatility value or series

    Examples:
        >>> data = pd.Series([100, 105, 95, 110, 90])
        >>> calculate_volatility(data)
        7.906
    """
    if window:
        return data.rolling(window=window).std()
    else:
        return data.std()


def calculate_trend_direction(
    data: pd.Series,
    threshold: float = 0.0
) -> str:
    """
    Determine overall trend direction.

    Args:
        data: Time series data
        threshold: Minimum change threshold to consider as trend

    Returns:
        Trend direction ('increasing', 'decreasing', 'stable')

    Examples:
        >>> data = pd.Series([100, 105, 110, 115, 120])
        >>> calculate_trend_direction(data)
        'increasing'
    """
    if len(data) < 2:
        return 'stable'

    first_value = data.iloc[0]
    last_value = data.iloc[-1]

    change_pct = ((last_value - first_value) / first_value * 100) if first_value != 0 else 0

    if change_pct > threshold:
        return 'increasing'
    elif change_pct < -threshold:
        return 'decreasing'
    else:
        return 'stable'


def calculate_concentration_index(
    values: Union[pd.Series, List[float]]
) -> float:
    """
    Calculate concentration index (Herfindahl-Hirschman Index).

    Args:
        values: Market shares or values

    Returns:
        HHI concentration index (0-10000)

    Examples:
        >>> values = [40, 30, 20, 10]  # Market shares
        >>> calculate_concentration_index(values)
        3000
    """
    if isinstance(values, list):
        values = pd.Series(values)

    # Normalize to percentages if not already
    total = values.sum()
    shares = (values / total * 100) if total > 0 else values

    # Calculate HHI
    hhi = (shares ** 2).sum()

    return round(hhi, 2)


def calculate_statistics_summary(
    data: pd.Series
) -> dict:
    """
    Calculate comprehensive statistics summary.

    Args:
        data: Data series

    Returns:
        Dictionary of statistics

    Examples:
        >>> data = pd.Series([100, 110, 105, 120, 115])
        >>> stats = calculate_statistics_summary(data)
        >>> print(stats['mean'])
        110.0
    """
    return {
        'count': len(data),
        'mean': data.mean(),
        'median': data.median(),
        'std': data.std(),
        'min': data.min(),
        'max': data.max(),
        'range': data.max() - data.min(),
        'q1': data.quantile(0.25),
        'q3': data.quantile(0.75),
        'iqr': data.quantile(0.75) - data.quantile(0.25),
        'skewness': data.skew(),
        'kurtosis': data.kurtosis()
    }


def identify_outliers(
    data: pd.Series,
    method: str = 'iqr',
    threshold: float = 1.5
) -> Tuple[pd.Series, pd.Series]:
    """
    Identify outliers in data.

    Args:
        data: Data series
        method: Detection method ('iqr' or 'zscore')
        threshold: Threshold multiplier

    Returns:
        Tuple of (outlier_mask, outlier_values)

    Examples:
        >>> data = pd.Series([10, 12, 11, 10, 100, 12, 11])
        >>> mask, values = identify_outliers(data)
    """
    if method == 'iqr':
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr

        outlier_mask = (data < lower_bound) | (data > upper_bound)

    elif method == 'zscore':
        z_scores = np.abs((data - data.mean()) / data.std())
        outlier_mask = z_scores > threshold

    else:
        raise ValueError(f"Unknown method: {method}")

    outlier_values = data[outlier_mask]

    return outlier_mask, outlier_values


def calculate_rank(
    df: pd.DataFrame,
    value_column: str,
    ascending: bool = False
) -> pd.DataFrame:
    """
    Add ranking column to DataFrame.

    Args:
        df: DataFrame
        value_column: Column to rank by
        ascending: Rank in ascending order

    Returns:
        DataFrame with rank column

    Examples:
        >>> df = pd.DataFrame({'country': ['US', 'China', 'Japan'],
        ...                     'export': [100, 80, 50]})
        >>> result = calculate_rank(df, 'export')
    """
    result = df.copy()
    result['rank'] = result[value_column].rank(ascending=ascending, method='dense').astype(int)

    return result.sort_values('rank')
