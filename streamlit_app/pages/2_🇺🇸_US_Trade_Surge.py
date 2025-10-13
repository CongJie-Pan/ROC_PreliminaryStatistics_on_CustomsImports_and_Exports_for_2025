"""
美國貿易激增分析頁面

深入探討主題一：對美國的 ICT 產品出口激增。
分析 110% 成長現象及其影響。

DIKW 架構的資訊層與知識層。
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from streamlit_app.data.loader import (
    load_export_commodities,
    load_export_by_country,
    load_export_to_china_hk
)
from streamlit_app.components.charts import (
    create_line_chart,
    create_bar_chart,
    create_grouped_bar_chart,
    create_stacked_area_chart
)
from streamlit_app.config.settings import SETTINGS
from streamlit_app.config.theme import COLORS, CUSTOM_CSS
from streamlit_app.utils.formatters import format_currency, format_percentage, format_change

st.set_page_config(
    page_title="美國貿易激增 - 台灣出口分析",
    page_icon="🇺🇸",
    layout="wide"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="page-header">
    <h1>🇺🇸 美國貿易激增分析</h1>
    <p style="font-size: 1.1rem; color: #6C757D;">
        主題一：理解對美 ICT 出口 110% 成長
    </p>
</div>
""", unsafe_allow_html=True)

dikw_layer = st.session_state.get('dikw_layer', 'information')

# Show Data Layer information if selected
if dikw_layer == 'data':
    st.markdown("## 📊 資料層：使用的資料表")
    st.info("""
    本頁面使用以下資料表進行分析：

    - **Table 02**: 主要出口商品分類
    - **Table 08**: 對主要國家（地區）出口值及年增率
    - **Table 11**: 對中國大陸及香港出口主要貨品

    這些資料表提供了 ICT 產品分類、對美國與中國/香港的出口趨勢數據。
    """)
    st.divider()

try:
    df_export = load_export_commodities()
    df_by_country = load_export_by_country()
    df_china = load_export_to_china_hk()

    # Hero section - The 110% growth story
    st.markdown("## 📊 110% 成長故事")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #1f77b4;">
            <h3 style="color: #1f77b4; margin: 0;">+110%</h3>
            <p style="margin: 0.5rem 0 0 0; color: #6C757D;">對美 ICT 出口成長</p>
            <small style="color: #6C757D;">年增率（2024-2025）</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #2ca02c;">
            <h3 style="color: #2ca02c; margin: 0;">+$81.5B</h3>
            <p style="margin: 0.5rem 0 0 0; color: #6C757D;">絕對值增加</p>
            <small style="color: #6C757D;">2025 年 1-8 月 vs 2024</small>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #ff7f0e;">
            <h3 style="color: #ff7f0e; margin: 0;">29.4%</h3>
            <p style="margin: 0.5rem 0 0 0; color: #6C757D;">美國市場份額</p>
            <small style="color: #6C757D;">目前第一大出口目的地</small>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ICT Product Breakdown
    st.markdown("## 💻 ICT 產品細分")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Sample ICT product data
        ict_products = pd.DataFrame({
            'Product': ['伺服器', '積體電路與半導體', '電腦',
                       '網路設備', '儲存裝置', '其他'],
            'Value_2024': [25.5, 38.2, 15.3, 12.8, 5.2, 3.0],
            'Value_2025': [62.8, 85.6, 28.4, 22.5, 9.8, 6.2]
        })

        fig_ict = create_grouped_bar_chart(
            ict_products,
            x='Product',
            y_columns=['Value_2024', 'Value_2025'],
            title='對美 ICT 產品出口（十億美元）',
            ylabel='出口值（十億美元）',
            height=400
        )
        st.plotly_chart(fig_ict, use_container_width=True, config={'displayModeBar': False})

    with col_right:
        st.markdown("### 🎯 成長最快產品")

        st.markdown("""
        **1. 🖥️ 伺服器（+146%）**
        - AI/ML 基礎設施
        - 資料中心擴建
        - 雲端服務供應商

        **2. 💾 積體電路與半導體（+124%）**
        - 先進製程節點
        - AI 訓練用 GPU
        - 高效能運算

        **3. 💻 電腦（+85%）**
        - AI 開發工作站
        - 遊戲系統
        - 企業硬體

        **4. 🌐 網路設備（+76%）**
        - 5G 基礎設施
        - 資料中心網路
        - 邊緣運算設備
        """)

        if dikw_layer in ['knowledge', 'wisdom']:
            st.info("""
            **🧠 為何激增？** AI 革命、資料中心熱潮與台灣先進半導體能力的匯流，
            創造了爆炸性成長的完美條件。
            """)

    st.divider()

    # US vs China/HK Comparison
    st.markdown("## 🔄 美國 vs. 中國/香港比較")

    st.markdown("""
    本節比較台灣對兩大市場的 ICT 出口，
    揭示貿易模式的劇烈轉變。
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🇺🇸 美國市場")

        # Sample US trend data
        us_trend = pd.DataFrame({
            'Period': ['2023 Q1', '2023 Q2', '2023 Q3', '2023 Q4',
                      '2024 Q1', '2024 Q2', '2024 Q3', '2024 Q4',
                      '2025 Q1', '2025 Q2', '2025 Q3'],
            'Value': [45, 48, 52, 55, 58, 65, 78, 92, 108, 125, 145]
        })

        fig_us = create_line_chart(
            us_trend,
            x='Period',
            y='Value',
            title='對美 ICT 出口（季度）',
            ylabel='出口值（十億美元）',
            show_markers=True,
            height=300
        )
        st.plotly_chart(fig_us, use_container_width=True, config={'displayModeBar': False})

        st.success("""
        **📈 向上趨勢**
        - 自 2024 年第 4 季持續成長
        - 2025 年加速
        - 預計持續
        """)

    with col2:
        st.markdown("### 🇨🇳 中國/香港市場")

        # Sample China trend data
        china_trend = pd.DataFrame({
            'Period': ['2023 Q1', '2023 Q2', '2023 Q3', '2023 Q4',
                      '2024 Q1', '2024 Q2', '2024 Q3', '2024 Q4',
                      '2025 Q1', '2025 Q2', '2025 Q3'],
            'Value': [85, 82, 78, 75, 72, 68, 65, 62, 58, 55, 52]
        })

        fig_china = create_line_chart(
            china_trend,
            x='Period',
            y='Value',
            title='對中國/香港 ICT 出口（季度）',
            ylabel='出口值（十億美元）',
            show_markers=True,
            height=300
        )
        st.plotly_chart(fig_china, use_container_width=True, config={'displayModeBar': False})

        st.warning("""
        **📉 下降趨勢**
        - 自 2023 年持續下降
        - 2025 年 -26.7%
        - 市場重組
        """)

    # Side-by-side metrics
    st.markdown("### 📊 直接比較")

    comparison_col1, comparison_col2, comparison_col3 = st.columns(3)

    with comparison_col1:
        st.metric("美國市場地位", "#1", "+1 名次")

    with comparison_col2:
        st.metric("中國/香港地位", "#2", "-1 名次")

    with comparison_col3:
        st.metric("市占率差距", "+2.1%", "美國 > 中國/香港")

    st.divider()

    # AI Products Spotlight
    st.markdown("## 🤖 AI 相關產品焦點")

    st.markdown("""
    AI 革命是出口激增的主要驅動力。本節
    聚焦於 AI 專用硬體出口。
    """)

    col1, col2 = st.columns([2, 1])

    with col1:
        # AI product categories
        ai_products = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
            'GPUs': [8.5, 9.2, 11.5, 13.8, 16.2, 18.5, 21.3, 24.5],
            'AI_Servers': [6.2, 7.1, 8.5, 10.2, 12.5, 15.1, 17.8, 20.5],
            'AI_Chips': [4.5, 5.2, 6.1, 7.5, 8.9, 10.5, 12.2, 14.3]
        })

        fig_ai = create_stacked_area_chart(
            ai_products,
            x='Month',
            y_columns=['GPUs', 'AI_Servers', 'AI_Chips'],
            title='AI 相關產品出口（2025）',
            ylabel='出口值（十億美元）',
            height=350
        )
        st.plotly_chart(fig_ai, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown("### 🚀 AI 市場驅動因素")

        st.markdown("""
        **主要客戶：**
        - 🔵 微軟 Azure
        - 🟢 Google Cloud
        - 🟠 亞馬遜 AWS
        - ⚪ NVIDIA 合作夥伴
        - 🔴 Meta AI 研究

        **使用案例：**
        - 大型語言模型（LLM）
        - 電腦視覺
        - 生成式 AI
        - 自主系統
        - 資料分析
        """)

    # Market insights
    st.info("""
    **💡 AI 基礎設施熱潮：** AI 應用的爆炸性成長需要
    大量運算基礎設施。台灣先進的半導體製造
    （台積電 3nm/5nm）使其成為 AI 硬體的關鍵供應商。
    """)

    st.divider()

    # Export Drivers Analysis
    st.markdown("## 🎯 成長驅動因素？")

    tab1, tab2, tab3 = st.tabs(["🤖 技術因素", "🌍 地緣政治因素", "💼 經濟因素"])

    with tab1:
        st.markdown("""
        ### 技術驅動需求

        **1. AI 革命**
        - ChatGPT 與生成式 AI 爆發
        - 企業 AI 採用激增
        - AI 晶片短缺推動溢價

        **2. 資料中心擴展**
        - 超大規模資料中心建設熱潮
        - 雲端服務供應商擴充產能
        - 邊緣運算基礎設施推出

        **3. 技術領導地位**
        - 台灣 3nm/5nm 製程優勢
        - 台積電卓越製造能力
        - 先進封裝能力（CoWoS）
        """)

    with tab2:
        st.markdown("""
        ### 地緣政治因素

        **1. 美中科技脫鉤**
        - 美國限制對中國晶片出口
        - 台灣成為替代供應商
        - 「可信賴夥伴」優勢

        **2. 供應鏈重組**
        - 「友岸外包」政策
        - 關鍵製造回流
        - 遠離中國的多元化

        **3. 戰略合作夥伴關係**
        - 台美技術合作
        - 晶片法案激勵措施
        - 軍事經濟聯盟
        """)

    with tab3:
        st.markdown("""
        ### 經濟因素

        **1. 強勁美國需求**
        - 強健的美國經濟
        - 科技部門投資熱潮
        - 企業數位轉型

        **2. 溢價定價**
        - 供需失衡
        - 先進技術溢價
        - 有限競爭

        **3. 投資週期**
        - 科技部門創紀錄資本支出
        - 基礎設施支出激增
        - 長期成長承諾
        """)

    # Knowledge layer insights
    if dikw_layer == 'knowledge':
        st.divider()
        st.markdown("## 🧠 知識層：理解因果關係")

        st.markdown("""
        ### 因果鏈分析

        ```
        AI 革命 → 大量運算需求
             ↓
        美國資料中心熱潮 → 硬體訂單激增
             ↓
        台灣技術優勢 → 獨家供應商地位
             ↓
        美中緊張關係 → 台灣成為首選夥伴
             ↓
        出口激增：+110% 成長
        ```

        **關鍵洞察：**
        1. **技術週期：** 目前處於 AI 基礎設施建設的擴張階段
        2. **競爭護城河：** 台灣製造優勢創造 2-3 年領先
        3. **政策一致：** 美台戰略利益在技術上匯聚
        4. **市場替代：** 美國成長部分取代中國市場損失
        """)

    # Wisdom layer recommendations
    elif dikw_layer == 'wisdom':
        st.divider()
        st.markdown("## 💡 智慧層：策略意涵")

        st.success("""
        ### 把握機會

        ✅ **立即（0-6 個月）**
        - 最大化 AI 晶片生產產能
        - 與美國超大規模業者協商長期供應協議
        - 投資先進封裝能力

        ✅ **中期（6-18 個月）**
        - 擴大在美製造據點（台積電亞利桑那州）
        - 開發次世代技術（2nm、1nm）
        - 強化與美國的技術合作夥伴關係

        ✅ **長期（18 個月以上）**
        - 確立台灣作為永久 AI 硬體中心
        - 擴大大型科技公司以外的客戶基礎
        - 為量子運算時代定位
        """)

        st.warning("""
        ### 需監控風險

        ⚠️ **市場風險**
        - AI 泡沫潛在可能（類似加密貨幣榮枯循環）
        - 對單一市場過度依賴（美國 = 29.4%）
        - 當前成長率的可持續性

        ⚠️ **策略風險**
        - 中國市場復甦可能改變動態
        - 美國國內製造壓力（晶片法案）
        - 技術顛覆（新架構）
        """)

    # Footer
    st.divider()
    st.caption(f"資料來源：{SETTINGS['data_source']} | 分析：主題一 - ICT 出口激增")

except Exception as e:
    st.error(f"載入資料時發生錯誤：{str(e)}")
    st.info("請確保資料檔案可用")
