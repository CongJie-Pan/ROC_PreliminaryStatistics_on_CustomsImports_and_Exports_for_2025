"""
UI theme and styling configuration.

This module contains color schemes, chart templates, and styling constants
used throughout the dashboard.
"""

from typing import Dict, List, Any

# Color palette
COLORS = {
    # Primary colors
    "primary": "#FF4B4B",
    "secondary": "#0068C9",
    "success": "#09AB3B",
    "warning": "#FFA421",
    "danger": "#FF4B4B",
    "info": "#00C0F2",

    # Background colors
    "background": "#FFFFFF",
    "background_secondary": "#F0F2F6",
    "background_dark": "#262730",

    # Text colors
    "text": "#262730",
    "text_secondary": "#6C757D",
    "text_light": "#FFFFFF",

    # Chart colors (professional color palette)
    "chart_colors": [
        "#1f77b4",  # Blue
        "#ff7f0e",  # Orange
        "#2ca02c",  # Green
        "#d62728",  # Red
        "#9467bd",  # Purple
        "#8c564b",  # Brown
        "#e377c2",  # Pink
        "#7f7f7f",  # Gray
        "#bcbd22",  # Yellow-green
        "#17becf"   # Cyan
    ],

    # Country/region specific colors
    "country_colors": {
        "United States": "#1f77b4",
        "China": "#d62728",
        "Hong Kong": "#ff7f0e",
        "ASEAN": "#2ca02c",
        "EU": "#9467bd",
        "Japan": "#8c564b",
        "Other": "#7f7f7f"
    },

    # DIKW layer colors
    "dikw_colors": {
        "data": "#1f77b4",
        "information": "#ff7f0e",
        "knowledge": "#2ca02c",
        "wisdom": "#d62728"
    }
}

# Chart template (Plotly)
CHART_TEMPLATE: Dict[str, Any] = {
    "layout": {
        "font": {
            "family": "Arial, sans-serif",
            "size": 14,
            "color": "#0e1117"  # Pure black for maximum contrast
        },
        "plot_bgcolor": COLORS["background"],
        "paper_bgcolor": COLORS["background"],
        # Add extra top/bottom margin to avoid legend/axis overlap
        "margin": {"l": 60, "r": 40, "t": 90, "b": 110},
        "hovermode": "closest",
        "hoverlabel": {
            "bgcolor": "white",
            "font": {
                "size": 14,
                "color": "#0e1117",
                "family": "Arial"
            },
            "bordercolor": "#0e1117"
        },
        "legend": {
            "orientation": "h",
            # Place legend above the plot to prevent overlap with
            # x-axis tick labels and title, which sit at the bottom.
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "center",
            "x": 0.5,
            "font": {
                "size": 12,
                "color": "#0e1117"
            },
            "itemsizing": "constant",
            "tracegroupgap": 40,
            "itemwidth": 50
        },
        "xaxis": {
            "showgrid": True,
            "gridcolor": "#E5E5E5",
            "gridwidth": 1,
            "zeroline": False,
            "title": {
                "font": {
                    "size": 14,
                    "color": "#0e1117",
                    "family": "Arial"
                }
            },
            "tickfont": {
                "size": 13,
                "color": "#0e1117"
            }
        },
        "yaxis": {
            "showgrid": True,
            "gridcolor": "#E5E5E5",
            "gridwidth": 1,
            "zeroline": False,
            "title": {
                "font": {
                    "size": 14,
                    "color": "#0e1117",
                    "family": "Arial"
                }
            },
            "tickfont": {
                "size": 13,
                "color": "#0e1117"
            }
        }
    }
}

# Metric card styling
METRIC_STYLE: Dict[str, str] = {
    "border": "1px solid #E5E5E5",
    "border-radius": "8px",
    "padding": "1rem",
    "background-color": COLORS["background"],
    "box-shadow": "0 2px 4px rgba(0,0,0,0.1)"
}

# Typography
TYPOGRAPHY = {
    "h1": {"size": "2.5rem", "weight": "700", "color": COLORS["text"]},
    "h2": {"size": "2rem", "weight": "600", "color": COLORS["text"]},
    "h3": {"size": "1.5rem", "weight": "600", "color": COLORS["text"]},
    "h4": {"size": "1.25rem", "weight": "500", "color": COLORS["text"]},
    "body": {"size": "1rem", "weight": "400", "color": COLORS["text"]},
    "caption": {"size": "0.875rem", "weight": "400", "color": COLORS["text_secondary"]}
}

# Chart-specific configurations
CHART_CONFIG = {
    # Display options
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "pan2d",
        "lasso2d",
        "select2d",
        "autoScale2d"
    ],
    "toImageButtonOptions": {
        "format": "png",
        "filename": "taiwan_export_chart",
        "height": 600,
        "width": 1000,
        "scale": 2
    }
}

# Custom CSS
CUSTOM_CSS = """
<style>
    /* Main container */
    .main {
        padding: 2rem;
    }

    /* Metric cards */
    .metric-card {
        border: 1px solid #E5E5E5;
        border-radius: 8px;
        padding: 1.5rem;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    /* Headers */
    .page-header {
        border-bottom: 3px solid #FF4B4B;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
    }

    /* Info boxes */
    .info-box {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }

    .warning-box {
        background-color: #FFF3E0;
        border-left: 4px solid #FF9800;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }

    .success-box {
        background-color: #E8F5E9;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }

    /* Streamlit tables and dataframes - ensure text is visible with high contrast */

    /* General table styles */
    table {
        background-color: #ffffff !important;
    }

    table thead th {
        color: #0e1117 !important;
        background-color: #f0f2f6 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #e6e6e6 !important;
    }

    table tbody td {
        color: #0e1117 !important;
        background-color: #ffffff !important;
    }

    table tbody tr {
        background-color: #ffffff !important;
    }

    table tbody tr:hover {
        background-color: #f9f9f9 !important;
    }

    /* Streamlit DataFrame component */
    .stDataFrame {
        color: #0e1117 !important;
    }

    .stDataFrame table {
        background-color: #ffffff !important;
    }

    .stDataFrame thead th {
        color: #0e1117 !important;
        background-color: #f0f2f6 !important;
        font-weight: 600 !important;
    }

    .stDataFrame tbody td {
        color: #0e1117 !important;
        background-color: #ffffff !important;
    }

    .stDataFrame tbody tr {
        background-color: #ffffff !important;
    }

    /* Streamlit Table component */
    .stTable {
        color: #0e1117 !important;
    }

    .stTable table {
        background-color: #ffffff !important;
    }

    .stTable thead th {
        color: #0e1117 !important;
        background-color: #f0f2f6 !important;
        font-weight: 600 !important;
    }

    .stTable tbody td {
        color: #0e1117 !important;
        background-color: #ffffff !important;
    }

    .stTable tbody tr {
        background-color: #ffffff !important;
    }

    /* Pandas DataFrame styling */
    .dataframe {
        color: #0e1117 !important;
        background-color: #ffffff !important;
    }

    .dataframe thead th {
        color: #0e1117 !important;
        background-color: #f0f2f6 !important;
        font-weight: 600 !important;
    }

    .dataframe tbody td {
        color: #0e1117 !important;
        background-color: #ffffff !important;
    }

    .dataframe tbody tr {
        background-color: #ffffff !important;
    }

    /* Markdown tables */
    .stMarkdown table {
        color: #0e1117 !important;
        background-color: #ffffff !important;
        border-collapse: collapse !important;
    }

    .stMarkdown table thead th {
        color: #0e1117 !important;
        background-color: #f0f2f6 !important;
        font-weight: 600 !important;
        padding: 0.5rem !important;
        border: 1px solid #e6e6e6 !important;
    }

    .stMarkdown table tbody td {
        color: #0e1117 !important;
        background-color: #ffffff !important;
        padding: 0.5rem !important;
        border: 1px solid #e6e6e6 !important;
    }

    .stMarkdown table tbody tr {
        background-color: #ffffff !important;
    }

    /* Tables inside alert/info boxes */
    .stAlert table, .stInfo table, .stSuccess table, .stWarning table, .stError table {
        color: #0e1117 !important;
        background-color: #ffffff !important;
    }

    .stAlert table td, .stInfo table td, .stSuccess table td, .stWarning table td, .stError table td {
        color: #0e1117 !important;
        background-color: #ffffff !important;
    }

    /* Element container tables */
    .element-container table {
        background-color: #ffffff !important;
    }

    .element-container table td, .element-container table th {
        color: #0e1117 !important;
    }

    /* Data editor tables */
    [data-testid="stDataFrame"] {
        color: #0e1117 !important;
    }

    [data-testid="stTable"] {
        color: #0e1117 !important;
    }

    [data-testid="stDataFrame"] table, [data-testid="stTable"] table {
        background-color: #ffffff !important;
    }

    [data-testid="stDataFrame"] td, [data-testid="stTable"] td,
    [data-testid="stDataFrame"] th, [data-testid="stTable"] th {
        color: #0e1117 !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Responsive design */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }

        .metric-card {
            margin-bottom: 1rem;
        }
    }
</style>
"""

# Theme configuration
THEME: Dict[str, Any] = {
    "colors": COLORS,
    "chart_template": CHART_TEMPLATE,
    "chart_config": CHART_CONFIG,
    "metric_style": METRIC_STYLE,
    "typography": TYPOGRAPHY,
    "custom_css": CUSTOM_CSS
}
