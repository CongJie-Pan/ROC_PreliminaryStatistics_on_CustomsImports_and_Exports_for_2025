"""
Taiwan Export Analysis Dashboard - Main Application

This is the main entry point for the multi-page Streamlit dashboard analyzing
Taiwan's ICT export surge and trade diversion patterns.

Author: 潘驄杰
Date: 2025-10-11
Version: 2.0.0
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from streamlit_app.config.settings import SETTINGS, DIKW_LAYERS
from streamlit_app.config.theme import THEME

# Page configuration
st.set_page_config(
    page_title=SETTINGS["app_title"],
    page_icon=SETTINGS["page_icon"],
    layout=SETTINGS["layout"],
    initial_sidebar_state=SETTINGS["initial_sidebar_state"],
    menu_items=SETTINGS["menu_items"]
)

# Apply custom CSS
st.markdown(THEME["custom_css"], unsafe_allow_html=True)

def render_sidebar():
    """
    Render the sidebar with navigation and DIKW layer selector.
    """
    with st.sidebar:
        # Application logo and title
        st.title(f"{SETTINGS['page_icon']} {SETTINGS['app_title']}")
        st.caption(SETTINGS["app_subtitle"])

        st.divider()

        # Data source information
        st.markdown("### 📂 Data Source")
        st.info(f"""
        **Source:** {SETTINGS['data_source']}
        **Period:** {SETTINGS['data_month']}
        **Version:** {SETTINGS['version']}
        """)

        st.divider()

        # DIKW Layer Selection
        st.markdown("### 🎯 Analysis Layer")
        st.caption("Select the depth of analysis to display")

        # Initialize session state for DIKW layer
        if 'dikw_layer' not in st.session_state:
            st.session_state.dikw_layer = 'information'

        # DIKW layer selector
        layer_options = list(DIKW_LAYERS.keys())
        layer_labels = [f"{DIKW_LAYERS[k]['icon']} {DIKW_LAYERS[k]['name']}" for k in layer_options]

        selected_index = layer_options.index(st.session_state.dikw_layer)

        selected_layer_label = st.radio(
            "Choose analysis layer:",
            layer_labels,
            index=selected_index,
            help="Switch between different levels of analysis depth"
        )

        # Update session state
        selected_layer = layer_options[layer_labels.index(selected_layer_label)]
        st.session_state.dikw_layer = selected_layer

        # Display layer description
        layer_info = DIKW_LAYERS[selected_layer]
        st.markdown(f"""
        <div style="padding: 0.5rem; background-color: {layer_info['color']}15; border-left: 3px solid {layer_info['color']}; border-radius: 4px; margin-top: 0.5rem;">
            <strong>{layer_info['icon']} {layer_info['name']}</strong><br>
            <small>{layer_info['description']}</small>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Navigation hint
        st.markdown("### 🧭 Navigation")
        st.caption("Use the sidebar to navigate between pages")

        # Page overview
        with st.expander("📚 Page Overview"):
            for page in SETTINGS["pages"]:
                st.markdown(f"""
                **{page['icon']} {page['name']}**
                {page['description']}
                """)

        st.divider()

        # Footer
        st.caption(f"Made with ❤️ by {SETTINGS['author']}")
        st.caption(f"Powered by Streamlit")

def render_welcome_page():
    """
    Render the welcome/landing page content.
    """
    # Header
    st.markdown(f"""
    <div class="page-header">
        <h1>{SETTINGS['page_icon']} {SETTINGS['app_title']}</h1>
        <p style="font-size: 1.2rem; color: #6C757D;">{SETTINGS['app_subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Overview section
    st.markdown("## 📖 Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🎯 Project Objectives

        This dashboard provides comprehensive analysis of Taiwan's international trade patterns,
        focusing on two key themes:

        1. **ICT Export Surge to US** (+110% growth)
           - AI infrastructure boom driving server demand
           - GPU and networking equipment exports
           - Record-breaking trade volumes

        2. **Trade Diversion Pattern**
           - US becomes #1 export market (29.4% share)
           - China/HK declines to #2 position
           - Supply chain reorganization (friend-shoring)
        """)

    with col2:
        st.markdown("""
        ### 📊 Data & Methodology

        **Data Source:**
        - ROC Ministry of Finance
        - 16 comprehensive trade tables
        - Monthly data through August 2025

        **Analysis Framework:**
        - DIKW (Data-Information-Knowledge-Wisdom)
        - Multi-dimensional trend analysis
        - Causal factor identification
        - Strategic recommendations
        """)

    st.divider()

    # Key findings
    st.markdown("## 🔑 Key Findings")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #FF4B4B; margin: 0;">+110%</h3>
            <p style="margin: 0.5rem 0 0 0; color: #6C757D;">ICT Export Growth to US</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #0068C9; margin: 0;">29.4%</h3>
            <p style="margin: 0.5rem 0 0 0; color: #6C757D;">US Market Share</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #09AB3B; margin: 0;">$853.6B</h3>
            <p style="margin: 0.5rem 0 0 0; color: #6C757D;">Trade Surplus</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #FFA421; margin: 0;">-26.7%</h3>
            <p style="margin: 0.5rem 0 0 0; color: #6C757D;">China/HK ICT Decline</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Navigation guidance
    st.markdown("## 🧭 How to Use This Dashboard")

    tab1, tab2, tab3 = st.tabs(["📄 Pages", "🎯 DIKW Layers", "🛠️ Features"])

    with tab1:
        st.markdown("""
        ### Dashboard Pages

        Navigate through the analysis using the sidebar:

        1. **📊 Executive Summary** - High-level overview with key metrics
        2. **🇺🇸 US Trade Surge** - Deep dive into ICT export growth (Theme 1)
        3. **🔄 Trade Diversion** - Market shift analysis (Theme 2)
        4. **📈 DIKW Analysis** - Methodology and framework explanation
        5. **💡 Insights & Wisdom** - Strategic recommendations and scenario analysis
        """)

    with tab2:
        st.markdown("""
        ### DIKW Framework

        Switch between analysis layers using the sidebar selector:

        - **📊 Data** - Raw statistics and measurements
        - **📈 Information** - Processed trends and patterns
        - **🧠 Knowledge** - Causal relationships and understanding
        - **💡 Wisdom** - Actionable insights and recommendations

        *Different content will be displayed based on your selection.*
        """)

    with tab3:
        st.markdown("""
        ### Dashboard Features

        - **Interactive Charts** - Hover, zoom, and download visualizations
        - **Dynamic Filters** - Customize data views by time period and category
        - **Comparison Mode** - Side-by-side market analysis
        - **Data Export** - Download filtered data in multiple formats
        - **Responsive Design** - Works on desktop, tablet, and mobile devices
        """)

    st.divider()

    # Getting started
    st.markdown("## 🚀 Getting Started")

    st.success("""
    **👉 Ready to explore?**

    Use the sidebar navigation to select a page and begin your analysis journey.
    We recommend starting with the **Executive Summary** for a comprehensive overview.
    """)

    # Technical details (collapsible)
    with st.expander("🔧 Technical Details"):
        st.markdown("""
        **Technology Stack:**
        - Frontend: Streamlit (Multi-Page App)
        - Data Processing: pandas, NumPy
        - Visualization: Plotly
        - Data Format: Apache Parquet (10x faster loading)

        **Performance:**
        - Page load time: <2 seconds
        - Data caching: Enabled (1-hour TTL)
        - Chart rendering: <1 second

        **Data Pipeline:**
        - Excel → Load → Clean → Transform → Validate → Export (Parquet/CSV/JSON)
        - 16 tables processed with 100% validation pass rate
        """)

def main():
    """
    Main application entry point.
    """
    # Render sidebar
    render_sidebar()

    # Render welcome page
    render_welcome_page()

if __name__ == "__main__":
    main()
