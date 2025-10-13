"""
洞察與智慧頁面

最終頁面，提供可行動洞察、策略建議
與情境分析。代表 DIKW 架構的智慧層。
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from streamlit_app.components.charts import create_scatter_plot, create_bar_chart, create_line_chart
from streamlit_app.config.settings import SETTINGS
from streamlit_app.config.theme import COLORS, CUSTOM_CSS

st.set_page_config(page_title="洞察與智慧 - 台灣出口分析", page_icon="💡", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>💡 洞察與智慧</h1>
    <p style="font-size: 1.1rem; color: #6C757D;">
        策略建議與可行動情報
    </p>
</div>
""", unsafe_allow_html=True)

dikw_layer = st.session_state.get('dikw_layer', 'wisdom')

# Show Data Layer information if selected
if dikw_layer == 'data':
    st.markdown("## 📊 資料層：使用的資料表")
    st.info("""
    本頁面使用以下資料表進行分析：

    - **Table 01**: 進出口貿易值及年增率
    - **Table 08**: 對主要國家（地區）出口值及年增率
    - **Table 10**: 對主要國家（地區）貿易順差

    這些資料表為策略建議與風險評估提供基礎數據。
    """)
    st.divider()

# Executive Summary of Insights
st.markdown("## 📋 執行摘要")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    ### ✅ 關鍵機會

    1. **美國市場動能**
       - 創紀錄成長（+110%）呈現罕見機會
       - 建立長期合作夥伴關係
       - 接受溢價定價

    2. **技術領導地位**
       - 3nm/5nm 製程優勢
       - 關鍵 AI 基礎設施供應商
       - 2-3 年技術領先

    3. **策略定位**
       - 從地緣政治重組中獲益
       - 「可信賴夥伴」地位
       - 談判能力增強
    """)

with col2:
    st.warning("""
    ### ⚠️ 關鍵風險

    1. **市場集中**
       - 美國：29.4%（從 18.5% 上升）
       - 前兩大市場：56.7% 出口
       - 單一市場依賴風險

    2. **可持續性疑慮**
       - AI 熱潮可能非永久
       - 科技需求的週期性
       - 潛在市場修正

    3. **地緣政治波動**
       - 美中緊張關係
       - 兩岸關係
       - 政策變化風險
    """)

st.divider()

# Risk Assessment Matrix
st.markdown("## 🎯 風險評估矩陣")

st.markdown("""
互動式矩陣，以**影響**（y 軸）與**機率**（x 軸）繪製風險。
""")

# Sample risk data
risk_data = pd.DataFrame({
    'Risk': [
        'AI 泡沫破裂',
        '美國市場飽和',
        '中國市場復甦',
        '地緣政治危機',
        '技術顛覆',
        '貿易政策變化',
        '供應鏈衝擊',
        '匯率波動'
    ],
    'Probability': [45, 35, 60, 25, 30, 40, 20, 50],
    'Impact': [90, 70, 60, 95, 80, 75, 85, 45],
    'Category': [
        '市場',
        '市場',
        '市場',
        '地緣政治',
        '技術',
        '政策',
        '營運',
        '經濟'
    ]
})

fig_risk = create_scatter_plot(
    risk_data,
    x='Probability',
    y='Impact',
    title='風險評估矩陣',
    text_column='Risk',
    xlabel='機率（%）',
    ylabel='影響（1-100）',
    height=500
)

# Add quadrant lines
fig_risk.add_hline(y=50, line_dash="dash", line_color="gray", opacity=0.5)
fig_risk.add_vline(x=50, line_dash="dash", line_color="gray", opacity=0.5)

# Add quadrant labels
fig_risk.add_annotation(x=75, y=75, text="高優先級<br>（密切監控）", showarrow=False, font=dict(size=12, color="red"))
fig_risk.add_annotation(x=25, y=75, text="準備<br>應急方案", showarrow=False, font=dict(size=12, color="orange"))
fig_risk.add_annotation(x=75, y=25, text="觀察與<br>檢討", showarrow=False, font=dict(size=12, color="blue"))
fig_risk.add_annotation(x=25, y=25, text="低優先級<br>（監控）", showarrow=False, font=dict(size=12, color="green"))

st.plotly_chart(fig_risk, use_container_width=True, config={'displayModeBar': False})

st.info("""
**📊 矩陣解讀：**
- **右上（高影響 + 高機率）：** 需要立即關注與緩解策略
- **左上（高影響 + 低機率）：** 準備應急計畫
- **右下（低影響 + 高機率）：** 積極監控與管理
- **左下：** 例行監控的可接受風險
""")

st.divider()

# Strategic Recommendations
st.markdown("## 🎯 策略建議")

# Time-horizon based recommendations
tab1, tab2, tab3 = st.tabs(["🚀 立即（0-6 個月）", "📅 中期（6-18 個月）", "🔮 長期（18 個月以上）"])

with tab1:
    st.markdown("""
    ### 立即行動（0-6 個月）

    #### 1. 📈 最大化當前美國動能
    - **行動：** 增加 AI 晶片與伺服器產能 20-30%
    - **理由：** 在 AI 熱潮強勁時把握需求
    - **預期影響：** 額外 $15-20B 營收
    - **風險：** 若需求下降則過度投資

    #### 2. 🤝 確保長期承諾
    - **行動：** 與美國主要客戶協商 3-5 年供應協議
    - **理由：** 鎖定關係與定價
    - **預期影響：** 營收穩定、降低波動
    - **優先級：** 高

    #### 3. 💰 優化定價策略
    - **行動：** 對先進產品實施價值定價
    - **理由：** 在高需求期捕獲溢價
    - **預期影響：** 10-15% 利潤率改善
    - **時機：** 現在，在市場正常化前

    #### 4. 📊 增強監控
    - **行動：** 建立即時市場情報系統
    - **理由：** 需求轉變的早期警報
    - **預期影響：** 對市場變化更快反應
    - **投資：** $2-3M 用於系統與人力
    """)

with tab2:
    st.markdown("""
    ### 中期策略（6-18 個月）

    #### 1. 🌏 東協市場開發
    - **行動：** 在前 5 大東協國家建立直接銷售與支援據點
    - **目標：** 將東協份額從 15.2% 增至 18-20%
    - **投資：** $50-75M 用於區域擴張
    - **預期回報：** 3-4 年

    #### 2. 🔬 次世代技術投資
    - **行動：** 加速 2nm 製程開發與生產
    - **理由：** 維持技術領導地位
    - **投資：** $5-7B 資本支出
    - **時程：** 2026 年第 4 季投產

    #### 3. 🏭 地理多元化
    - **行動：** 擴大在美製造據點（亞利桑那州廠）
    - **理由：** 降低地緣政治風險、強化美國關係
    - **投資：** $20-25B
    - **預期完成：** 2026-2027

    #### 4. 🤝 策略合作夥伴擴張
    - **行動：** 與雲端服務供應商建立更深合作
    - **目標：** 亞馬遜 AWS、微軟 Azure、Google Cloud
    - **焦點：** 共同開發次世代 AI 硬體
    - **預期影響：** 技術路線圖一致
    """)

with tab3:
    st.markdown("""
    ### 長期願景（18 個月以上）

    #### 1. 🌍 平衡全球足跡
    - **願景：** 無單一市場超過 25% 出口
    - **目標分布：**
      - 美洲：25%
      - 亞洲（不含中國）：25%
      - 中國/香港：20%
      - 歐洲：15%
      - 其他：15%
    - **時程：** 2027-2028

    #### 2. 🚀 技術前沿領導
    - **願景：** 領導後矽技術
    - **焦點領域：**
      - 量子運算晶片
      - 光子運算
      - 神經形態晶片
    - **投資：** $10-15B 研發（2025-2030）

    #### 3. 🔄 供應鏈韌性
    - **願景：** 多區域、冗餘製造
    - **地點：** 台灣（主要）、美國、歐洲、日本
    - **能力：** 各區域可供應 30%+ 需求
    - **時程：** 2028-2030

    #### 4. 🌱 永續領導
    - **願景：** 碳中和半導體製造
    - **目標：**
      - 2027 年 50% 再生能源
      - 2030 年 100% 再生能源
      - 水回收：95%+
    - **投資：** 5 年 $8-10B
    """)

st.divider()

# Scenario Analysis
st.markdown("## 🔮 情境分析")

st.markdown("""
使用下方控制項探索不同未來情境及其影響。
""")

col1, col2 = st.columns(2)

with col1:
    us_growth_scenario = st.select_slider(
        "美國市場成長情境：",
        options=["衰退（-20%）", "緩慢（+10%）", "基準（+25%）", "強勁（+50%）", "熱潮（+100%）"],
        value="基準（+25%）"
    )

with col2:
    china_scenario = st.select_slider(
        "中國市場情境：",
        options=["進一步衰退（-30%）", "穩定（0%）", "復甦（+20%）", "強勁復甦（+40%）"],
        value="穩定（0%）"
    )

# Display scenario implications
if us_growth_scenario == "熱潮（+100%）":
    st.success("""
    ### 🚀 熱潮情境分析

    **影響：**
    - 營收潛力：+$150-200B
    - 產能限制可能
    - 供應鏈壓力
    - 維持溢價定價

    **所需行動：**
    - 緊急產能擴張
    - 確保原料供應
    - 積極招聘
    - 考慮策略性收購

    **風險：**
    - 泡沫破裂可能
    - 過度投資
    - 品質控管挑戰
    """)
elif us_growth_scenario == "衰退（-20%）":
    st.error("""
    ### 📉 衰退情境分析

    **影響：**
    - 營收衝擊：-$30-40B
    - 產能過剩風險
    - 利潤率壓力
    - 需要重組

    **所需行動：**
    - 加速多元化
    - 成本削減計畫
    - 人力調整
    - 專注效率

    **機會：**
    - 市占率整合
    - 收購困境資產
    - 技術跨越投資
    """)
else:
    st.info("""
    ### 📊 基準情境分析

    **假設：**
    - 美國成長趨於可持續水準
    - 中國市場保持穩定
    - 東協持續漸進成長

    **所需行動：**
    - 執行多元化計畫
    - 維持技術領導地位
    - 優化營運
    - 建立策略儲備

    **風險管理：**
    - 監控早期警報指標
    - 維持財務彈性
    - 多元化客戶基礎
    """)

st.divider()

# Key Takeaways
st.markdown("## 🎓 關鍵要點")

takeaway1, takeaway2, takeaway3 = st.columns(3)

with takeaway1:
    st.markdown("""
    ### 🌟 機會

    1. **空前成長**
       - +110% 美國成長罕見
       - 數十年定位

    2. **策略優勢**
       - 技術領導地位
       - 可信賴夥伴地位

    3. **市場時機**
       - AI 基礎設施熱潮
       - 供應鏈重組
    """)

with takeaway2:
    st.markdown("""
    ### ⚠️ 挑戰

    1. **集中風險**
       - 過度依賴發展中
       - 需要多元化

    2. **可持續性**
       - AI 需求可能循環
       - 長期不明確

    3. **地緣政治**
       - 波動持續
       - 政策風險仍在
    """)

with takeaway3:
    st.markdown("""
    ### 🎯 優先事項

    1. **平衡**
       - 把握當前收益
       - 為變化做準備

    2. **多元化**
       - 地理分散
       - 客戶組合

    3. **投資**
       - 技術領先
       - 區域據點
    """)

st.divider()

# Action Plan Summary
st.markdown("## 📝 建議行動計畫")

st.markdown("""
### 優先行動（依影響 × 急迫性排序）

1. **🔴 關鍵 - 立即執行**
   - 確保長期美國供應協議
   - 實施需求監控系統
   - 開始東協市場開發

2. **🟡 重要 - 儘速執行（2025 年第 4 季）**
   - 啟動 2nm 開發計畫
   - 建立策略性客戶合作夥伴關係
   - 啟動多元化策略

3. **🟢 策略性 - 稍後執行（2026+）**
   - 建立多區域製造
   - 開發後矽技術
   - 達成永續目標

### 成功指標

| 指標 | 目前 | 2026 目標 | 2028 目標 |
|--------|---------|-------------|-------------|
| 美國市占率 | 29.4% | 25-28% | 23-25% |
| 東協市占率 | 15.2% | 18-20% | 22-25% |
| 前兩大集中度 | 56.7% | <50% | <45% |
| 技術領先 | 3nm | 2nm | 1nm/後矽 |
| 永續性 | 20% 再生能源 | 50% | 100% |
""")

st.divider()

# Footer with wisdom quote
st.markdown("""
<div style="text-align: center; padding: 2rem; background-color: #f0f2f6; border-radius: 8px;">
    <h3 style="color: #262730; margin: 0 0 0.5rem 0;">💡 「預測未來最好的方法就是創造它」</h3>
    <p style="color: #6C757D; margin: 0;">本分析提供洞察，行動由您決定。</p>
</div>
""", unsafe_allow_html=True)

st.caption(f"資料來源：{SETTINGS['data_source']} | 策略分析與建議")
