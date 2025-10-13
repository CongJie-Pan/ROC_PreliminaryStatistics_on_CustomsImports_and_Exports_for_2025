"""
Data Table Components

This module provides reusable components for displaying data tables
with consistent styling and formatting.
"""

import io
import streamlit as st
import pandas as pd
from typing import Optional, List, Dict, Any


def display_dataframe(
    df: pd.DataFrame,
    title: Optional[str] = None,
    height: Optional[int] = None,
    use_container_width: bool = True,
    hide_index: bool = True,
    column_config: Optional[Dict[str, Any]] = None
):
    """
    Display a styled dataframe with optional title.

    Args:
        df: DataFrame to display
        title: Table title (optional)
        height: Table height in pixels
        use_container_width: Whether to use full container width
        hide_index: Whether to hide the index column
        column_config: Column configuration for st.dataframe
    """
    if title:
        st.markdown(f"### {title}")

    st.dataframe(
        df,
        height=height,
        use_container_width=use_container_width,
        hide_index=hide_index,
        column_config=column_config
    )


def display_summary_table(
    data: Dict[str, Any],
    title: str = "Summary Statistics"
):
    """
    Display a summary statistics table from a dictionary.

    Args:
        data: Dictionary of label-value pairs
        title: Table title

    Example:
        >>> data = {
        ...     "Total Export Value": "$123.4B",
        ...     "Growth Rate": "+15.2%",
        ...     "Market Share": "29.4%"
        ... }
        >>> display_summary_table(data)
    """
    st.markdown(f"### {title}")

    # Convert to DataFrame
    df = pd.DataFrame(list(data.items()), columns=["Metric", "Value"])

    st.table(df)


def display_comparison_table(
    df: pd.DataFrame,
    index_col: str,
    compare_cols: List[str],
    title: str = "Comparison",
    highlight_max: bool = True,
    highlight_min: bool = False
):
    """
    Display a comparison table with optional highlighting.

    Args:
        df: DataFrame to display
        index_col: Column to use as index
        compare_cols: Columns to compare
        title: Table title
        highlight_max: Whether to highlight maximum values
        highlight_min: Whether to highlight minimum values
    """
    st.markdown(f"### {title}")

    # Set index
    display_df = df.set_index(index_col)[compare_cols]

    # Apply styling
    def highlight_values(s):
        styles = [''] * len(s)
        if highlight_max:
            max_idx = s.idxmax()
            styles[s.index.get_loc(max_idx)] = 'background-color: #d4edda; font-weight: bold;'
        if highlight_min:
            min_idx = s.idxmin()
            styles[s.index.get_loc(min_idx)] = 'background-color: #f8d7da; font-weight: bold;'
        return styles

    styled_df = display_df.style.apply(highlight_values, axis=0)

    st.dataframe(styled_df, use_container_width=True)


def display_paginated_table(
    df: pd.DataFrame,
    title: Optional[str] = None,
    rows_per_page: int = 10,
    show_filters: bool = False
):
    """
    Display a paginated table with optional filtering.

    Args:
        df: DataFrame to display
        title: Table title
        rows_per_page: Number of rows per page
        show_filters: Whether to show column filters
    """
    if title:
        st.markdown(f"### {title}")

    # Initialize session state for pagination
    if 'table_page' not in st.session_state:
        st.session_state.table_page = 0

    # Filters
    filtered_df = df.copy()

    if show_filters:
        cols = st.columns(len(df.columns))
        for i, col in enumerate(df.columns):
            with cols[i]:
                if df[col].dtype in ['int64', 'float64']:
                    # Numeric filter
                    min_val = float(df[col].min())
                    max_val = float(df[col].max())
                    selected_range = st.slider(
                        f"{col}",
                        min_val, max_val, (min_val, max_val),
                        key=f"filter_{col}"
                    )
                    filtered_df = filtered_df[
                        (filtered_df[col] >= selected_range[0]) &
                        (filtered_df[col] <= selected_range[1])
                    ]
                else:
                    # Categorical filter
                    unique_vals = df[col].unique()
                    selected_vals = st.multiselect(
                        f"{col}",
                        unique_vals,
                        default=unique_vals,
                        key=f"filter_{col}"
                    )
                    filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]

    # Pagination
    total_pages = len(filtered_df) // rows_per_page + (1 if len(filtered_df) % rows_per_page > 0 else 0)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("← Previous") and st.session_state.table_page > 0:
            st.session_state.table_page -= 1

    with col2:
        st.markdown(f"<p style='text-align: center;'>Page {st.session_state.table_page + 1} of {total_pages}</p>",
                    unsafe_allow_html=True)

    with col3:
        if st.button("Next →") and st.session_state.table_page < total_pages - 1:
            st.session_state.table_page += 1

    # Display current page
    start_idx = st.session_state.table_page * rows_per_page
    end_idx = start_idx + rows_per_page

    st.dataframe(
        filtered_df.iloc[start_idx:end_idx],
        use_container_width=True,
        hide_index=True
    )

    # Show total
    st.caption(f"Showing {start_idx + 1}-{min(end_idx, len(filtered_df))} of {len(filtered_df)} rows")


def create_downloadable_table(
    df: pd.DataFrame,
    filename: str = "data",
    title: Optional[str] = None,
    formats: List[str] = ["csv", "xlsx", "json"]
):
    """
    Display a table with download buttons for multiple formats.

    Args:
        df: DataFrame to display and make downloadable
        filename: Base filename for downloads
        title: Table title
        formats: List of formats to offer ('csv', 'xlsx', 'json')
    """
    if title:
        st.markdown(f"### {title}")

    # Display table
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Download buttons
    st.markdown("**Download data:**")
    cols = st.columns(len(formats))

    for col, fmt in zip(cols, formats):
        with col:
            if fmt == "csv":
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📄 CSV",
                    data=csv_data,
                    file_name=f"{filename}.csv",
                    mime="text/csv"
                )
            elif fmt == "xlsx":
                # This requires openpyxl
                try:
                    excel_buffer = io.BytesIO()
                    df.to_excel(excel_buffer, index=False, engine='openpyxl')
                    st.download_button(
                        label="📊 Excel",
                        data=excel_buffer.getvalue(),
                        file_name=f"{filename}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except ImportError:
                    st.warning("Excel export requires openpyxl library")
            elif fmt == "json":
                json_data = df.to_json(orient='records', indent=2).encode('utf-8')
                st.download_button(
                    label="📋 JSON",
                    data=json_data,
                    file_name=f"{filename}.json",
                    mime="application/json"
                )


def display_pivot_table(
    df: pd.DataFrame,
    index: str,
    columns: str,
    values: str,
    aggfunc: str = 'sum',
    title: Optional[str] = None
):
    """
    Display a pivot table with aggregation.

    Args:
        df: DataFrame to pivot
        index: Column to use as row index
        columns: Column to use as column headers
        values: Column to aggregate
        aggfunc: Aggregation function ('sum', 'mean', 'count', etc.)
        title: Table title
    """
    if title:
        st.markdown(f"### {title}")

    pivot_df = df.pivot_table(
        index=index,
        columns=columns,
        values=values,
        aggfunc=aggfunc,
        fill_value=0
    )

    st.dataframe(pivot_df, use_container_width=True)
