"""
Reusable Chart Components Library

This module provides reusable Plotly chart functions with consistent styling
for the Taiwan Export Analysis Dashboard.

Chart types:
- Line charts (time series)
- Bar charts (comparisons)
- Pie charts (market share)
- Waterfall charts (trade balance)
- Sankey diagrams (trade flows)
- Heatmaps (correlation matrix)
- Area charts (stacked trends)
- Scatter plots (correlations)
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any, Optional, Union
import streamlit as st

from streamlit_app.config.theme import COLORS, CHART_TEMPLATE, CHART_CONFIG


def create_line_chart(
    df: pd.DataFrame,
    x: str,
    y: Union[str, List[str]],
    title: str,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    color_map: Optional[Dict[str, str]] = None,
    show_markers: bool = True,
    height: int = 400
) -> go.Figure:
    """
    Create an interactive line chart for time series data.

    Args:
        df: DataFrame containing the data
        x: Column name for x-axis
        y: Column name(s) for y-axis (single or multiple lines)
        title: Chart title
        xlabel: X-axis label (optional)
        ylabel: Y-axis label (optional)
        color_map: Dictionary mapping line names to colors
        show_markers: Whether to show markers on lines
        height: Chart height in pixels

    Returns:
        Plotly Figure object

    Examples:
        >>> fig = create_line_chart(df, x='year_month', y='export_value',
        ...                         title='Export Trends')
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    fig = go.Figure()

    # Handle single or multiple y columns
    y_columns = [y] if isinstance(y, str) else y

    for i, col in enumerate(y_columns):
        color = None
        if color_map and col in color_map:
            color = color_map[col]
        elif not color_map:
            color = COLORS["chart_colors"][i % len(COLORS["chart_colors"])]

        mode = 'lines+markers' if show_markers else 'lines'

        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[col],
            name=col,
            mode=mode,
            line=dict(color=color, width=2),
            marker=dict(size=6),
            hovertemplate='%{x}<br>%{y:,.2f}<extra></extra>'
        ))

    # Update layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, weight='bold')),
        xaxis_title=xlabel or x,
        yaxis_title=ylabel or "",
        height=height,
        **CHART_TEMPLATE["layout"]
    )

    return fig


def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    orientation: str = 'v',
    color_column: Optional[str] = None,
    color_map: Optional[Dict[str, str]] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    show_values: bool = True,
    height: int = 400
) -> go.Figure:
    """
    Create an interactive bar chart.

    Args:
        df: DataFrame containing the data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        orientation: 'v' for vertical, 'h' for horizontal
        color_column: Column to use for color coding
        color_map: Dictionary mapping categories to colors
        xlabel: X-axis label
        ylabel: Y-axis label
        show_values: Whether to display values on bars
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    # Determine color
    if color_column:
        colors = [color_map.get(val, COLORS["primary"]) if color_map else COLORS["primary"]
                  for val in df[color_column]]
    else:
        colors = COLORS["primary"]

    fig = go.Figure()

    if orientation == 'h':
        fig.add_trace(go.Bar(
            x=df[y],
            y=df[x],
            orientation='h',
            marker=dict(color=colors),
            text=df[y] if show_values else None,
            texttemplate='%{text:,.0f}' if show_values else None,
            textposition='outside',
            hovertemplate='%{y}<br>%{x:,.2f}<extra></extra>'
        ))
    else:
        fig.add_trace(go.Bar(
            x=df[x],
            y=df[y],
            marker=dict(color=colors),
            text=df[y] if show_values else None,
            texttemplate='%{text:,.0f}' if show_values else None,
            textposition='outside',
            hovertemplate='%{x}<br>%{y:,.2f}<extra></extra>'
        ))

    # Update layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, weight='bold')),
        xaxis_title=xlabel or x,
        yaxis_title=ylabel or y,
        height=height,
        showlegend=False,
        **CHART_TEMPLATE["layout"]
    )

    return fig


def create_pie_chart(
    df: pd.DataFrame,
    values: str,
    names: str,
    title: str,
    color_map: Optional[Dict[str, str]] = None,
    hole: float = 0.3,
    height: int = 400
) -> go.Figure:
    """
    Create an interactive pie/donut chart.

    Args:
        df: DataFrame containing the data
        values: Column name for values
        names: Column name for labels
        title: Chart title
        color_map: Dictionary mapping categories to colors
        hole: Size of center hole (0 = pie, >0 = donut)
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    # Assign colors
    if color_map:
        colors = [color_map.get(name, COLORS["chart_colors"][i % len(COLORS["chart_colors"])])
                  for i, name in enumerate(df[names])]
    else:
        colors = COLORS["chart_colors"]

    fig = go.Figure(data=[go.Pie(
        labels=df[names],
        values=df[values],
        hole=hole,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textposition='auto',
        hovertemplate='%{label}<br>%{value:,.2f}<br>%{percent}<extra></extra>'
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, weight='bold')),
        height=height,
        **CHART_TEMPLATE["layout"]
    )

    return fig


def create_grouped_bar_chart(
    df: pd.DataFrame,
    x: str,
    y_columns: List[str],
    title: str,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    color_map: Optional[Dict[str, str]] = None,
    height: int = 400
) -> go.Figure:
    """
    Create a grouped bar chart for comparing multiple categories.

    Args:
        df: DataFrame containing the data
        x: Column name for x-axis (categories)
        y_columns: List of column names to compare
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        color_map: Dictionary mapping column names to colors
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    for i, col in enumerate(y_columns):
        color = None
        if color_map and col in color_map:
            color = color_map[col]
        else:
            color = COLORS["chart_colors"][i % len(COLORS["chart_colors"])]

        fig.add_trace(go.Bar(
            x=df[x],
            y=df[col],
            name=col,
            marker=dict(color=color),
            hovertemplate='%{x}<br>%{y:,.2f}<extra></extra>'
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, weight='bold')),
        xaxis_title=xlabel or x,
        yaxis_title=ylabel or "",
        barmode='group',
        height=height,
        **CHART_TEMPLATE["layout"]
    )

    return fig


def create_stacked_area_chart(
    df: pd.DataFrame,
    x: str,
    y_columns: List[str],
    title: str,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    color_map: Optional[Dict[str, str]] = None,
    height: int = 400
) -> go.Figure:
    """
    Create a stacked area chart for showing composition over time.

    Args:
        df: DataFrame containing the data
        x: Column name for x-axis
        y_columns: List of column names to stack
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        color_map: Dictionary mapping column names to colors
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    for i, col in enumerate(y_columns):
        color = None
        if color_map and col in color_map:
            color = color_map[col]
        else:
            color = COLORS["chart_colors"][i % len(COLORS["chart_colors"])]

        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[col],
            name=col,
            mode='lines',
            stackgroup='one',
            fillcolor=color,
            line=dict(color=color, width=0),
            hovertemplate='%{x}<br>%{y:,.2f}<extra></extra>'
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, weight='bold')),
        xaxis_title=xlabel or x,
        yaxis_title=ylabel or "",
        height=height,
        **CHART_TEMPLATE["layout"]
    )

    return fig


def create_heatmap(
    df: pd.DataFrame,
    x: str,
    y: str,
    values: str,
    title: str,
    colorscale: str = 'RdYlGn',
    height: int = 400
) -> go.Figure:
    """
    Create a heatmap for correlation or comparison matrices.

    Args:
        df: DataFrame containing the data
        x: Column name for x-axis
        y: Column name for y-axis
        values: Column name for cell values
        title: Chart title
        colorscale: Plotly colorscale name
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    # Pivot data for heatmap
    pivot_df = df.pivot(index=y, columns=x, values=values)

    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale=colorscale,
        hovertemplate='%{x}<br>%{y}<br>%{z:,.2f}<extra></extra>',
        text=pivot_df.values,
        texttemplate='%{text:.1f}',
        textfont={"size": 10}
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, weight='bold')),
        height=height,
        **CHART_TEMPLATE["layout"]
    )

    return fig


def create_waterfall_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    measure: Optional[List[str]] = None,
    height: int = 400
) -> go.Figure:
    """
    Create a waterfall chart for showing cumulative effects.

    Args:
        df: DataFrame containing the data
        x: Column name for categories
        y: Column name for values
        title: Chart title
        measure: List indicating type ('relative', 'total', 'absolute')
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    if measure is None:
        # Auto-detect: last item is total
        measure = ['relative'] * (len(df) - 1) + ['total']

    fig = go.Figure(go.Waterfall(
        name="",
        orientation="v",
        measure=measure,
        x=df[x],
        y=df[y],
        textposition="outside",
        text=df[y],
        texttemplate='%{text:,.0f}',
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": COLORS["success"]}},
        decreasing={"marker": {"color": COLORS["danger"]}},
        totals={"marker": {"color": COLORS["secondary"]}}
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, weight='bold')),
        height=height,
        showlegend=False,
        **CHART_TEMPLATE["layout"]
    )

    return fig


def create_sankey_diagram(
    df: pd.DataFrame,
    source: str,
    target: str,
    value: str,
    title: str,
    height: int = 500,
    node_color_map: Optional[Dict[str, str]] = None,
    fix_node_positions: bool = True
) -> go.Figure:
    """
    Create a Sankey diagram for flow visualization.

    Args:
        df: DataFrame containing flow data
        source: Column name for source nodes
        target: Column name for target nodes
        value: Column name for flow values
        title: Chart title
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    # Create node labels with deterministic ordering so the layout is stable:
    # 1) keep sources in the order they appear
    # 2) then append targets (excluding duplicates)
    left_nodes = list(pd.unique(df[source]))
    right_nodes = [n for n in pd.unique(df[target]) if n not in left_nodes]
    all_nodes = left_nodes + right_nodes
    node_dict = {node: idx for idx, node in enumerate(all_nodes)}

    # Map sources and targets to indices
    source_indices = [node_dict[src] for src in df[source]]
    target_indices = [node_dict[tgt] for tgt in df[target]]

    # Assign colors (allow caller to override specific nodes)
    default_colors = COLORS["chart_colors"]
    node_colors = []
    for i, n in enumerate(all_nodes):
        if node_color_map and n in node_color_map:
            node_colors.append(node_color_map[n])
        else:
            node_colors.append(default_colors[i % len(default_colors)])

    # Color links by their target to help readability
    def _hex_to_rgba(h: str, a: float = 0.45) -> str:
        h = h.lstrip('#')
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r},{g},{b},{a})"

    link_colors = []
    for t in df[target].tolist():
        color = None
        # try to map link color to target node color
        if t in node_dict:
            idx = node_dict[t]
            color = _hex_to_rgba(node_colors[idx])
        link_colors.append(color or 'rgba(150,150,150,0.4)')

    node_kwargs = dict(
        pad=15,
        thickness=20,
        line=dict(color="white", width=0.5),
        label=all_nodes,
        color=node_colors
    )

    # Optionally fix node positions to keep sources on the left and targets on the right
    if fix_node_positions:
        n_left, n_right = len(left_nodes), len(right_nodes)
        # evenly space nodes along y-axis
        if n_left > 0:
            node_kwargs["x"] = [0.01] * n_left + [0.99] * n_right
            # y positions between 0 and 1 (avoid touching edges)
            if n_left == 1:
                left_y = [0.5]
            else:
                left_y = [i / (n_left - 1) for i in range(n_left)]
            if n_right == 1:
                right_y = [0.5]
            else:
                right_y = [i / (n_right - 1) for i in range(n_right)]
            node_kwargs["y"] = left_y + right_y

    fig = go.Figure(data=[go.Sankey(
        arrangement='snap',
        node=node_kwargs,
        link=dict(
            source=source_indices,
            target=target_indices,
            value=df[value].tolist(),
            color=link_colors,
            hovertemplate='%{source.label} → %{target.label}<br>%{value:.1f} pp<extra></extra>'
        )
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, weight='bold')),
        height=height,
        font=dict(size=12)
    )

    return fig


def create_scatter_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color_column: Optional[str] = None,
    size_column: Optional[str] = None,
    text_column: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    height: int = 400
) -> go.Figure:
    """
    Create an interactive scatter plot.

    Args:
        df: DataFrame containing the data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        color_column: Column for color coding
        size_column: Column for sizing markers
        text_column: Column for text labels
        xlabel: X-axis label
        ylabel: Y-axis label
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df[x],
        y=df[y],
        mode='markers+text' if text_column else 'markers',
        marker=dict(
            size=df[size_column] if size_column else 10,
            color=df[color_column] if color_column else COLORS["primary"],
            colorscale='Viridis' if color_column else None,
            showscale=True if color_column else False,
            line=dict(width=1, color='white')
        ),
        text=df[text_column] if text_column else None,
        textposition='top center',
        hovertemplate='%{x:,.2f}<br>%{y:,.2f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, weight='bold')),
        xaxis_title=xlabel or x,
        yaxis_title=ylabel or y,
        height=height,
        **CHART_TEMPLATE["layout"]
    )

    return fig


def apply_chart_config(fig: go.Figure) -> go.Figure:
    """
    Apply consistent configuration to any Plotly figure.

    Args:
        fig: Plotly Figure object

    Returns:
        Updated Figure object with consistent config
    """
    fig.update_layout(**CHART_TEMPLATE["layout"])
    return fig
