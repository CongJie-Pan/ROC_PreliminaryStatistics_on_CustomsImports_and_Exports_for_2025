# Taiwan Export Analysis Project - Task Implementation Plan

**Project Title**: Taiwan's ICT Export Surge and Trade Diversion Pattern Analysis
**Date Created**: 2025-10-11
**Last Updated**: 2025-10-11
**Project Owner**: AI Analysis Team
**Expected Duration**: 5-6 weeks

---

## Phase 1: Data Pipeline Development

### [ ] **Task ID**: PHASE1-TASK1
- **Task Name**: Excel Data Loader Module Development
- **Work Description**:
    - **Why**: Current Excel files have irregular structures (Chinese headers, merged cells, formatting) that prevent direct loading into Python. We need a robust parser to extract clean data from 16 Excel tables.
    - **How**:
        1. Create `src/data_processing/excel_loader.py` module
        2. Implement functions to detect header rows (skip Chinese titles)
        3. Parse merged cells using `openpyxl` library
        4. Extract metadata (table name, date, source)
        5. Handle multi-sheet Excel files
        6. Return pandas DataFrame with raw data
- **Resources Required**:
    - **Materials**:
        - 16 Excel files in `data/August2025_PreliminaryStatistics_on_CustomsImports_and_Exports/`
        - Python libraries: `pandas`, `openpyxl`, `xlrd`
    - **Personnel**:
        - 1 Python developer (data engineering focus)
    - **Reference Codes/docs**:
        - Pandas Excel I/O documentation: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
        - Openpyxl documentation: https://openpyxl.readthedocs.io/
        - `docs/TaiwanExport_Transform.md` (Section: Data Transformation Pipeline Architecture)
- **Deliverables**:
    - [ ] `src/data_processing/excel_loader.py` (< 200 lines)
    - [ ] Function: `load_excel_table(file_path: str, table_id: str) -> pd.DataFrame`
    - [ ] Unit tests in `tests/test_excel_loader.py`
    - [ ] Documentation with usage examples
- **Dependencies**:
    - None (first task in pipeline)
- **Constraints**:
    - Must handle all 16 tables with different structures
    - Must preserve data types (numeric, date, text)
    - Processing time < 5 seconds per table
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Priority tables: Table 2, 4, 8, 10, 11 (needed for Theme 1 & 2)
    - Consider creating table-specific parsers if structures vary significantly

---

### [ ] **Task ID**: PHASE1-TASK2
- **Task Name**: Data Cleaning and Standardization Module
- **Work Description**:
    - **Why**: Raw Excel data contains inconsistent formats (units like 千/百萬, percentages, missing values). We need standardized, clean data for analysis.
    - **How**:
        1. Create `src/data_processing/data_cleaner.py` module
        2. Implement column renaming: Chinese → English snake_case (出口金額 → export_value_usd_billion)
        3. Remove formatting symbols and convert to numeric
        4. Handle missing values (NaN, -, empty cells) with appropriate strategies
        5. Normalize units (convert all to billions USD, percentages to decimal)
        6. Standardize date formats (YYYY-MM)
- **Resources Required**:
    - **Materials**:
        - Output from Task PHASE1-TASK1 (raw DataFrames)
        - Column mapping dictionary (Chinese-English)
    - **Personnel**:
        - 1 Python developer (data cleaning expertise)
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (Section: Column Naming Convention)
        - Pandas data cleaning guide
        - `src/data_processing/schema_definitions.py` (to be created)
- **Deliverables**:
    - [ ] `src/data_processing/data_cleaner.py` (< 250 lines)
    - [ ] `src/data_processing/schema_definitions.py` (schema specs for all tables)
    - [ ] Function: `clean_dataframe(df: pd.DataFrame, table_id: str) -> pd.DataFrame`
    - [ ] Column mapping configuration file: `config/column_mappings.json`
    - [ ] Unit tests in `tests/test_data_cleaner.py`
- **Dependencies**:
    - PHASE1-TASK1 (Excel Loader must be completed)
- **Constraints**:
    - Must not lose data during cleaning
    - Column names must follow snake_case convention
    - All numeric values must be float64 type
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Create reusable cleaning functions for common patterns
    - Log all cleaning operations for audit trail

---

### [ ] **Task ID**: PHASE1-TASK3
- **Task Name**: Data Transformation and Enrichment Module
- **Work Description**:
    - **Why**: Beyond cleaning, we need calculated fields (growth rates, market shares, trade balances) and enriched metadata for analysis.
    - **How**:
        1. Create `src/data_processing/data_transformer.py` module
        2. Calculate derived metrics:
            - Year-over-year growth rates
            - Market share percentages
            - Trade balance (export - import)
            - Cumulative sums
        3. Add metadata fields (source_table, processing_date, data_month)
        4. Create aggregated views (e.g., quarterly summaries)
        5. Link related tables (foreign keys for joins)
- **Resources Required**:
    - **Materials**:
        - Cleaned DataFrames from PHASE1-TASK2
        - Business logic specifications from `docs/TaiwanExport_Transform.md`
    - **Personnel**:
        - 1 Data analyst/developer (business logic understanding)
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (Appendix B: Calculation Formulas)
        - Domain expert consultation for business rules
- **Deliverables**:
    - [ ] `src/data_processing/data_transformer.py` (< 300 lines)
    - [ ] Function: `transform_dataframe(df: pd.DataFrame, table_id: str) -> pd.DataFrame`
    - [ ] Business logic documentation
    - [ ] Unit tests in `tests/test_data_transformer.py`
- **Dependencies**:
    - PHASE1-TASK2 (Data Cleaner must be completed)
- **Constraints**:
    - Calculations must be accurate (tested against source data)
    - Performance: < 2 seconds per table transformation
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Ensure growth rate formula matches official calculation method
    - Add validation to check calculated values against source when available

---

### [ ] **Task ID**: PHASE1-TASK4
- **Task Name**: Parquet Format Converter and Multi-Format Export
- **Work Description**:
    - **Why**: Parquet format provides 10x faster read performance and 50% smaller file size compared to CSV, crucial for Streamlit dashboard performance.
    - **How**:
        1. Create `src/data_processing/format_converter.py` module
        2. Implement Parquet export with compression (snappy)
        3. Implement CSV export (UTF-8 with BOM for Excel compatibility)
        4. Implement JSON export (for API use)
        5. Create SQLite database with all tables (for complex queries)
        6. Add schema preservation for Parquet files
- **Resources Required**:
    - **Materials**:
        - Transformed DataFrames from PHASE1-TASK3
        - Python libraries: `pyarrow`, `fastparquet`
    - **Personnel**:
        - 1 Python developer (data engineering)
    - **Reference Codes/docs**:
        - Apache Parquet documentation
        - `docs/TaiwanExport_Transform.md` (Section: Why Parquet Format?)
- **Deliverables**:
    - [ ] `src/data_processing/format_converter.py` (< 150 lines)
    - [ ] Function: `export_to_parquet(df: pd.DataFrame, output_path: str)`
    - [ ] Function: `export_to_csv(df: pd.DataFrame, output_path: str)`
    - [ ] Function: `export_to_sqlite(dfs: Dict[str, pd.DataFrame], db_path: str)`
    - [ ] Directory structure: `data/processed/{parquet,csv,json,database}/`
    - [ ] Unit tests in `tests/test_format_converter.py`
- **Dependencies**:
    - PHASE1-TASK3 (Data Transformer must be completed)
- **Constraints**:
    - Parquet files must be readable by Streamlit
    - CSV must be Excel-compatible (UTF-8 with BOM)
    - File size reduction target: 50% vs CSV
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Use snappy compression for Parquet (good balance of speed/size)
    - Test cross-platform compatibility (Windows/Linux/Mac)

---

### [ ] **Task ID**: PHASE1-TASK5
- **Task Name**: Data Validation and Quality Assurance Module
- **Work Description**:
    - **Why**: Ensure data integrity and accuracy before using in analysis. Catch errors early to prevent incorrect insights.
    - **How**:
        1. Create `src/data_processing/data_validator.py` module
        2. Implement value range checks (min/max bounds)
        3. Implement consistency checks (trade balance = export - import)
        4. Verify sum constraints (market shares ≈ 100%)
        5. Check for missing critical data
        6. Validate against business rules
        7. Generate validation reports
- **Resources Required**:
    - **Materials**:
        - Processed data from previous tasks
        - Validation rules from `docs/TaiwanExport_Transform.md`
    - **Personnel**:
        - 1 QA analyst/developer
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (Section: Data Quality Assurance)
        - Great Expectations library (optional)
- **Deliverables**:
    - [ ] `src/data_processing/data_validator.py` (< 200 lines)
    - [ ] Validation rules configuration: `config/validation_rules.yaml`
    - [ ] Function: `validate_dataframe(df: pd.DataFrame, rules: dict) -> ValidationReport`
    - [ ] Validation report generator (HTML/JSON output)
    - [ ] Unit tests in `tests/test_data_validator.py`
- **Dependencies**:
    - PHASE1-TASK4 (Format Converter must be completed)
- **Constraints**:
    - Validation must run in < 10 seconds for all tables
    - Must catch at least 95% of data quality issues
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Consider using Great Expectations for advanced validation
    - Create alerting for critical validation failures

---

### [ ] **Task ID**: PHASE1-TASK6
- **Task Name**: Data Pipeline Orchestration and CLI Tool
- **Work Description**:
    - **Why**: Need automated pipeline to process new data each month without manual intervention. CLI tool enables easy execution and scheduling.
    - **How**:
        1. Create `src/data_processing/run_pipeline.py` orchestrator
        2. Integrate all modules (loader → cleaner → transformer → converter → validator)
        3. Add CLI interface with argparse (--month, --all, --validate-only, --format)
        4. Implement error handling and logging
        5. Create progress indicators
        6. Add rollback capability on failure
- **Resources Required**:
    - **Materials**:
        - All modules from PHASE1-TASK1 to PHASE1-TASK5
        - Python libraries: `argparse`, `logging`, `tqdm`
    - **Personnel**:
        - 1 Python developer (pipeline/DevOps focus)
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (Section: Data Update Workflow)
        - Python Click or argparse documentation
- **Deliverables**:
    - [ ] `src/data_processing/run_pipeline.py` (< 300 lines)
    - [ ] CLI usage documentation: `docs/pipeline_usage.md`
    - [ ] Logging configuration: `config/logging.yaml`
    - [ ] Example commands in README
    - [ ] Shell script for automated runs: `scripts/run_monthly_update.sh`
- **Dependencies**:
    - All PHASE1 tasks (TASK1-5) must be completed
- **Constraints**:
    - Pipeline must complete in < 2 minutes for all 16 tables
    - Must handle failures gracefully (continue on non-critical errors)
    - Logs must be detailed enough for debugging
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Add dry-run mode (--dry-run) for testing
    - Consider adding email notifications on completion/failure

---

## Phase 2: Streamlit Dashboard Restructure

### [ ] **Task ID**: PHASE2-TASK1
- **Task Name**: Multi-Page Streamlit Application Setup
- **Work Description**:
    - **Why**: Current single-file dashboard (895 lines) exceeds best practices (500 lines max). Multi-page structure improves maintainability and focus.
    - **How**:
        1. Create new directory structure: `streamlit_app/` with pages, components, utils
        2. Set up `app.py` as main entry point (< 200 lines)
        3. Configure Streamlit multi-page settings
        4. Implement navigation sidebar
        5. Set up page routing
        6. Migrate theme/styling to `config/theme.py`
- **Resources Required**:
    - **Materials**:
        - Existing `code/streamlit_analyze.py` (for reference)
        - Streamlit Multi-Page Apps documentation
    - **Personnel**:
        - 1 Frontend developer (Streamlit experience)
    - **Reference Codes/docs**:
        - Streamlit Multi-Page Apps: https://docs.streamlit.io/library/get-started/multipage-apps
        - `docs/TaiwanExport_Transform.md` (Section: New Dashboard Structure)
- **Deliverables**:
    - [ ] New directory structure: `streamlit_app/{app.py, config/, pages/, components/, utils/, data/}`
    - [ ] `streamlit_app/app.py` - Main entry point
    - [ ] `streamlit_app/config/settings.py` - App configuration
    - [ ] `streamlit_app/config/theme.py` - UI theme
    - [ ] Navigation sidebar implementation
    - [ ] `.streamlit/config.toml` - Streamlit configuration
- **Dependencies**:
    - None (can start in parallel with Phase 1)
- **Constraints**:
    - Each page file must be < 300 lines
    - Must maintain current UI/UX quality
    - Page load time < 2 seconds
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Use Streamlit's native multi-page feature (st.pages)
    - Consider adding page icons for better UX

---

### [ ] **Task ID**: PHASE2-TASK2
- **Task Name**: Parquet Data Loader and Caching System
- **Work Description**:
    - **Why**: Parquet provides 10x faster loading than CSV. Streamlit caching prevents redundant loads, improving performance.
    - **How**:
        1. Create `streamlit_app/data/loader.py` module
        2. Implement Parquet loading functions with `@st.cache_data`
        3. Add error handling for missing files
        4. Create data refresh mechanism (cache invalidation)
        5. Implement lazy loading (load only when needed)
        6. Add data versioning support
- **Resources Required**:
    - **Materials**:
        - Parquet files from `data/processed/parquet/`
        - Python libraries: `pandas`, `pyarrow`, `streamlit`
    - **Personnel**:
        - 1 Python developer (performance optimization focus)
    - **Reference Codes/docs**:
        - Streamlit caching documentation: https://docs.streamlit.io/library/advanced-features/caching
        - `docs/TaiwanExport_Transform.md` (Section: Parquet Integration)
- **Deliverables**:
    - [ ] `streamlit_app/data/loader.py` (< 150 lines)
    - [ ] Function: `load_parquet_data(table_name: str) -> pd.DataFrame` with caching
    - [ ] `streamlit_app/data/cache.py` - Cache utilities
    - [ ] Data loading performance tests
    - [ ] Documentation with usage examples
- **Dependencies**:
    - PHASE1-TASK4 (Parquet files must exist)
    - PHASE2-TASK1 (App structure must be set up)
- **Constraints**:
    - Load time < 500ms per table
    - Cache TTL: 1 hour (configurable)
    - Memory usage < 500MB for all cached data
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Test with large datasets to ensure performance
    - Add cache statistics display in sidebar (for debugging)

---

### [ ] **Task ID**: PHASE2-TASK3
- **Task Name**: Reusable Chart Components Library
- **Work Description**:
    - **Why**: Avoid code duplication. Consistent visualizations across all pages. Easier maintenance and updates.
    - **How**:
        1. Create `streamlit_app/components/charts.py` module
        2. Implement reusable Plotly chart functions:
            - Line chart (time series)
            - Bar chart (comparisons)
            - Pie chart (market share)
            - Waterfall chart (trade balance)
            - Sankey diagram (trade flows)
            - Heatmap (correlation matrix)
        3. Add customization parameters (colors, titles, annotations)
        4. Ensure responsive design (mobile-friendly)
- **Resources Required**:
    - **Materials**:
        - Plotly documentation
        - Design guidelines from `docs/TaiwanExport_Transform.md` (Appendix C: Color Scheme)
    - **Personnel**:
        - 1 Data visualization specialist
    - **Reference Codes/docs**:
        - Plotly documentation: https://plotly.com/python/
        - `code/streamlit_analyze.py` (existing charts for reference)
        - `docs/TaiwanExport_Transform.md` (Color Scheme section)
- **Deliverables**:
    - [ ] `streamlit_app/components/charts.py` (< 400 lines)
    - [ ] Functions for all chart types (8+ chart functions)
    - [ ] `streamlit_app/components/metrics.py` - KPI display components
    - [ ] `streamlit_app/components/tables.py` - Data table components
    - [ ] Chart gallery page (for testing/showcase)
    - [ ] Component documentation
- **Dependencies**:
    - PHASE2-TASK2 (Data loader must be ready)
- **Constraints**:
    - All charts must use consistent color scheme
    - Chart rendering time < 1 second
    - Must work on mobile screens (responsive)
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Use Plotly Express for simpler charts
    - Consider adding export functionality (PNG, SVG)

---

### [ ] **Task ID**: PHASE2-TASK4
- **Task Name**: Business Logic and Calculation Utilities
- **Work Description**:
    - **Why**: Separate business logic from presentation. Enable testing and reuse across pages.
    - **How**:
        1. Create `streamlit_app/utils/calculations.py` module
        2. Implement calculation functions:
            - Growth rate calculations
            - Market share calculations
            - Trade balance calculations
            - Trend analysis (moving averages, etc.)
            - Statistical summaries
        3. Add formatters in `streamlit_app/utils/formatters.py`:
            - Number formatting (billions, percentages)
            - Date formatting
            - Currency formatting
- **Resources Required**:
    - **Materials**:
        - Business logic from `docs/TaiwanExport_Transform.md` (Appendix B)
        - Existing calculations in `code/streamlit_analyze.py`
    - **Personnel**:
        - 1 Python developer
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (Calculation Formulas)
- **Deliverables**:
    - [ ] `streamlit_app/utils/calculations.py` (< 200 lines)
    - [ ] `streamlit_app/utils/formatters.py` (< 100 lines)
    - [ ] Unit tests in `tests/test_calculations.py`
    - [ ] Utility functions documentation
- **Dependencies**:
    - PHASE2-TASK2 (Data loader)
- **Constraints**:
    - All calculations must be unit tested
    - Performance: < 100ms for any calculation
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Consider using numpy for vectorized operations (faster)

---

### [ ] **Task ID**: PHASE2-TASK5
- **Task Name**: Page 1 - Executive Summary (Data + Information Layers)
- **Work Description**:
    - **Why**: First page must hook audience with key facts and trends. Represents Data and Information layers of DIKW.
    - **How**:
        1. Create `streamlit_app/pages/1_📊_Executive_Summary.py`
        2. Display hero metrics: US export growth (+110%), Trade surplus (853.6B)
        3. Interactive timeline: Monthly export trends (13 months)
        4. Market share evolution chart (US vs China/HK vs ASEAN)
        5. Product structure breakdown (ICT vs Electronics vs Others)
        6. Key findings summary
- **Resources Required**:
    - **Materials**:
        - Data from `table01_overall_trade.parquet`, `table02_export_commodities.parquet`, `table08_export_by_country.parquet`
        - Chart components from PHASE2-TASK3
    - **Personnel**:
        - 1 Frontend developer (Streamlit)
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (Page 1 specification)
        - Existing executive summary in `code/streamlit_analyze.py`
- **Deliverables**:
    - [ ] `streamlit_app/pages/1_📊_Executive_Summary.py` (< 250 lines)
    - [ ] 4 hero metrics (KPI cards)
    - [ ] Interactive timeline chart
    - [ ] Market share pie chart
    - [ ] Product structure visualization
- **Dependencies**:
    - PHASE2-TASK2 (Data loader)
    - PHASE2-TASK3 (Chart components)
    - PHASE2-TASK4 (Calculations)
- **Constraints**:
    - Page load time < 2 seconds
    - All data must be from Parquet files (no hardcoding)
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - This is the landing page - must make strong first impression

---

### [ ] **Task ID**: PHASE2-TASK6
- **Task Name**: Page 2 - US Trade Surge Analysis (Theme 1 Deep Dive)
- **Work Description**:
    - **Why**: Core analysis page for Theme 1 (ICT export surge to US). Must show detailed breakdown and comparisons.
    - **How**:
        1. Create `streamlit_app/pages/2_🇺🇸_US_Trade_Surge.py`
        2. Display ICT product detail breakdown (servers, ICs, computers)
        3. US vs China/HK side-by-side comparison charts
        4. AI-related products spotlight section
        5. Monthly trend analysis (13-month interactive chart)
        6. Export drivers analysis (what products drive growth)
- **Resources Required**:
    - **Materials**:
        - Data from `table02_export_commodities.parquet`, `table04_export_items_detail.parquet`, `table08_export_by_country.parquet`, `table11_export_to_china_hk.parquet`
        - Chart components
    - **Personnel**:
        - 1 Frontend developer + 1 Data analyst (for insights)
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (Page 2 specification, Theme 1 section)
- **Deliverables**:
    - [ ] `streamlit_app/pages/2_🇺🇸_US_Trade_Surge.py` (< 300 lines)
    - [ ] ICT product breakdown dashboard
    - [ ] US vs China/HK comparison section
    - [ ] AI products spotlight visualization
    - [ ] Monthly trend interactive chart with filters
- **Dependencies**:
    - PHASE2-TASK2, PHASE2-TASK3, PHASE2-TASK4
- **Constraints**:
    - Must clearly show the 110% growth story
    - Interactive filters must work smoothly
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - This page tells the main story - invest time in UX

---

### [ ] **Task ID**: PHASE2-TASK7
- **Task Name**: Page 3 - Trade Diversion Pattern Analysis (Theme 2 Deep Dive)
- **Work Description**:
    - **Why**: Core analysis page for Theme 2 (trade shift from China to US). Must visualize market dynamics.
    - **How**:
        1. Create `streamlit_app/pages/3_🔄_Trade_Diversion.py`
        2. Market comparison dashboard (US vs China/HK vs ASEAN vs EU vs Japan)
        3. Sankey diagram showing trade flow shifts
        4. Correlation analysis: Show inverse relationship (US ↑ when China ↓)
        5. Trade balance by country visualization
        6. Time series showing market share evolution
- **Resources Required**:
    - **Materials**:
        - Data from `table08_export_by_country.parquet`, `table09_import_by_country.parquet`, `table10_trade_balance_by_country.parquet`
        - Sankey diagram component (Plotly)
    - **Personnel**:
        - 1 Frontend developer + 1 Data visualization specialist
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (Page 3 specification, Theme 2 section)
        - Plotly Sankey diagram: https://plotly.com/python/sankey-diagram/
- **Deliverables**:
    - [ ] `streamlit_app/pages/3_🔄_Trade_Diversion.py` (< 300 lines)
    - [ ] Market comparison dashboard (5 markets)
    - [ ] Sankey diagram for trade flows
    - [ ] Correlation analysis visualization
    - [ ] Trade balance charts
- **Dependencies**:
    - PHASE2-TASK2, PHASE2-TASK3, PHASE2-TASK4
- **Constraints**:
    - Sankey diagram must clearly show diversion pattern
    - All 5 markets must be comparable on same scale
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Sankey diagram is key - test thoroughly for clarity

---

### [ ] **Task ID**: PHASE2-TASK8
- **Task Name**: Page 4 - DIKW Analysis Framework (Methodology Showcase)
- **Work Description**:
    - **Why**: Educational page to demonstrate data analysis methodology. Shows how we go from Data → Information → Knowledge → Wisdom.
    - **How**:
        1. Create `streamlit_app/pages/4_📈_DIKW_Analysis.py`
        2. Interactive DIKW pyramid visualization (click to expand each level)
        3. Layer-by-layer exploration:
            - Data layer: Show raw tables
            - Information layer: Show processed trends/charts
            - Knowledge layer: Show causal analysis
            - Wisdom layer: Show recommendations
        4. Examples from actual data for each layer
        5. Educational walkthrough with explanations
- **Resources Required**:
    - **Materials**:
        - DIKW framework documentation from `docs/TaiwanExport_Transform.md`
        - All processed data
    - **Personnel**:
        - 1 Frontend developer + 1 Educational content designer
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (DIKW Principles Application section)
        - DIKW Pyramid references
- **Deliverables**:
    - [ ] `streamlit_app/pages/4_📈_DIKW_Analysis.py` (< 250 lines)
    - [ ] Interactive DIKW pyramid component
    - [ ] Layer toggle functionality (radio buttons)
    - [ ] Examples for each DIKW layer
    - [ ] Educational explanations
- **Dependencies**:
    - PHASE2-TASK5, PHASE2-TASK6, PHASE2-TASK7 (need content from other pages)
- **Constraints**:
    - Must be educational yet engaging
    - Clear differentiation between each DIKW layer
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - This page demonstrates methodology - important for academic presentation

---

### [ ] **Task ID**: PHASE2-TASK9
- **Task Name**: Page 5 - Insights & Wisdom (Knowledge + Wisdom Layers)
- **Work Description**:
    - **Why**: Final page delivers actionable insights and recommendations. Represents Knowledge and Wisdom layers of DIKW.
    - **How**:
        1. Create `streamlit_app/pages/5_💡_Insights_Wisdom.py`
        2. Causal factor analysis section (AI boom, supply chain, geopolitics)
        3. Interactive risk assessment matrix (2D scatter plot)
        4. Policy recommendations dashboard
        5. Scenario analysis with what-if sliders (e.g., if US imports increase by X%)
        6. Sustainability assessment (short/medium/long term outlook)
- **Resources Required**:
    - **Materials**:
        - Analysis insights from `docs/TaiwanExport_Transform.md` (Knowledge and Wisdom sections)
        - Risk matrix data
    - **Personnel**:
        - 1 Frontend developer + 1 Policy analyst (for content)
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (Level 3 & 4: Knowledge and Wisdom)
        - Interactive Plotly scatter for risk matrix
- **Deliverables**:
    - [ ] `streamlit_app/pages/5_💡_Insights_Wisdom.py` (< 300 lines)
    - [ ] Causal factor analysis visualization
    - [ ] Interactive risk assessment matrix
    - [ ] Policy recommendations section
    - [ ] Scenario analysis tool (sliders + reactive charts)
    - [ ] Sustainability outlook dashboard
- **Dependencies**:
    - All previous Phase 2 tasks
- **Constraints**:
    - Recommendations must be data-driven (linked to charts)
    - Scenario analysis must update in real-time (< 500ms)
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - This is the "so what?" page - critical for demonstrating value

---

## Phase 3: DIKW Framework Integration

### [ ] **Task ID**: PHASE3-TASK1
- **Task Name**: DIKW Layer Toggle System Implementation
- **Work Description**:
    - **Why**: Allow users to switch between DIKW layers to understand depth of analysis. Educational tool for methodology demonstration.
    - **How**:
        1. Create global state management for DIKW layer selection
        2. Implement sidebar toggle (radio buttons: Data, Information, Knowledge, Wisdom)
        3. Make all pages respond to layer selection
        4. Show/hide content based on selected layer
        5. Add layer indicators on each page
- **Resources Required**:
    - **Materials**:
        - Streamlit session state
        - All page files from Phase 2
    - **Personnel**:
        - 1 Frontend developer (Streamlit state management)
    - **Reference Codes/docs**:
        - Streamlit session state: https://docs.streamlit.io/library/api-reference/session-state
        - `docs/TaiwanExport_Transform.md` (DIKW Layer Toggle section)
- **Deliverables**:
    - [ ] Global DIKW state management in `streamlit_app/app.py`
    - [ ] Sidebar DIKW layer selector
    - [ ] Layer-responsive content in all 5 pages
    - [ ] Visual indicators for current layer
- **Dependencies**:
    - PHASE2-TASK5 to TASK9 (all pages must be created)
- **Constraints**:
    - Layer switching must be instant (< 100ms)
    - State must persist during page navigation
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Test thoroughly across all pages for consistency

---

### [ ] **Task ID**: PHASE3-TASK2
- **Task Name**: Interactive Analysis Tools Development
- **Work Description**:
    - **Why**: Enable users to explore data themselves. Increases engagement and understanding.
    - **How**:
        1. Add date range selector (filter by month)
        2. Add country/region selector (multi-select)
        3. Add product category filter
        4. Implement drill-down functionality (click chart to see details)
        5. Add comparison mode (side-by-side market comparison)
        6. Create data export tool (download filtered data)
- **Resources Required**:
    - **Materials**:
        - Streamlit widgets (selectbox, multiselect, date_input)
        - Plotly click events
    - **Personnel**:
        - 1 Frontend developer (interactivity focus)
    - **Reference Codes/docs**:
        - Streamlit widgets: https://docs.streamlit.io/library/api-reference/widgets
        - Plotly events: https://plotly.com/python/click-events/
- **Deliverables**:
    - [ ] Global filter panel in sidebar
    - [ ] Drill-down functionality on all charts
    - [ ] Comparison mode toggle
    - [ ] Data export component (CSV, JSON, Excel)
    - [ ] Filter state management
- **Dependencies**:
    - PHASE3-TASK1 (DIKW layer system must be in place)
- **Constraints**:
    - Filters must update charts in < 1 second
    - Export must work for all data sizes
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Consider adding "Reset all filters" button

---

### [ ] **Task ID**: PHASE3-TASK3
- **Task Name**: Knowledge Base and Causal Analysis Components
- **Work Description**:
    - **Why**: Represent the Knowledge layer - explain WHY patterns occur. Differentiate from just showing data.
    - **How**:
        1. Create causal diagram component (flow chart)
        2. Implement factor analysis visualization (bar chart of contributing factors)
        3. Add correlation analysis tool (heatmap)
        4. Create evidence presentation format (data → conclusion links)
        5. Build knowledge cards (expandable sections with explanations)
- **Resources Required**:
    - **Materials**:
        - Causal relationships from `docs/TaiwanExport_Transform.md` (Knowledge section)
        - Plotly for network diagrams
    - **Personnel**:
        - 1 Data visualization specialist + 1 Content writer
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (Level 3: Knowledge)
        - Network diagrams with Plotly
- **Deliverables**:
    - [ ] Causal diagram component in `streamlit_app/components/`
    - [ ] Factor analysis visualization
    - [ ] Correlation heatmap tool
    - [ ] Knowledge card component (reusable)
    - [ ] Evidence linking system (data → conclusion)
- **Dependencies**:
    - PHASE2-TASK3 (Chart components)
    - PHASE3-TASK1 (DIKW layer system)
- **Constraints**:
    - Causal diagrams must be clear and not cluttered
    - Knowledge must be backed by data (verifiable)
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - This component differentiates our analysis from simple reporting

---

### [ ] **Task ID**: PHASE3-TASK4
- **Task Name**: Wisdom Dashboard and Recommendation System
- **Work Description**:
    - **Why**: Highest DIKW layer - provide actionable insights and strategic recommendations.
    - **How**:
        1. Create recommendation card component
        2. Implement risk assessment matrix visualization
        3. Build priority ranking system (sort recommendations by impact/urgency)
        4. Add scenario simulator (what-if analysis)
        5. Create sustainability outlook timeline (short/medium/long term)
        6. Implement action plan generator
- **Resources Required**:
    - **Materials**:
        - Recommendations from `docs/TaiwanExport_Transform.md` (Wisdom section)
        - Risk matrix data
    - **Personnel**:
        - 1 Frontend developer + 1 Policy/strategy analyst
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (Level 4: Wisdom, Strategic Implications)
        - Risk matrix templates
- **Deliverables**:
    - [ ] Recommendation dashboard in Page 5
    - [ ] Risk assessment matrix (interactive 2D plot)
    - [ ] Priority ranking system
    - [ ] Scenario simulator component
    - [ ] Sustainability timeline visualization
    - [ ] Downloadable action plan (PDF)
- **Dependencies**:
    - PHASE3-TASK3 (Knowledge components)
- **Constraints**:
    - Recommendations must be specific and actionable
    - Risk scores must be data-driven (not subjective)
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - This is the "value delivery" component - critical for impact

---

## Phase 4: Testing & Refinement

### [ ] **Task ID**: PHASE4-TASK1
- **Task Name**: Unit Testing for All Modules
- **Work Description**:
    - **Why**: Ensure code correctness and prevent regressions. Required for maintainability.
    - **How**:
        1. Write unit tests for all data processing modules
        2. Write unit tests for all utility functions
        3. Achieve minimum 80% code coverage
        4. Test edge cases (empty data, missing values, extreme values)
        5. Set up pytest framework
        6. Configure continuous testing
- **Resources Required**:
    - **Materials**:
        - All modules from Phase 1 and Phase 2
        - Python libraries: `pytest`, `pytest-cov`, `pytest-mock`
    - **Personnel**:
        - 1 QA engineer / Test developer
    - **Reference Codes/docs**:
        - Pytest documentation: https://docs.pytest.org/
        - Testing best practices
- **Deliverables**:
    - [ ] Complete test suite in `tests/` directory
    - [ ] Test coverage report (>80% coverage)
    - [ ] `pytest.ini` configuration
    - [ ] Test documentation: `tests/README.md`
    - [ ] CI/CD integration (GitHub Actions / GitLab CI)
- **Dependencies**:
    - PHASE1 (all data processing modules)
    - PHASE2 (all utility functions)
- **Constraints**:
    - Minimum 80% code coverage
    - All tests must pass before deployment
    - Test execution time < 30 seconds
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Use fixtures for test data
    - Mock external dependencies (file I/O)

---

### [ ] **Task ID**: PHASE4-TASK2
- **Task Name**: Integration Testing for End-to-End Pipeline
- **Work Description**:
    - **Why**: Ensure all components work together correctly. Catch integration issues before production.
    - **How**:
        1. Create integration test scenarios (Excel → Parquet → Streamlit)
        2. Test full pipeline execution
        3. Test Streamlit app loading and functionality
        4. Verify data consistency across all components
        5. Test error handling and recovery
- **Resources Required**:
    - **Materials**:
        - Complete pipeline from Phase 1
        - Complete dashboard from Phase 2-3
        - Test data (sample Excel files)
    - **Personnel**:
        - 1 QA engineer
    - **Reference Codes/docs**:
        - Integration testing best practices
        - Streamlit testing guide
- **Deliverables**:
    - [ ] Integration test suite in `tests/integration/`
    - [ ] End-to-end test scenarios
    - [ ] Streamlit app tests (using Playwright or Selenium)
    - [ ] Data consistency validation tests
    - [ ] Integration test report
- **Dependencies**:
    - PHASE4-TASK1 (unit tests must pass)
    - All previous phases complete
- **Constraints**:
    - Full pipeline test must complete in < 5 minutes
    - All integration tests must pass
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Consider using Docker for consistent test environment

---

### [ ] **Task ID**: PHASE4-TASK3
- **Task Name**: Performance Optimization and Profiling
- **Work Description**:
    - **Why**: Ensure dashboard loads quickly and handles data efficiently. User experience depends on performance.
    - **How**:
        1. Profile data loading performance (identify bottlenecks)
        2. Optimize Streamlit caching strategies
        3. Reduce memory usage (lazy loading, data sampling)
        4. Optimize Plotly chart rendering
        5. Implement progressive loading for large datasets
        6. Add performance monitoring
- **Resources Required**:
    - **Materials**:
        - Complete dashboard from Phase 2-3
        - Python profiling tools: `cProfile`, `memory_profiler`, `line_profiler`
    - **Personnel**:
        - 1 Performance engineer
    - **Reference Codes/docs**:
        - Streamlit performance tips: https://docs.streamlit.io/library/advanced-features/performance
        - Python profiling guide
- **Deliverables**:
    - [ ] Performance profiling report
    - [ ] Optimized data loading (target: < 500ms per table)
    - [ ] Optimized chart rendering (target: < 1s per chart)
    - [ ] Memory usage optimization (target: < 500MB)
    - [ ] Performance monitoring dashboard (optional)
- **Dependencies**:
    - PHASE4-TASK2 (integration tests must pass)
- **Constraints**:
    - Page load time < 2 seconds (target)
    - Memory usage < 500MB (target)
    - No degradation in functionality
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Focus on Parquet loading and caching - biggest impact areas

---

### [ ] **Task ID**: PHASE4-TASK4
- **Task Name**: User Acceptance Testing (UAT) and Feedback Collection
- **Work Description**:
    - **Why**: Validate that dashboard meets user needs and expectations. Gather feedback before final deployment.
    - **How**:
        1. Recruit 3-5 test users (classmates, instructors)
        2. Prepare UAT test plan and scenarios
        3. Conduct user testing sessions
        4. Collect feedback (surveys, interviews)
        5. Identify usability issues
        6. Prioritize and implement fixes
- **Resources Required**:
    - **Materials**:
        - Complete dashboard (production-ready)
        - UAT test plan
        - Feedback collection forms
    - **Personnel**:
        - 1 UX researcher / Product manager
        - 3-5 test users
    - **Reference Codes/docs**:
        - UAT best practices
        - Usability testing guides
- **Deliverables**:
    - [ ] UAT test plan document
    - [ ] User testing sessions (record videos if possible)
    - [ ] Feedback collection report
    - [ ] Prioritized improvement backlog
    - [ ] Implementation of critical fixes
- **Dependencies**:
    - PHASE4-TASK3 (performance optimization complete)
- **Constraints**:
    - Minimum 3 users must test
    - Must address critical issues (severity 1-2) before launch
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Consider testing with both technical and non-technical users
    - Focus on classroom presentation usability

---

## Phase 5: Documentation & Deployment

### [ ] **Task ID**: PHASE5-TASK1
- **Task Name**: User Documentation and Guide Creation
- **Work Description**:
    - **Why**: Enable users to understand and use the dashboard effectively. Essential for classroom presentation and handoff.
    - **How**:
        1. Create user guide: `docs/user_guide.md`
        2. Write feature documentation for each page
        3. Create quick start guide
        4. Add troubleshooting section
        5. Create video walkthrough (optional but recommended)
        6. Add inline help tooltips in dashboard
- **Resources Required**:
    - **Materials**:
        - Complete dashboard
        - Screenshots and screen recordings
    - **Personnel**:
        - 1 Technical writer
    - **Reference Codes/docs**:
        - Technical writing best practices
        - Streamlit documentation examples
- **Deliverables**:
    - [ ] User guide: `docs/user_guide.md`
    - [ ] Quick start guide: `docs/quick_start.md`
    - [ ] Feature documentation for each page
    - [ ] Troubleshooting guide
    - [ ] Video walkthrough (5-10 minutes, optional)
    - [ ] Inline help tooltips in dashboard
- **Dependencies**:
    - PHASE4-TASK4 (UAT complete, all features finalized)
- **Constraints**:
    - Documentation must be clear for non-technical users
    - Must include screenshots for all major features
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Consider creating a separate guide for classroom presentation tips

---

### [ ] **Task ID**: PHASE5-TASK2
- **Task Name**: API and Developer Documentation
- **Work Description**:
    - **Why**: Enable future developers to maintain and extend the system. Good documentation is critical for sustainability.
    - **How**:
        1. Create API documentation for all modules
        2. Document data pipeline architecture
        3. Create code contribution guide
        4. Document deployment procedures
        5. Add docstrings to all functions (Google style)
        6. Generate API docs with Sphinx or MkDocs
- **Resources Required**:
    - **Materials**:
        - All source code
        - Architecture diagrams
    - **Personnel**:
        - 1 Developer + 1 Technical writer
    - **Reference Codes/docs**:
        - Sphinx documentation: https://www.sphinx-doc.org/
        - Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
- **Deliverables**:
    - [ ] API documentation (auto-generated from docstrings)
    - [ ] Architecture documentation: `docs/architecture.md`
    - [ ] Code contribution guide: `CONTRIBUTING.md`
    - [ ] Deployment guide: `docs/deployment.md`
    - [ ] Docstrings for all functions (Google style)
    - [ ] Generated API docs site (Sphinx/MkDocs)
- **Dependencies**:
    - All code from Phase 1-3 must be complete
- **Constraints**:
    - All public functions must have docstrings
    - API docs must be auto-generated (not manual)
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Consider using Read the Docs for hosting documentation

---

### [ ] **Task ID**: PHASE5-TASK3
- **Task Name**: Cloud Deployment Setup
- **Work Description**:
    - **Why**: Make dashboard accessible online for classroom presentation and sharing. Enable remote access.
    - **How**:
        1. Choose deployment platform (Streamlit Cloud / AWS / Heroku)
        2. Set up deployment configuration
        3. Configure environment variables and secrets
        4. Set up CI/CD pipeline for automatic deployment
        5. Configure custom domain (optional)
        6. Set up SSL certificate (HTTPS)
        7. Monitor deployment health
- **Resources Required**:
    - **Materials**:
        - Complete dashboard code
        - Deployment platform account (Streamlit Cloud recommended)
        - CI/CD tools (GitHub Actions)
    - **Personnel**:
        - 1 DevOps engineer
    - **Reference Codes/docs**:
        - Streamlit Cloud docs: https://docs.streamlit.io/streamlit-community-cloud
        - GitHub Actions: https://docs.github.com/en/actions
- **Deliverables**:
    - [ ] Deployed dashboard (public URL)
    - [ ] Deployment configuration files (e.g., `.streamlit/config.toml`)
    - [ ] CI/CD pipeline (auto-deploy on git push)
    - [ ] Environment variables setup
    - [ ] SSL certificate (HTTPS)
    - [ ] Monitoring setup (uptime, errors)
- **Dependencies**:
    - PHASE4 (all testing complete)
    - PHASE5-TASK1, TASK2 (documentation complete)
- **Constraints**:
    - Must support HTTPS (secure connection)
    - Uptime target: 99% (monitoring required)
    - Free tier acceptable if meets requirements
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Streamlit Cloud is recommended (free tier, easy setup)
    - Keep API keys and secrets in environment variables (not in code)

---

### [ ] **Task ID**: PHASE5-TASK4
- **Task Name**: Classroom Presentation Materials Preparation
- **Work Description**:
    - **Why**: Final goal is successful classroom presentation. Need polished materials and practice.
    - **How**:
        1. Create presentation slides (15-20 slides)
        2. Prepare demo script (step-by-step)
        3. Create handout materials (summary sheet)
        4. Prepare Q&A anticipated questions
        5. Rehearse presentation (2-3 practice runs)
        6. Set up backup plan (offline demo, video recording)
- **Resources Required**:
    - **Materials**:
        - Complete dashboard (deployed)
        - Key findings from analysis
        - Presentation software (PowerPoint, Google Slides)
    - **Personnel**:
        - Presenter(s)
        - 1 Presentation coach (optional)
    - **Reference Codes/docs**:
        - `docs/TaiwanExport_Transform.md` (Section: Classroom Presentation Strategy)
        - Presentation best practices
- **Deliverables**:
    - [ ] Presentation slides (15-20 slides, PDF + source)
    - [ ] Demo script with timing: `docs/presentation_script.md`
    - [ ] Handout materials (1-page summary)
    - [ ] Q&A preparation document (anticipated questions + answers)
    - [ ] Backup materials (video recording, offline demo)
    - [ ] Rehearsal feedback report
- **Dependencies**:
    - PHASE5-TASK3 (dashboard must be deployed)
    - All documentation complete
- **Constraints**:
    - Presentation must be 15 minutes ± 2 minutes
    - Must demonstrate live dashboard (not just slides)
    - Must cover DIKW framework explicitly
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - Practice with timer - 15 minutes goes fast
    - Prepare for technical issues (have backup video/screenshots)

---

### [ ] **Task ID**: PHASE5-TASK5
- **Task Name**: Final Review and Quality Assurance
- **Work Description**:
    - **Why**: Final checkpoint before presentation. Ensure everything works perfectly.
    - **How**:
        1. Conduct final code review
        2. Verify all deliverables are complete
        3. Test deployed dashboard (production environment)
        4. Review all documentation for accuracy
        5. Verify presentation materials
        6. Create handoff checklist
        7. Archive project assets
- **Resources Required**:
    - **Materials**:
        - All project deliverables
        - Deployed dashboard
        - Documentation
    - **Personnel**:
        - 1 Project manager + 1 QA lead
    - **Reference Codes/docs**:
        - Quality assurance checklists
        - Project closeout best practices
- **Deliverables**:
    - [ ] Final code review report
    - [ ] Deliverables completion checklist (all tasks verified)
    - [ ] Production environment test report
    - [ ] Documentation accuracy verification
    - [ ] Presentation materials final review
    - [ ] Project handoff package (ZIP with all assets)
    - [ ] Lessons learned document
- **Dependencies**:
    - All previous tasks (PHASE5-TASK1 to TASK4)
- **Constraints**:
    - All tasks must be 100% complete
    - No critical bugs in production
    - All documentation must be up-to-date
- **Completion Status**: ⬜ Not Started
- **Notes**:
    - This is the final gate before presentation
    - Be thorough - last chance to catch issues

---

## Project Timeline Summary

| Phase | Duration | Tasks | Critical Path |
|-------|----------|-------|---------------|
| **Phase 1: Data Pipeline** | 2 weeks | 6 tasks | TASK1 → TASK2 → TASK3 → TASK4 → TASK5 → TASK6 |
| **Phase 2: Dashboard Restructure** | 2 weeks | 9 tasks | TASK1 → TASK2 → (TASK3,TASK4) → (TASK5-9 parallel) |
| **Phase 3: DIKW Integration** | 1 week | 4 tasks | TASK1 → (TASK2,TASK3,TASK4 parallel) |
| **Phase 4: Testing & Refinement** | 1 week | 4 tasks | TASK1 → TASK2 → TASK3 → TASK4 |
| **Phase 5: Documentation & Deployment** | 1 week | 5 tasks | (TASK1,TASK2 parallel) → TASK3 → TASK4 → TASK5 |
| **Total** | **5-6 weeks** | **28 tasks** | - |

---

## Risk Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Data quality issues | High | Medium | Comprehensive validation (PHASE1-TASK5) |
| Performance problems | High | Low | Parquet format + caching + profiling (PHASE4-TASK3) |
| Scope creep | Medium | High | Strict adherence to Theme 1 & 2 only |
| Technical failures during presentation | High | Low | Backup materials (video, offline demo) |
| Timeline delays | Medium | Medium | Parallel task execution where possible |
| Missing requirements | Medium | Medium | UAT early (PHASE4-TASK4) |

---

## Success Criteria

### Technical Success
- [ ] All 16 Excel tables successfully converted to Parquet format
- [ ] Dashboard loads in < 2 seconds
- [ ] All data visualizations render correctly
- [ ] DIKW framework clearly demonstrated
- [ ] 80%+ test coverage achieved
- [ ] Zero critical bugs in production

### Academic Success
- [ ] Clear demonstration of Theme 1 (ICT export surge)
- [ ] Clear demonstration of Theme 2 (trade diversion)
- [ ] DIKW methodology explicitly shown
- [ ] Presentation within 15-minute timeframe
- [ ] Audience engagement and understanding
- [ ] Q&A handled successfully

### Project Management Success
- [ ] All 28 tasks completed on schedule
- [ ] Documentation complete and accurate
- [ ] Deployed dashboard accessible online
- [ ] Handoff package delivered
- [ ] Lessons learned documented

---

## Appendix: Key Commands

### Data Pipeline
```bash
# Run full pipeline
python src/data_processing/run_pipeline.py --month 2025-08

# Validate data only
python src/data_processing/run_pipeline.py --validate-only

# Export specific formats
python src/data_processing/run_pipeline.py --format parquet,csv
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_excel_loader.py -v
```

### Streamlit
```bash
# Run dashboard locally
streamlit run streamlit_app/app.py

# Run with specific port
streamlit run streamlit_app/app.py --server.port 8502
```

### Deployment
```bash
# Deploy to Streamlit Cloud (via git push)
git push origin main

# Check deployment status
streamlit cloud logs
```

---

**Document End**

*This task list provides a comprehensive roadmap for implementing the Taiwan Export Analysis project with clear deliverables, dependencies, and success criteria.*
