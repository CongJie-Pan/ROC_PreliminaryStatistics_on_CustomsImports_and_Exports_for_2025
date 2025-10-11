# Taiwan Customs Import/Export Trade Statistics Analysis

**Project:** Taiwan's ICT Export Surge and Trade Diversion Pattern Analysis
**Data Source:** ROC Ministry of Finance - Preliminary Statistics on Customs Imports and Exports (August 2025)
**Status:** Phase 1 Complete ✅

---

## Project Overview

This project analyzes Taiwan's customs import/export trade statistics, focusing on:
1. **ICT Product Export Surge to US** (+110% growth)
2. **Trade Diversion Patterns** (China/HK → US market shift)
3. **DIKW Framework Application** (Data → Information → Knowledge → Wisdom)

The analysis combines Theme 1 (ICT export surge) and Theme 2 (trade diversion) for a comprehensive data-driven narrative suitable for classroom presentation.

---

## Phase 1: Data Pipeline Development ✅ COMPLETED

**Status:** 100% Success Rate (16/16 tables processed)

### What's Built

Complete data processing pipeline with 6 core modules:

1. **Excel Data Loader** - Handles Chinese headers, merged cells, and irregular structures
2. **Data Cleaner** - Column renaming, sub-header removal, data type standardization
3. **Data Transformer** - Growth calculations, metadata enrichment
4. **Format Converter** - Export to Parquet (fast), CSV (Excel-compatible), JSON (API-ready)
5. **Data Validator** - Comprehensive validation with reporting
6. **Pipeline Orchestrator** - CLI tool for end-to-end processing

### Output Files

**48 files generated** (16 tables × 3 formats):
- `data/processed/parquet/` - 16 Parquet files (268K) - Optimized for Streamlit
- `data/processed/csv/` - 16 CSV files (80K) - Excel-compatible
- `data/processed/json/` - 16 JSON files (136K) - API-ready

---

## Quick Start

### Prerequisites

- Python 3.8+
- pandas, openpyxl, pyarrow

### Installation

```bash
# Clone repository
git clone <repository-url>
cd ROC_PreliminaryStatistics_on_CustomsImports_and_Exports_for_2025

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Process All Tables

```bash
python src/data_processing/run_pipeline.py --all --format parquet,csv,json
```

#### Process Specific Tables

```bash
# Process priority tables (table02, table08, table11)
python src/data_processing/run_pipeline.py --tables table02,table08,table11 --format parquet

# Process single table
python src/data_processing/run_pipeline.py --tables table08 --format csv
```

#### Validation Only (No Export)

```bash
python src/data_processing/run_pipeline.py --all --validate-only
```

#### Available Options

- `--all` - Process all 16 tables
- `--tables <table_ids>` - Process specific tables (comma-separated)
- `--format <formats>` - Export formats: parquet, csv, json (comma-separated)
- `--validate-only` - Only validate, don't export
- `--month <YYYY-MM>` - Future: specify data month

---

## Data Tables

| Table | Description | Rows | Status |
|-------|-------------|------|--------|
| table01 | Import and Export Trade Values | 11 | ✅ |
| table02 | Classification of Major Export Commodities | 11 | ✅ |
| table03 | Classification of Major Imported Goods | 11 | ✅ |
| table04 | Major Export Commodities (Detailed) | 11 | ✅ |
| table05 | Major Imported Commodities | 11 | ✅ |
| table06 | Export Trade Structure | 11 | ✅ |
| table07 | Import Trade Structure | 11 | ✅ |
| table08 | Export Value and Growth Rate by Country/Region | 11 | ✅ |
| table09 | Import Value and Growth Rate by Country/Region | 11 | ✅ |
| table10 | Trade Surplus by Major Countries/Regions | 11 | ✅ |
| table11 | Major Export Commodities to China/Hong Kong | 11 | ✅ |
| table12 | Export to 18 New Southbound Policy Countries | 11 | ✅ |
| table13 | Seasonally Adjusted Trade Values | 2 | ✅ |
| table14 | Import/Export Values for Major Countries (Comprehensive) | 10 | ✅ |
| table15 | Import and Export Price-Related Indicators | 10 | ✅ |
| table16 | Exchange Rates of Major Currencies | 11 | ✅ |

**Total:** 163 rows across 16 tables

---

## Project Structure

```
.
├── README.md
├── CLAUDE.md                  # Project guidelines for Claude Code
├── requirements.txt           # Python dependencies
├── config/
│   └── column_mappings.json   # Chinese-English column mappings
├── data/
│   ├── August2025_PreliminaryStatistics_on_CustomsImports_and_Exports/
│   │   └── [16 Excel files]   # Raw data
│   └── processed/
│       ├── parquet/           # Parquet exports (fast reading)
│       ├── csv/               # CSV exports (Excel-compatible)
│       └── json/              # JSON exports (API-ready)
├── docs/
│   ├── TASK.md                # Implementation plan (28 tasks, 5 phases)
│   ├── TASK_zh-TW.md          # Implementation plan (Traditional Chinese)
│   ├── TaiwanExport_Transform_zh-TW.md  # Analysis framework
│   ├── Worklog.md             # Project worklog
│   └── PHASE1_COMPLETION_REPORT.md      # Phase 1 completion report
├── src/
│   └── data_processing/
│       ├── __init__.py
│       ├── excel_loader.py         # Excel data loading
│       ├── data_cleaner.py         # Data cleaning & standardization
│       ├── data_transformer.py     # Data transformation & enrichment
│       ├── format_converter.py     # Multi-format export
│       ├── data_validator.py       # Data validation & QA
│       ├── schema_definitions.py   # Table schemas
│       └── run_pipeline.py         # Pipeline orchestration (CLI)
└── code/
    └── streamlit_analyze.py   # Original Streamlit dashboard (to be restructured in Phase 2)
```

---

## DIKW Framework

This project applies the DIKW (Data-Information-Knowledge-Wisdom) framework:

### 📊 Data Layer
Raw statistics from 16 Excel tables (Taiwan Ministry of Finance)

### 📈 Information Layer
Processed trends and patterns:
- US export growth: +110% (ICT products)
- China/HK export decline: -26.7%
- US becomes #1 export market (29.4% share)

### 🧠 Knowledge Layer
Understanding WHY patterns occur:
- AI infrastructure boom driving server demand
- Supply chain reorganization (friend-shoring)
- Geopolitical shifts affecting trade routes

### 💡 Wisdom Layer
Actionable insights and recommendations:
- Market diversification strategies
- Risk assessment (trade imbalance, concentration)
- Policy recommendations for sustainability

---

## Key Findings

### Theme 1: ICT Export Surge to US
- **+110% growth** in ICT product exports to US (August 2025)
- **+81.5 billion USD** increase in absolute value
- Driven by AI infrastructure boom (servers, GPUs, networking equipment)

### Theme 2: Trade Diversion Pattern
- **US becomes #1** export market (29.4% share, historically ~20%)
- **China/HK drops to #2** (27.3% share, historically #1)
- **-26.7% decline** in ICT exports to China/HK
- Clear substitution effect: US ↑ when China ↓

### Strategic Implications
- **Opportunity:** Leverage current advantage for Taiwan-US trade agreement
- **Risk:** Over-dependence on single market (29.4% concentration)
- **Sustainability:** Short-term AI boom may not be sustainable long-term

---

## Next Steps

### Phase 2: Streamlit Dashboard Restructure (9 tasks, 2 weeks)

**Goal:** Create multi-page interactive dashboard with DIKW framework visualization

**Tasks:**
1. Multi-page Streamlit application setup
2. Parquet data loader with caching (10x performance boost)
3. Reusable chart component library
4. Business logic and calculation utilities
5. Page 1: Executive Summary (Data + Information)
6. Page 2: US Trade Surge Analysis (Theme 1)
7. Page 3: Trade Diversion Pattern (Theme 2)
8. Page 4: DIKW Analysis Framework (Methodology)
9. Page 5: Insights & Wisdom (Recommendations)

---

## Documentation

- **[TASK.md](docs/TASK.md)** - Complete implementation plan (28 tasks, 5 phases)
- **[TASK_zh-TW.md](docs/TASK_zh-TW.md)** - Implementation plan (Traditional Chinese)
- **[TaiwanExport_Transform_zh-TW.md](docs/TaiwanExport_Transform_zh-TW.md)** - Analysis framework (Traditional Chinese)
- **[PHASE1_COMPLETION_REPORT.md](docs/PHASE1_COMPLETION_REPORT.md)** - Phase 1 completion report
- **[Worklog.md](docs/Worklog.md)** - Project worklog

---

## Authors

- **潘驄杰** - Project Lead
- **Claude AI** - Development Assistant

---

## License

This project is for educational and research purposes.

---

## Data Source

**Ministry of Finance, Republic of China (Taiwan)**
Preliminary Statistics on Customs Imports and Exports - August 2025

---

**Last Updated:** 2025-10-11
**Phase 1 Status:** ✅ COMPLETED (100% success rate)
