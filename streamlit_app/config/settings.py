"""
Application settings and configuration.

This module contains all application-level settings including:
- Data paths
- Display settings
- Page configurations
- Feature flags
"""

from pathlib import Path
from typing import Dict, Any

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PARQUET_DIR = PROCESSED_DATA_DIR / "parquet"
CSV_DIR = PROCESSED_DATA_DIR / "csv"
JSON_DIR = PROCESSED_DATA_DIR / "json"

# Application settings
SETTINGS: Dict[str, Any] = {
    # Application metadata
    "app_title": "Taiwan Export Analysis Dashboard",
    "app_subtitle": "ICT Export Surge & Trade Diversion Pattern Analysis",
    "version": "2.0.0",
    "author": "潘驄杰",

    # Data settings
    "data_source": "ROC Ministry of Finance",
    "data_month": "August 2025",
    "data_format": "parquet",  # Default format: parquet, csv, or json

    # Display settings
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        "Get Help": "https://github.com/yourusername/taiwan-export-analysis",
        "Report a bug": "https://github.com/yourusername/taiwan-export-analysis/issues",
        "About": "Taiwan's ICT Export Surge and Trade Diversion Pattern Analysis Dashboard"
    },

    # Performance settings
    "cache_ttl": 3600,  # Cache time-to-live in seconds (1 hour)
    "max_rows_display": 1000,  # Maximum rows to display in tables
    "chart_height": 400,  # Default chart height in pixels

    # Feature flags
    "enable_data_export": True,
    "enable_comparison_mode": True,
    "enable_advanced_filters": True,

    # Page configurations
    "pages": [
        {
            "name": "Executive Summary",
            "icon": "📊",
            "path": "1_📊_Executive_Summary.py",
            "description": "Overview of key metrics and trends"
        },
        {
            "name": "US Trade Surge",
            "icon": "🇺🇸",
            "path": "2_🇺🇸_US_Trade_Surge.py",
            "description": "Theme 1: ICT product export surge to US"
        },
        {
            "name": "Trade Diversion",
            "icon": "🔄",
            "path": "3_🔄_Trade_Diversion.py",
            "description": "Theme 2: Trade diversion pattern analysis"
        },
        {
            "name": "DIKW Analysis",
            "icon": "📈",
            "path": "4_📈_DIKW_Analysis.py",
            "description": "Data-Information-Knowledge-Wisdom framework"
        },
        {
            "name": "Insights & Wisdom",
            "icon": "💡",
            "path": "5_💡_Insights_Wisdom.py",
            "description": "Actionable insights and recommendations"
        }
    ]
}

# Table mappings
TABLE_MAPPING: Dict[str, str] = {
    "table01": "overall_trade",
    "table02": "export_commodities",
    "table03": "import_commodities",
    "table04": "export_items_detail",
    "table05": "import_items_detail",
    "table06": "export_structure",
    "table07": "import_structure",
    "table08": "export_by_country",
    "table09": "import_by_country",
    "table10": "trade_balance_by_country",
    "table11": "export_to_china_hk",
    "table12": "export_to_new_southbound",
    "table13": "seasonally_adjusted",
    "table14": "comprehensive_trade",
    "table15": "price_indicators",
    "table16": "exchange_rates"
}

# DIKW layers configuration
DIKW_LAYERS = {
    "data": {
        "name": "Data",
        "icon": "📊",
        "color": "#1f77b4",
        "description": "Raw statistics and measurements"
    },
    "information": {
        "name": "Information",
        "icon": "📈",
        "color": "#ff7f0e",
        "description": "Processed trends and patterns"
    },
    "knowledge": {
        "name": "Knowledge",
        "icon": "🧠",
        "color": "#2ca02c",
        "description": "Understanding of causal relationships"
    },
    "wisdom": {
        "name": "Wisdom",
        "icon": "💡",
        "color": "#d62728",
        "description": "Actionable insights and recommendations"
    }
}

def get_data_path(table_name: str, format: str = "parquet") -> Path:
    """
    Get the file path for a specific data table.

    Args:
        table_name: Name of the table (e.g., 'table08', 'export_by_country')
        format: Data format ('parquet', 'csv', or 'json')

    Returns:
        Path object pointing to the data file
    """
    # Normalize table name
    if table_name in TABLE_MAPPING:
        table_id = table_name
    else:
        # Reverse lookup
        table_id = next((k for k, v in TABLE_MAPPING.items() if v == table_name), table_name)

    # Select directory based on format
    format_dirs = {
        "parquet": PARQUET_DIR,
        "csv": CSV_DIR,
        "json": JSON_DIR
    }

    data_dir = format_dirs.get(format, PARQUET_DIR)
    return data_dir / f"{table_id}.{format}"
