#!/usr/bin/env python3
"""
Data Pipeline Orchestration and CLI Tool

This module orchestrates the complete data processing pipeline:
1. Load Excel files
2. Clean and standardize data
3. Transform and enrich data
4. Validate data quality
5. Export to multiple formats (Parquet, CSV, JSON, SQLite)

Usage:
    python src/data_processing/run_pipeline.py --month 2025-08
    python src/data_processing/run_pipeline.py --all
    python src/data_processing/run_pipeline.py --validate-only
    python src/data_processing/run_pipeline.py --format parquet,csv

Author: Claude AI & 潘驄杰
Date: 2025-10-11
"""

import argparse
import sys
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_processing.excel_loader import ExcelLoader
from data_processing.data_cleaner import DataCleaner
from data_processing.data_transformer import DataTransformer
from data_processing.format_converter import FormatConverter
from data_processing.data_validator import DataValidator, ValidationResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DataPipeline:
    """
    Orchestrates the complete data processing pipeline.
    """

    def __init__(self, validate_only: bool = False):
        """
        Initialize pipeline.

        Args:
            validate_only: If True, only validate data without exporting
        """
        self.validate_only = validate_only
        self.loader = ExcelLoader()
        self.cleaner = DataCleaner()
        self.transformer = DataTransformer()
        self.converter = FormatConverter()
        self.validator = DataValidator()

        self.results = {}
        self.validation_results = {}

    def process_table(
        self,
        table_id: str,
        export_formats: Optional[List[str]] = None
    ) -> bool:
        """
        Process a single table through the complete pipeline.

        Args:
            table_id: Table identifier (e.g., 'table08')
            export_formats: List of formats to export to

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"{'=' * 80}")
        logger.info(f"Processing {table_id.upper()}")
        logger.info(f"{'=' * 80}")

        try:
            # Step 1: Load
            logger.info(f"📥 Loading {table_id}...")
            df_raw, metadata = self.loader.load_excel_table(table_id)
            logger.info(f"   ✅ Loaded: {df_raw.shape}")

            # Step 2: Clean
            logger.info(f"🧹 Cleaning {table_id}...")
            df_clean = self.cleaner.clean_dataframe(df_raw, table_id)
            logger.info(f"   ✅ Cleaned: {df_clean.shape}")

            # Step 3: Transform
            logger.info(f"🔄 Transforming {table_id}...")
            df_transformed = self.transformer.transform_dataframe(df_clean, table_id)
            logger.info(f"   ✅ Transformed: {df_transformed.shape}")

            # Step 4: Validate
            logger.info(f"✓  Validating {table_id}...")
            validation_result = self.validator.validate_dataframe(df_transformed, table_id)
            self.validation_results[table_id] = validation_result

            if not validation_result.passed:
                logger.error(f"   ❌ Validation failed for {table_id}")
                for error in validation_result.errors:
                    logger.error(f"      - {error}")
                return False
            else:
                logger.info(f"   ✅ Validation passed")

            if validation_result.warnings:
                for warning in validation_result.warnings:
                    logger.warning(f"      ⚠️  {warning}")

            # Step 5: Export (if not validate-only mode)
            if not self.validate_only:
                logger.info(f"💾 Exporting {table_id}...")
                export_paths = self.converter.export_all_formats(
                    df_transformed,
                    table_id,
                    formats=export_formats
                )
                for format_name, path in export_paths.items():
                    logger.info(f"   ✅ {format_name.upper()}: {path}")

            # Store result
            self.results[table_id] = {
                'success': True,
                'final_shape': df_transformed.shape,
                'validation': validation_result
            }

            return True

        except Exception as e:
            logger.error(f"❌ Failed to process {table_id}: {e}", exc_info=True)
            self.results[table_id] = {
                'success': False,
                'error': str(e)
            }
            return False

    def process_multiple_tables(
        self,
        table_ids: List[str],
        export_formats: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """
        Process multiple tables.

        Args:
            table_ids: List of table identifiers
            export_formats: List of export formats

        Returns:
            Dictionary mapping table_id to success status
        """
        results = {}

        for table_id in table_ids:
            success = self.process_table(table_id, export_formats)
            results[table_id] = success

        return results

    def process_all_tables(
        self,
        export_formats: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """
        Process all 16 tables.

        Args:
            export_formats: List of export formats

        Returns:
            Dictionary mapping table_id to success status
        """
        all_table_ids = [f"table{i:02d}" for i in range(1, 17)]
        return self.process_multiple_tables(all_table_ids, export_formats)

    def generate_summary_report(self) -> str:
        """
        Generate summary report of pipeline execution.

        Returns:
            Report string
        """
        total = len(self.results)
        successful = sum(1 for r in self.results.values() if r.get('success', False))
        failed = total - successful

        report = f"""
{'=' * 80}
PIPELINE EXECUTION SUMMARY
{'=' * 80}
Total Tables Processed: {total}
Successful: {successful}
Failed: {failed}
Success Rate: {(successful/total*100 if total > 0 else 0):.1f}%

"""

        # Validation summary
        report += "VALIDATION RESULTS:\n"
        for table_id, result in self.validation_results.items():
            status = "✅ PASSED" if result.passed else "❌ FAILED"
            report += f"  {table_id}: {status}"
            if result.errors:
                report += f" ({len(result.errors)} errors)"
            if result.warnings:
                report += f" ({len(result.warnings)} warnings)"
            report += "\n"

        report += f"\n{'=' * 80}\n"

        return report


def main():
    """
    Main CLI entry point.
    """
    parser = argparse.ArgumentParser(
        description='Taiwan Trade Statistics Data Processing Pipeline'
    )

    parser.add_argument(
        '--month',
        type=str,
        help='Process specific month (e.g., 2025-08)'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Process all 16 tables'
    )

    parser.add_argument(
        '--tables',
        type=str,
        help='Comma-separated list of table IDs (e.g., table01,table08)'
    )

    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate data, do not export'
    )

    parser.add_argument(
        '--format',
        type=str,
        default='parquet,csv',
        help='Export formats (comma-separated: parquet,csv,json)'
    )

    args = parser.parse_args()

    # Parse export formats
    export_formats = args.format.split(',') if args.format else None

    # Create pipeline
    pipeline = DataPipeline(validate_only=args.validate_only)

    logger.info("Starting data processing pipeline...")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info(f"Validate only: {args.validate_only}")
    logger.info(f"Export formats: {export_formats}")

    # Execute pipeline
    try:
        if args.all:
            # Process all tables
            results = pipeline.process_all_tables(export_formats)
        elif args.tables:
            # Process specific tables
            table_ids = args.tables.split(',')
            results = pipeline.process_multiple_tables(table_ids, export_formats)
        else:
            # Default: process priority tables (table02, table08, table11)
            priority_tables = ['table02', 'table08', 'table11']
            logger.info(f"No tables specified, processing priority tables: {priority_tables}")
            results = pipeline.process_multiple_tables(priority_tables, export_formats)

        # Generate and print summary
        summary = pipeline.generate_summary_report()
        print(summary)
        logger.info("Pipeline execution completed")

        # Exit with appropriate code
        if all(results.values()):
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
