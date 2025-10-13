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
            "size": 12,
            "color": COLORS["text"]
        },
        "plot_bgcolor": COLORS["background"],
        "paper_bgcolor": COLORS["background"],
        "margin": {"l": 60, "r": 40, "t": 60, "b": 60},
        "hovermode": "closest",
        "hoverlabel": {
            "bgcolor": "white",
            "font_size": 12,
            "font_family": "Arial"
        },
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.2,
            "xanchor": "center",
            "x": 0.5
        },
        "xaxis": {
            "showgrid": True,
            "gridcolor": "#E5E5E5",
            "gridwidth": 1,
            "zeroline": False
        },
        "yaxis": {
            "showgrid": True,
            "gridcolor": "#E5E5E5",
            "gridwidth": 1,
            "zeroline": False
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
