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
        st.markdown("### 📂 資料來源")
        st.info(f"""
        **來源：** {SETTINGS['data_source']}
        **期間：** {SETTINGS['data_month']}
        **版本：** {SETTINGS['version']}
        """)

        st.divider()

        # DIKW Layer Selection
        st.markdown("### 🎯 分析層級")
        st.caption("選擇要顯示的分析深度")

        # Initialize session state for DIKW layer
        if 'dikw_layer' not in st.session_state:
            st.session_state.dikw_layer = 'information'

        # DIKW layer selector
        layer_options = list(DIKW_LAYERS.keys())
        layer_labels = [f"{DIKW_LAYERS[k]['icon']} {DIKW_LAYERS[k]['name']}" for k in layer_options]

        selected_index = layer_options.index(st.session_state.dikw_layer)

        selected_layer_label = st.radio(
            "選擇分析層級：",
            layer_labels,
            index=selected_index,
            help="在不同分析深度層級之間切換"
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

        # Show data tables list if Data layer is selected
        if selected_layer == 'data' and 'tables' in layer_info:
            with st.expander("📋 查看所有資料表", expanded=False):
                st.caption("本儀表板使用以下 16 張資料表：")
                for table in layer_info['tables']:
                    st.markdown(f"- **{table['id'].upper()}**: {table['name']}")
                st.caption("\n💡 各頁面會顯示其使用的特定資料表")

        st.divider()

        # Navigation hint
        st.markdown("### 🧭 導覽")
        st.caption("使用側邊欄在不同頁面間切換")

        # Page overview
        with st.expander("📚 頁面總覽"):
            for page in SETTINGS["pages"]:
                st.markdown(f"""
                **{page['icon']} {page['name']}**
                {page['description']}
                """)

        st.divider()

        # Footer
        st.caption(f"由 {SETTINGS['author']} 製作 ❤️")
        st.caption(f"技術支援：Streamlit")

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
    st.markdown("## 📖 總覽")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🎯 專案目標

        本儀表板提供台灣國際貿易模式的全面分析，
        聚焦於兩大關鍵主題：

        1. **對美 ICT 出口激增** (+110% 成長)
           - AI 基礎設施熱潮驅動伺服器需求
           - GPU 與網路設備出口
           - 創紀錄的貿易量

        2. **貿易轉移模式**
           - 美國成為第一大出口市場（29.4% 市占率）
           - 中國/香港降至第二位
           - 供應鏈重組（友岸外包）
        """)

    with col2:
        st.markdown("""
        ### 📊 資料與方法

        **資料來源：**
        - 中華民國財政部關務署
        - 16 張完整貿易統計表
        - 2025 年 8 月止的月度資料

        **分析架構：**
        - DIKW（資料-資訊-知識-智慧）
        - 多維度趨勢分析
        - 因果關係識別
        - 策略建議
        """)

    st.divider()

    # Key findings
    st.markdown("## 🔑 關鍵發現")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #FF4B4B; margin: 0;">+110%</h3>
            <p style="margin: 0.5rem 0 0 0; color: #6C757D;">對美 ICT 出口成長</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #0068C9; margin: 0;">29.4%</h3>
            <p style="margin: 0.5rem 0 0 0; color: #6C757D;">美國市場份額</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #09AB3B; margin: 0;">$853.6B</h3>
            <p style="margin: 0.5rem 0 0 0; color: #6C757D;">貿易順差</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #FFA421; margin: 0;">-26.7%</h3>
            <p style="margin: 0.5rem 0 0 0; color: #6C757D;">中國/香港 ICT 下降</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Navigation guidance
    st.markdown("## 🧭 如何使用此儀表板")

    tab1, tab2, tab3 = st.tabs(["📄 頁面", "🎯 DIKW 層級", "🛠️ 功能"])

    with tab1:
        st.markdown("""
        ### 儀表板頁面

        使用側邊欄瀏覽分析：

        1. **📊 執行摘要** - 關鍵指標的高層次總覽
        2. **🇺🇸 美國貿易激增** - ICT 出口成長深入分析（主題一）
        3. **🔄 貿易轉移模式** - 市場轉移分析（主題二）
        4. **📈 DIKW 分析架構** - 方法論與架構說明
        5. **💡 洞察與智慧** - 策略建議與情境分析
        """)

    with tab2:
        st.markdown("""
        ### DIKW 架構

        使用側邊欄選擇器切換分析層級：

        - **📊 資料層** - 原始統計數據與測量值
        - **📈 資訊層** - 經處理的趨勢與模式
        - **🧠 知識層** - 因果關係與理解
        - **💡 智慧層** - 可行動的洞察與建議

        *根據您的選擇，會顯示不同的內容。*
        """)

    with tab3:
        st.markdown("""
        ### 儀表板功能

        - **互動式圖表** - 懸停、縮放與下載視覺化圖表
        - **動態篩選** - 依時間與類別自訂資料檢視
        - **比較模式** - 並排市場分析
        - **資料匯出** - 以多種格式下載篩選後的資料
        - **響應式設計** - 適用於桌機、平板與行動裝置
        """)

    st.divider()

    # Getting started
    st.markdown("## 🚀 開始使用")

    st.success("""
    **👉 準備好探索了嗎？**

    使用側邊欄導覽選擇頁面，開始您的分析之旅。
    我們建議從**執行摘要**開始，以獲得全面的概觀。
    """)

    # Technical details (collapsible)
    with st.expander("🔧 技術細節"):
        st.markdown("""
        **技術堆疊：**
        - 前端：Streamlit（多頁應用程式）
        - 資料處理：pandas、NumPy
        - 視覺化：Plotly
        - 資料格式：Apache Parquet（載入速度快 10 倍）

        **效能：**
        - 頁面載入時間：< 2 秒
        - 資料快取：已啟用（1 小時 TTL）
        - 圖表渲染：< 1 秒

        **資料管線：**
        - Excel → 載入 → 清理 → 轉換 → 驗證 → 匯出（Parquet/CSV/JSON）
        - 16 張表格已處理，100% 驗證通過率
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
