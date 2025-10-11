"""
Format Converter Module

This module provides multi-format export capabilities:
- Parquet (columnar, compressed, optimized for analytics)
- CSV (UTF-8 with BOM for Excel compatibility)
- JSON (for APIs and web applications)
- SQLite (for complex queries and joins)

Author: Claude AI & 潘驄杰
Date: 2025-10-11
"""

import pandas as pd
import sqlite3
from pathlib import Path
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class FormatConverter:
    """
    Format converter for Taiwan customs trade statistics.

    Supports export to Parquet, CSV, JSON, and SQLite formats.
    """

    def __init__(self, output_base_dir: Optional[Path] = None):
        """
        Initialize format converter.

        Args:
            output_base_dir: Base directory for output files.
                            Defaults to data/processed/
        """
        if output_base_dir is None:
            self.output_base_dir = Path("data/processed")
        else:
            self.output_base_dir = Path(output_base_dir)

        # Create output directories
        self.parquet_dir = self.output_base_dir / "parquet"
        self.csv_dir = self.output_base_dir / "csv"
        self.json_dir = self.output_base_dir / "json"
        self.database_dir = self.output_base_dir / "database"

        # Ensure directories exist
        for directory in [self.parquet_dir, self.csv_dir, self.json_dir, self.database_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def export_to_parquet(
        self,
        df: pd.DataFrame,
        table_id: str,
        compression: str = 'snappy'
    ) -> Path:
        """
        Export dataframe to Parquet format.

        Args:
            df: Input dataframe
            table_id: Table identifier (used for file naming)
            compression: Compression algorithm ('snappy', 'gzip', 'brotli')

        Returns:
            Path to created Parquet file
        """
        output_path = self.parquet_dir / f"{table_id}.parquet"

        try:
            df.to_parquet(
                output_path,
                engine='pyarrow',
                compression=compression,
                index=False
            )
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            logger.info(f"Exported {table_id} to Parquet: {output_path} ({file_size_mb:.2f} MB)")
            return output_path

        except Exception as e:
            logger.error(f"Failed to export {table_id} to Parquet: {e}")
            raise

    def export_to_csv(
        self,
        df: pd.DataFrame,
        table_id: str,
        encoding: str = 'utf-8-sig'
    ) -> Path:
        """
        Export dataframe to CSV format.

        Args:
            df: Input dataframe
            table_id: Table identifier
            encoding: Encoding (utf-8-sig includes BOM for Excel compatibility)

        Returns:
            Path to created CSV file
        """
        output_path = self.csv_dir / f"{table_id}.csv"

        try:
            df.to_csv(
                output_path,
                encoding=encoding,
                index=False
            )
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            logger.info(f"Exported {table_id} to CSV: {output_path} ({file_size_mb:.2f} MB)")
            return output_path

        except Exception as e:
            logger.error(f"Failed to export {table_id} to CSV: {e}")
            raise

    def export_to_json(
        self,
        df: pd.DataFrame,
        table_id: str,
        orient: str = 'records'
    ) -> Path:
        """
        Export dataframe to JSON format.

        Args:
            df: Input dataframe
            table_id: Table identifier
            orient: JSON orientation ('records', 'split', 'index', 'columns')

        Returns:
            Path to created JSON file
        """
        output_path = self.json_dir / f"{table_id}.json"

        try:
            df.to_json(
                output_path,
                orient=orient,
                force_ascii=False,
                indent=2
            )
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            logger.info(f"Exported {table_id} to JSON: {output_path} ({file_size_mb:.2f} MB)")
            return output_path

        except Exception as e:
            logger.error(f"Failed to export {table_id} to JSON: {e}")
            raise

    def export_to_sqlite(
        self,
        dfs: Dict[str, pd.DataFrame],
        database_name: str = 'taiwan_trade.db'
    ) -> Path:
        """
        Export multiple dataframes to SQLite database.

        Args:
            dfs: Dictionary mapping table_id to dataframe
            database_name: Name of SQLite database file

        Returns:
            Path to created database file
        """
        output_path = self.database_dir / database_name

        try:
            # Create or connect to database
            conn = sqlite3.connect(output_path)

            # Export each dataframe as a table
            for table_id, df in dfs.items():
                df.to_sql(
                    name=table_id,
                    con=conn,
                    if_exists='replace',
                    index=False
                )
                logger.debug(f"Added table {table_id} to database")

            conn.close()

            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            logger.info(f"Exported {len(dfs)} tables to SQLite: {output_path} ({file_size_mb:.2f} MB)")
            return output_path

        except Exception as e:
            logger.error(f"Failed to export to SQLite: {e}")
            raise

    def export_all_formats(
        self,
        df: pd.DataFrame,
        table_id: str,
        formats: Optional[List[str]] = None
    ) -> Dict[str, Path]:
        """
        Export dataframe to multiple formats.

        Args:
            df: Input dataframe
            table_id: Table identifier
            formats: List of formats to export ('parquet', 'csv', 'json')
                    None = all formats

        Returns:
            Dictionary mapping format name to output path
        """
        if formats is None:
            formats = ['parquet', 'csv', 'json']

        output_paths = {}

        if 'parquet' in formats:
            output_paths['parquet'] = self.export_to_parquet(df, table_id)

        if 'csv' in formats:
            output_paths['csv'] = self.export_to_csv(df, table_id)

        if 'json' in formats:
            output_paths['json'] = self.export_to_json(df, table_id)

        logger.info(f"Exported {table_id} to {len(output_paths)} formats")
        return output_paths


# Convenience functions
def export_to_parquet(df: pd.DataFrame, table_id: str, output_dir: Optional[Path] = None) -> Path:
    """Convenience function to export to Parquet."""
    converter = FormatConverter(output_base_dir=output_dir)
    return converter.export_to_parquet(df, table_id)


def export_to_csv(df: pd.DataFrame, table_id: str, output_dir: Optional[Path] = None) -> Path:
    """Convenience function to export to CSV."""
    converter = FormatConverter(output_base_dir=output_dir)
    return converter.export_to_csv(df, table_id)
