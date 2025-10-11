"""
Schema Definitions for Taiwan Trade Statistics Tables

This module defines the expected schema (column names, data types, and structure)
for all 16 Excel tables after cleaning and standardization.

Author: Claude AI & 潘驄杰
Date: 2025-10-11
"""

from typing import Dict, List

# Schema definitions for each table
# Format: {
#   'column_name': {
#       'dtype': 'data type',
#       'required': True/False,
#       'description': 'Column description'
#   }
# }

SCHEMA_TABLE08 = {
    'year_month': {
        'dtype': 'string',
        'required': True,
        'description': 'Year or year-month identifier'
    },
    'total_export_value_usd_million': {
        'dtype': 'float64',
        'required': True,
        'description': 'Total export value in millions USD'
    },
    'total_export_growth_rate_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'Total export year-over-year growth rate %'
    },
    'china_hk_export_value_usd_million': {
        'dtype': 'float64',
        'required': True,
        'description': 'Export to China/HK in millions USD'
    },
    'china_hk_export_share_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'China/HK share of total exports %'
    },
    'china_hk_export_growth_rate_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'China/HK export growth rate %'
    },
    'us_export_value_usd_million': {
        'dtype': 'float64',
        'required': True,
        'description': 'Export to US in millions USD'
    },
    'us_export_share_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'US share of total exports %'
    },
    'us_export_growth_rate_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'US export growth rate %'
    },
    'asean_export_value_usd_million': {
        'dtype': 'float64',
        'required': True,
        'description': 'Export to ASEAN in millions USD'
    },
    'asean_export_share_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'ASEAN share of total exports %'
    },
    'asean_export_growth_rate_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'ASEAN export growth rate %'
    },
    'japan_export_value_usd_million': {
        'dtype': 'float64',
        'required': True,
        'description': 'Export to Japan in millions USD'
    },
    'japan_export_growth_rate_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'Japan export growth rate %'
    },
    'south_korea_export_value_usd_million': {
        'dtype': 'float64',
        'required': True,
        'description': 'Export to South Korea in millions USD'
    },
    'south_korea_export_growth_rate_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'South Korea export growth rate %'
    },
    'europe_export_value_usd_million': {
        'dtype': 'float64',
        'required': True,
        'description': 'Export to Europe in millions USD'
    },
    'europe_export_growth_rate_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'Europe export growth rate %'
    },
}

SCHEMA_TABLE02 = {
    'year_month': {
        'dtype': 'string',
        'required': True,
        'description': 'Year or year-month identifier'
    },
    'ict_products_export_value_usd_million': {
        'dtype': 'float64',
        'required': True,
        'description': 'ICT products export value in millions USD'
    },
    'ict_products_export_share_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'ICT products share of total exports %'
    },
    'ict_products_export_growth_rate_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'ICT products export growth rate %'
    },
    'electronic_components_export_value_usd_million': {
        'dtype': 'float64',
        'required': True,
        'description': 'Electronic components export value in millions USD'
    },
    'electronic_components_export_share_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'Electronic components share of total exports %'
    },
    'electronic_components_export_growth_rate_pct': {
        'dtype': 'float64',
        'required': False,
        'description': 'Electronic components export growth rate %'
    },
}

# Table ID to schema mapping
SCHEMAS = {
    'table08': SCHEMA_TABLE08,
    'table02': SCHEMA_TABLE02,
    # Add more schemas as needed for other tables
}


def get_schema(table_id: str) -> Dict:
    """
    Get schema definition for a specific table.

    Args:
        table_id: Table identifier (e.g., 'table08')

    Returns:
        Dictionary containing schema definition

    Raises:
        KeyError: If table_id not found
    """
    if table_id not in SCHEMAS:
        raise KeyError(f"Schema not found for table_id: {table_id}")
    return SCHEMAS[table_id]


def get_required_columns(table_id: str) -> List[str]:
    """
    Get list of required columns for a table.

    Args:
        table_id: Table identifier

    Returns:
        List of required column names
    """
    schema = get_schema(table_id)
    return [col for col, spec in schema.items() if spec['required']]


def get_column_dtype(table_id: str, column_name: str) -> str:
    """
    Get expected data type for a column.

    Args:
        table_id: Table identifier
        column_name: Column name

    Returns:
        Data type string (e.g., 'float64', 'string')
    """
    schema = get_schema(table_id)
    if column_name not in schema:
        raise KeyError(f"Column {column_name} not found in schema for {table_id}")
    return schema[column_name]['dtype']
