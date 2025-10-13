"""
DIKW 分析架構頁面

教育性頁面，展示貫穿本分析的 DIKW（資料-資訊-知識-智慧）方法論。
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from streamlit_app.config.settings import SETTINGS, DIKW_LAYERS
from streamlit_app.config.theme import COLORS, CUSTOM_CSS

st.set_page_config(page_title="DIKW 架構 - 台灣出口分析", page_icon="📈", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>📈 DIKW 分析架構</h1>
    <p style="font-size: 1.1rem; color: #6C757D;">
        理解我們的方法論：從資料到智慧
    </p>
</div>
""", unsafe_allow_html=True)

dikw_layer = st.session_state.get('dikw_layer', 'information')

# Show Data Layer information if selected
if dikw_layer == 'data':
    st.markdown("## 📊 資料層：使用的資料表")
    st.info("""
    本頁面為方法論說明頁，使用所有 16 張資料表作為示範：

    - **Table 01-16**: 完整的進出口貿易統計資料集

    這些資料表共同組成 DIKW 架構的基礎資料層。
    """)
    st.divider()

# DIKW Pyramid visualization
st.markdown("## 🔺 DIKW 金字塔")

st.markdown("""
DIKW 金字塔代表從原始資料到可行動智慧的進程。
此架構指導我們整個分析方法。
""")

# Visual pyramid representation
st.markdown("""
<div style="text-align: center; padding: 2rem;">
    <div style="width: 0; height: 0; border-left: 200px solid transparent; border-right: 200px solid transparent;
                border-bottom: 300px solid #d6272830; margin: 0 auto; position: relative;">
        <div style="position: absolute; top: 230px; left: -180px; width: 360px; text-align: center;">
            <h3 style="color: #d62728;">💡 WISDOM</h3>
            <p style="font-size: 0.9rem;">Actionable Insights</p>
        </div>
        <div style="position: absolute; top: 150px; left: -150px; width: 300px; text-align: center;">
            <h3 style="color: #2ca02c;">🧠 KNOWLEDGE</h3>
            <p style="font-size: 0.9rem;">Understanding Why</p>
        </div>
        <div style="position: absolute; top: 70px; left: -120px; width: 240px; text-align: center;">
            <h3 style="color: #ff7f0e;">📈 INFORMATION</h3>
            <p style="font-size: 0.9rem;">Processed Patterns</p>
        </div>
        <div style="position: absolute; top: -10px; left: -90px; width: 180px; text-align: center;">
            <h3 style="color: #1f77b4;">📊 DATA</h3>
            <p style="font-size: 0.9rem;">Raw Facts</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Layer-by-layer exploration
st.markdown("## 🎯 探索各層")

# Layer selector
selected_layer = st.radio(
    "選擇要探索的層級：",
    options=list(DIKW_LAYERS.keys()),
    format_func=lambda x: f"{DIKW_LAYERS[x]['icon']} {DIKW_LAYERS[x]['name']}",
    horizontal=True
)

layer_info = DIKW_LAYERS[selected_layer]

# Display selected layer
st.markdown(f"""
<div style="padding: 1.5rem; background-color: {layer_info['color']}15; border-left: 4px solid {layer_info['color']}; border-radius: 8px; margin: 1rem 0;">
    <h2 style="margin: 0; color: {layer_info['color']};">{layer_info['icon']} {layer_info['name']}</h2>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">{layer_info['description']}</p>
</div>
""", unsafe_allow_html=True)

# Layer-specific content
if selected_layer == 'data':
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📊 何謂資料？

        **定義：** 未經處理的原始事實與數據，缺乏脈絡

        **在我們的分析中：**
        - 來自台灣財政部的 16 張 Excel 表
        - 月度貿易統計
        - 各國進出口值
        - 產品類別與分類
        - 匯率與價格指數

        **特徵：**
        - 客觀測量
        - 無解讀
        - 需要處理
        - 分析基礎
        """)

    with col2:
        st.markdown("""
        ### 📋 範例：原始資料

        **Table 08 - 各國出口（範例）**

        | 年月 | 國家 | 值（百萬美元）|
        |------------|---------|---------------------|
        | 114年1-8月 | 美國 | 145,231 |
        | 114年1-8月 | 中國大陸及香港 | 128,456 |
        | 113年1-8月 | 美國 | 89,432 |
        | 113年1-8月 | 中國大陸及香港 | 135,789 |

        ➡️ *只是數字，尚無意義*
        """)

elif selected_layer == 'information':
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📈 何謂資訊？

        **定義：** 經處理並具脈絡與組織的資料

        **在我們的分析中：**
        - 成長率計算（+110%）
        - 市占率百分比（29.4%）
        - 趨勢識別（增加/減少）
        - 時間序列視覺化
        - 比較圖表

        **轉換過程：**
        1. 資料清理與標準化
        2. 衍生指標計算
        3. 組織成有意義結構
        4. 視覺化呈現模式
        """)

    with col2:
        st.markdown("""
        ### 📊 範例：資訊

        **處理後洞察：**

        - **美國出口成長：** +110% 年增率
        - **中國/香港出口變化：** -26.7% 年增率
        - **美國市占率：** 從 20% 增至 29.4%
        - **貿易順差：** $853.6 十億（2025 年 1-8 月）

        ➡️ *現在我們看到模式與趨勢*

        **視覺呈現：**
        圖表顯示美國向上趨勢，中國/香港向下
        """)

elif selected_layer == 'knowledge':
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🧠 何謂知識？

        **定義：** 理解模式為何發生及其關聯

        **在我們的分析中：**
        - 因果因素識別
        - 關係分析
        - 脈絡整合
        - 機制理解
        - 預測性洞察

        **知識發展：**
        1. 模式解讀
        2. 因果關係映射
        3. 領域專業知識應用
        4. 歷史脈絡整合
        5. 理論架構應用
        """)

    with col2:
        st.markdown("""
        ### 🔍 範例：知識

        **理解「為什麼」：**

        **為何美國出口成長？**
        - AI 革命驅動硬體需求
        - 美中科技脫鉤
        - 台灣半導體優勢
        - 友岸外包政策

        **為何中國/香港下降？**
        - 美國出口限制
        - 供應鏈重組
        - 地緣政治緊張
        - 中國國產替代

        **因果鏈：**
        ```
        AI 熱潮 → 硬體需求
             ↓
        地緣政治轉變 → 台灣優勢
             ↓
        結果：+110% 美國成長
        ```

        ➡️ *現在我們理解因果關係*
        """)

else:  # wisdom
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 💡 何謂智慧？

        **定義：** 可行動洞察與策略建議

        **在我們的分析中：**
        - 策略機會
        - 風險評估
        - 決策建議
        - 情境規劃
        - 長期影響

        **智慧應用：**
        1. 評估選項
        2. 評估權衡
        3. 考量長期影響
        4. 整合倫理考量
        5. 提供可行動指引
        """)

    with col2:
        st.markdown("""
        ### 🎯 範例：智慧

        **策略建議：**

        **把握機會：**
        - ✅ 立即最大化美國市場產能
        - ✅ 協商長期供應協議
        - ✅ 投資次世代技術（2nm/3nm）

        **減緩風險：**
        - ⚠️ 避免過度依賴美國（29.4%）
        - ⚠️ 監控 AI 泡沫可能
        - ⚠️ 多元化至東協/歐盟市場

        **策略方向：**
        - 🎯 平衡：把握當前優勢
        - 🎯 多元化：降低集中風險
        - 🎯 投資：長期定位

        ➡️ *現在我們可以做出明智決策*
        """)

st.divider()

# Practical application
st.markdown("## 🔧 儀表板中的實際應用")

st.markdown("""
貫穿整個儀表板，我們應用 DIKW 架構：
""")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 資料層",
    "📈 資訊層",
    "🧠 知識層",
    "💡 智慧層"
])

with tab1:
    st.markdown("""
    ### 資料層出現位置

    **來源：**
    - 從處理過的資料載入 Parquet 檔案
    - 來自台灣財政部的 16 張表
    - 原始進出口統計

    **用途：**
    - 所有視覺化的基礎
    - 所有計算的輸入
    - 驗證參考

    **存取：**
    - 在側邊欄切換到「資料」層
    - 檢視原始表格
    - 下載原始資料
    """)

with tab2:
    st.markdown("""
    ### 資訊層出現位置

    **頁面 1：執行摘要**
    - 關鍵指標與 KPI
    - 趨勢視覺化
    - 市占率圖表

    **所有頁面：**
    - 顯示趨勢的折線圖
    - 比較值的長條圖
    - 顯示分布的圓餅圖

    **計算：**
    - 成長率
    - 市占率
    - 年增率變化
    """)

with tab3:
    st.markdown("""
    ### 知識層出現位置

    **頁面 2：美國貿易激增**
    - 「成長驅動因素」章節
    - 因果因素分析
    - 技術/地緣政治/經濟因素

    **頁面 3：貿易轉移**
    - 「轉移驅動因素」分析
    - 因果鏈解釋
    - 關係解讀

    **整合：**
    - 多來源脈絡
    - 領域專業知識應用
    - 歷史視角
    """)

with tab4:
    st.markdown("""
    ### 智慧層出現位置

    **頁面 5：洞察與智慧**
    - 策略建議
    - 風險評估矩陣
    - 情境分析
    - 決策架構

    **貫穿全站：**
    - 「機會」標註
    - 「需監控風險」警告
    - 策略意涵
    - 行動建議
    """)

st.divider()

# Benefits of DIKW approach
st.markdown("## ✅ 為何使用 DIKW 架構？")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🎯 結構化思考

    - 系統性進程
    - 清晰方法論
    - 可重現流程
    - 減少偏見
    """)

with col2:
    st.markdown("""
    ### 📚 全面分析

    - 多層次深度
    - 從事實到行動
    - 整體視角
    - 脈絡整合
    """)

with col3:
    st.markdown("""
    ### 💼 商業價值

    - 可行動洞察
    - 清晰建議
    - 風險意識
    - 決策支援
    """)

st.success("""
**🎓 教育價值：** 此架構廣泛用於資料分析、商業智慧
與策略規劃。理解 DIKW 幫助您成為更好的分析師與決策者。
""")

st.divider()
st.caption("💡 使用側邊欄 DIKW 層級選擇器，查看各頁面如何適應不同層級")

