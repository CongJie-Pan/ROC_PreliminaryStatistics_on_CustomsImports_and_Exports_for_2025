# Taiwan Export Analysis Dashboard

Multi-page Streamlit application for analyzing Taiwan's ICT export surge and trade diversion patterns.

## 🎯 Overview

This dashboard provides comprehensive analysis of Taiwan's international trade using the DIKW (Data-Information-Knowledge-Wisdom) framework. It features:

- **5 Interactive Pages**: From executive summary to strategic insights
- **DIKW Layer System**: Switch between data, information, knowledge, and wisdom views
- **Advanced Visualizations**: 9+ chart types with interactive features
- **Performance Optimized**: Parquet data loading with caching (<500ms target)

## 📁 Project Structure

```
streamlit_app/
├── app.py                          # Main entry point (welcome page)
├── config/
│   ├── settings.py                 # App settings, paths, configurations
│   └── theme.py                    # Colors, styling, chart templates
├── data/
│   ├── loader.py                   # Parquet data loader with caching
│   └── cache.py                    # Cache management utilities
├── components/
│   ├── charts.py                   # 9 reusable chart types
│   ├── metrics.py                  # KPI display components
│   └── tables.py                   # Data table components
├── utils/
│   ├── calculations.py             # Business logic (25+ functions)
│   └── formatters.py               # Display formatting utilities
└── pages/
    ├── 1_📊_Executive_Summary.py   # Overview and key metrics
    ├── 2_🇺🇸_US_Trade_Surge.py     # Theme 1: ICT export growth
    ├── 3_🔄_Trade_Diversion.py      # Theme 2: Market shifts
    ├── 4_📈_DIKW_Analysis.py        # Methodology explanation
    └── 5_💡_Insights_Wisdom.py      # Strategic recommendations
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# From project root
pip install -r requirements.txt
```

Required packages:
- streamlit>=1.28.0
- pandas>=2.0.0
- plotly>=5.17.0
- pyarrow>=14.0.0
- numpy>=1.24.0
- openpyxl>=3.1.0

### 2. Ensure Data is Available

Phase 1 data processing must be completed:

```bash
# Verify parquet files exist
ls data/processed/parquet/*.parquet

# Should see 16 files (table01.parquet - table16.parquet)
```

### 3. Launch the App

```bash
# From project root
streamlit run streamlit_app/app.py

# Opens in browser at http://localhost:8501
```

## 📊 Features

### Page 1: Executive Summary
- Hero metrics dashboard (4 KPIs)
- Export trends visualization (13-month view)
- Market distribution pie chart
- Product structure analysis
- Key findings summary

### Page 2: US Trade Surge Analysis
- ICT product breakdown (+110% growth)
- US vs China/HK comparison
- AI products spotlight
- Growth driver analysis (Technology/Geopolitical/Economic factors)

### Page 3: Trade Diversion Pattern
- Five-market comparison (US, China/HK, ASEAN, EU, Japan)
- Sankey diagram for trade flows
- Correlation analysis (inverse relationship)
- Trade balance by country
- Historical market share evolution

### Page 4: DIKW Analysis Framework
- Interactive DIKW pyramid
- Layer-by-layer exploration
- Methodology explanation
- Practical application examples

### Page 5: Insights & Wisdom
- Risk assessment matrix (interactive)
- Strategic recommendations (3 time horizons)
- Scenario analysis tool
- Action plan summary

## 🎨 DIKW Layer System

Use the sidebar selector to switch between analysis depths:

- **📊 Data**: Raw statistics and measurements
- **📈 Information**: Processed trends and patterns
- **🧠 Knowledge**: Understanding causal relationships
- **💡 Wisdom**: Actionable insights and recommendations

Pages adapt their content based on the selected layer.

## 🏗️ Architecture

### Data Loading
- **Parquet Format**: 10x faster than CSV, 50% smaller
- **Caching**: `@st.cache_data` with 1-hour TTL
- **Lazy Loading**: Only load data when needed

### Component Library
**Charts** (9 types):
- Line charts, bar charts, pie charts
- Grouped bars, stacked areas
- Heatmaps, waterfall, Sankey, scatter

**Metrics**:
- KPI cards, comparison metrics
- Progress bars, trend indicators
- Stat boxes, ranking lists

**Tables**:
- Styled dataframes, paginated tables
- Comparison tables, pivot tables
- Downloadable tables (CSV/Excel/JSON)

### Business Logic
**Calculations** (25+ functions):
- Growth rates, CAGR, market share
- Trade balance, moving averages
- Correlations, volatility, trends
- Statistical summaries, outlier detection

**Formatters** (15+ functions):
- Currency, percentage, number formatting
- Date handling, large number scaling
- Table cell formatting

## ⚙️ Configuration

### Settings (`config/settings.py`)
```python
SETTINGS = {
    "app_title": "Taiwan Export Analysis Dashboard",
    "data_month": "August 2025",
    "cache_ttl": 3600,  # 1 hour
    "chart_height": 400,
    # ... more settings
}
```

### Theme (`config/theme.py`)
```python
COLORS = {
    "primary": "#FF4B4B",
    "chart_colors": [...],
    "country_colors": {...}
}
```

### Streamlit Config (`.streamlit/config.toml`)
- Theme colors and fonts
- Server settings
- Browser behavior

## 📈 Performance

**Targets:**
- Page load: <2 seconds
- Data loading: <500ms per table
- Chart rendering: <1 second
- Navigation: <500ms

**Optimization:**
- Parquet format for fast data access
- Streamlit caching for computed results
- Lazy loading of components
- Efficient data structures

## 🧪 Testing

See `TEST_CHECKLIST.md` for comprehensive testing guide.

**Quick Test:**
```bash
# Run syntax check
python -m py_compile streamlit_app/**/*.py

# Check imports (requires dependencies)
python -c "import streamlit_app.config.settings"
```

## 📝 Development Guidelines

### Adding New Pages

1. Create file: `pages/N_📊_Page_Name.py`
2. Import required modules
3. Set page config
4. Implement page logic
5. Add DIKW layer responsiveness

### Creating Components

1. Add to appropriate module (charts/metrics/tables)
2. Include docstring with parameters and examples
3. Use consistent styling from theme
4. Add type hints
5. Handle edge cases gracefully

### Data Access

```python
from streamlit_app.data.loader import load_parquet_data

# Load specific table
df = load_parquet_data('table08')

# Load with filters
df = load_parquet_data('table08',
                       columns=['year_month', 'export_value'],
                       filters={'year_month': '114年1-8月'})
```

## 🐛 Troubleshooting

**Issue: Module not found**
```bash
# Ensure you're in project root
cd /path/to/ROC_PreliminaryStatistics_on_CustomsImports_and_Exports_for_2025
python -m streamlit run streamlit_app/app.py
```

**Issue: Data not loading**
- Check parquet files exist in `data/processed/parquet/`
- Run Phase 1 pipeline if missing
- Verify file permissions

**Issue: Charts not displaying**
- Install plotly: `pip install plotly`
- Clear browser cache
- Check browser console for errors

**Issue: Slow performance**
- Enable caching (check settings.py)
- Reduce data volume for testing
- Use smaller time ranges

## 📦 Dependencies

See `requirements.txt` for full list.

**Core:**
- streamlit: Web framework
- pandas: Data manipulation
- plotly: Interactive charts
- pyarrow: Parquet file support

**Optional:**
- openpyxl: Excel export
- matplotlib: Additional visualizations

## 📄 License

This project is part of the Taiwan Export Analysis research project.

## 👥 Authors

- 潘驄杰 (Pan Chongjie)
- Claude AI Assistant

## 📞 Support

For issues or questions:
1. Check `TEST_CHECKLIST.md`
2. Review error messages in console
3. Verify all dependencies installed
4. Ensure Phase 1 data available

---

**Version:** 2.0.0
**Last Updated:** 2025-10-11
**Status:** Phase 2 Complete ✅
