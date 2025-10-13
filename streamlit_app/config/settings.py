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
    "app_title": "台灣出口分析儀表板",
    "app_subtitle": "ICT 出口激增與貿易轉移模式分析",
    "version": "2.0.0",
    "author": "潘驄杰",

    # Data settings
    "data_source": "中華民國財政部關務署",
    "data_month": "2025年8月",
    "data_format": "parquet",  # Default format: parquet, csv, or json

    # Display settings
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        "Get Help": "https://github.com/yourusername/taiwan-export-analysis",
        "Report a bug": "https://github.com/yourusername/taiwan-export-analysis/issues",
        "About": "台灣 ICT 出口激增與貿易轉移模式分析儀表板"
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
            "name": "執行摘要",
            "icon": "📊",
            "path": "1_📊_Executive_Summary.py",
            "description": "關鍵指標與趨勢總覽"
        },
        {
            "name": "美國貿易激增",
            "icon": "🇺🇸",
            "path": "2_🇺🇸_US_Trade_Surge.py",
            "description": "主題一：ICT 產品對美出口激增分析"
        },
        {
            "name": "貿易轉移模式",
            "icon": "🔄",
            "path": "3_🔄_Trade_Diversion.py",
            "description": "主題二：貿易轉移模式分析"
        },
        {
            "name": "DIKW 分析架構",
            "icon": "📈",
            "path": "4_📈_DIKW_Analysis.py",
            "description": "資料-資訊-知識-智慧分析架構"
        },
        {
            "name": "洞察與智慧",
            "icon": "💡",
            "path": "5_💡_Insights_Wisdom.py",
            "description": "可行動洞察與策略建議"
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
        "name": "資料層",
        "icon": "📊",
        "color": "#1f77b4",
        "description": "原始統計數據與測量值",
        "tables": [
            {"id": "table01", "name": "進出口貿易值及年增率"},
            {"id": "table02", "name": "主要出口商品分類"},
            {"id": "table03", "name": "主要進口商品分類"},
            {"id": "table04", "name": "出口主要貨品詳細資料"},
            {"id": "table05", "name": "進口主要貨品詳細資料"},
            {"id": "table06", "name": "出口貿易結構"},
            {"id": "table07", "name": "進口貿易結構"},
            {"id": "table08", "name": "對主要國家（地區）出口值及年增率"},
            {"id": "table09", "name": "自主要國家（地區）進口值及年增率"},
            {"id": "table10", "name": "對主要國家（地區）貿易順差"},
            {"id": "table11", "name": "對中國大陸及香港出口主要貨品"},
            {"id": "table12", "name": "對新南向政策18國出口值及年增率"},
            {"id": "table13", "name": "季節調整後進出口貿易值"},
            {"id": "table14", "name": "主要國家（地區）進出口值及年增率"},
            {"id": "table15", "name": "進出口價格相關指標"},
            {"id": "table16", "name": "主要國家貨幣對美元匯率"}
        ]
    },
    "information": {
        "name": "資訊層",
        "icon": "📈",
        "color": "#ff7f0e",
        "description": "經處理的趨勢與模式"
    },
    "knowledge": {
        "name": "知識層",
        "icon": "🧠",
        "color": "#2ca02c",
        "description": "對因果關係的理解"
    },
    "wisdom": {
        "name": "智慧層",
        "icon": "💡",
        "color": "#d62728",
        "description": "可行動的洞察與建議"
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
