"""
Metric Display Components

This module provides reusable components for displaying KPIs and metrics
with consistent styling.
"""

import streamlit as st
from typing import Optional, Union
from streamlit_app.config.theme import COLORS


def display_metric_card(
    title: str,
    value: Union[int, float, str],
    delta: Optional[Union[int, float, str]] = None,
    delta_color: str = "normal",
    prefix: str = "",
    suffix: str = "",
    help_text: Optional[str] = None,
    icon: Optional[str] = None
):
    """
    Display a metric card with optional delta indicator.

    Args:
        title: Metric title/label
        value: Main metric value
        delta: Change value (optional)
        delta_color: Color scheme for delta ('normal', 'inverse', 'off')
        prefix: Prefix for value (e.g., '$', '+')
        suffix: Suffix for value (e.g., '%', 'B')
        help_text: Tooltip help text
        icon: Emoji icon to display
    """
    # Format value
    if isinstance(value, (int, float)):
        formatted_value = f"{prefix}{value:,.0f}{suffix}"
    else:
        formatted_value = f"{prefix}{value}{suffix}"

    # Display metric
    if icon:
        st.markdown(f"### {icon} {title}")
    else:
        st.markdown(f"### {title}")

    st.metric(
        label="",
        value=formatted_value,
        delta=delta,
        delta_color=delta_color,
        help=help_text
    )


def display_kpi_row(metrics: list):
    """
    Display a row of KPI metrics.

    Args:
        metrics: List of dictionaries containing metric data
                Each dict should have: title, value, delta (optional)

    Example:
        >>> metrics = [
        ...     {"title": "Export Value", "value": 123.4, "suffix": "B", "delta": "+10%"},
        ...     {"title": "Growth Rate", "value": 15.2, "suffix": "%", "delta": "+2.3%"}
        ... ]
        >>> display_kpi_row(metrics)
    """
    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):
        with col:
            display_metric_card(**metric)


def display_comparison_metrics(
    label1: str,
    value1: Union[int, float],
    label2: str,
    value2: Union[int, float],
    title: str = "Comparison",
    suffix: str = ""
):
    """
    Display side-by-side comparison of two metrics.

    Args:
        label1: Label for first metric
        value1: Value for first metric
        label2: Label for second metric
        value2: Value for second metric
        title: Overall title
        suffix: Unit suffix
    """
    st.markdown(f"### {title}")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.metric(label1, f"{value1:,.1f}{suffix}")

    with col2:
        # Calculate difference
        diff = value2 - value1
        pct_change = (diff / value1 * 100) if value1 != 0 else 0

        st.markdown(f"**Change:**")
        color = COLORS["success"] if diff > 0 else COLORS["danger"]
        st.markdown(f"<p style='color: {color}; font-size: 1.5rem; font-weight: bold;'>{diff:+,.1f}{suffix} ({pct_change:+.1f}%)</p>",
                    unsafe_allow_html=True)

    with col3:
        st.metric(label2, f"{value2:,.1f}{suffix}")


def display_progress_bar(
    value: float,
    max_value: float,
    label: str,
    show_percentage: bool = True,
    color: Optional[str] = None
):
    """
    Display a progress bar with label.

    Args:
        value: Current value
        max_value: Maximum value
        label: Label text
        show_percentage: Whether to show percentage
        color: Progress bar color (optional)
    """
    percentage = (value / max_value * 100) if max_value > 0 else 0

    st.markdown(f"**{label}**")

    if show_percentage:
        st.markdown(f"{percentage:.1f}%")

    st.progress(min(percentage / 100, 1.0))


def display_trend_indicator(
    value: float,
    threshold_positive: float = 0,
    threshold_negative: float = 0,
    label: str = "Trend"
):
    """
    Display a trend indicator with color coding.

    Args:
        value: Value to evaluate
        threshold_positive: Threshold for positive indicator
        threshold_negative: Threshold for negative indicator
        label: Label text
    """
    if value > threshold_positive:
        icon = "📈"
        color = COLORS["success"]
        status = "Increasing"
    elif value < threshold_negative:
        icon = "📉"
        color = COLORS["danger"]
        status = "Decreasing"
    else:
        icon = "➡️"
        color = COLORS["warning"]
        status = "Stable"

    st.markdown(f"""
    <div style="padding: 1rem; background-color: {color}15; border-left: 4px solid {color}; border-radius: 4px;">
        <h4 style="margin: 0;">{icon} {label}: {status}</h4>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: bold; color: {color};">{value:+.1f}%</p>
    </div>
    """, unsafe_allow_html=True)


def display_stat_box(
    title: str,
    value: Union[int, float, str],
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    color: str = "primary"
):
    """
    Display a styled statistics box.

    Args:
        title: Box title
        value: Main value to display
        subtitle: Additional info text
        icon: Emoji icon
        color: Color theme ('primary', 'success', 'warning', 'danger', 'info')
    """
    color_value = COLORS.get(color, COLORS["primary"])

    st.markdown(f"""
    <div style="
        padding: 1.5rem;
        background-color: white;
        border: 2px solid {color_value};
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    ">
        {f'<div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>' if icon else ''}
        <h4 style="margin: 0; color: #6C757D;">{title}</h4>
        <h2 style="margin: 0.5rem 0; color: {color_value};">{value}</h2>
        {f'<p style="margin: 0; color: #6C757D; font-size: 0.9rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def display_ranking_list(
    items: list,
    title: str = "Rankings",
    show_index: bool = True
):
    """
    Display a ranked list of items.

    Args:
        items: List of items to display
        title: List title
        show_index: Whether to show ranking numbers

    Example:
        >>> items = [
        ...     {"name": "United States", "value": 29.4},
        ...     {"name": "China", "value": 27.3},
        ...     {"name": "ASEAN", "value": 15.2}
        ... ]
        >>> display_ranking_list(items, "Top Export Markets")
    """
    st.markdown(f"### {title}")

    for i, item in enumerate(items, 1):
        if show_index:
            # Medal emojis for top 3
            if i == 1:
                prefix = "🥇"
            elif i == 2:
                prefix = "🥈"
            elif i == 3:
                prefix = "🥉"
            else:
                prefix = f"**{i}.**"

            st.markdown(f"{prefix} **{item['name']}**: {item['value']:.1f}%")
        else:
            st.markdown(f"• **{item['name']}**: {item['value']:.1f}%")
