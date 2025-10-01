# -*- coding: utf-8 -*-
"""
中華民國114年受美國關稅調整影響之海關進出口貿易統計趨勢分析
互動式 Streamlit 儀表板

數據來源: 財政部114年8月海關進出口貿易初步統計
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==================== 頁面配置 ====================
st.set_page_config(
    page_title="美國關稅影響分析",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定義樣式 ====================
st.markdown("""
<style>
    .big-metric {
        font-size: 2.5rem !important;
        font-weight: bold;
        color: #1f77b4;
    }
    .positive-change {
        color: #2ca02c;
    }
    .negative-change {
        color: #d62728;
    }
    .section-header {
        background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%);
        color: white;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 數據準備 ====================

# 整體貿易數據 (114年1-8月累計)
overall_trade_data = {
    '項目': ['總出口', '總進口', '總順差'],
    '金額(億美元)': [3984.3, 3115.4, 868.9],
    '年增率(%)': [29.2, 21.7, 65.6]
}

# 對美貿易數據
us_trade_summary = {
    '8月單月': {
        '出口': 196.3,
        '進口': 39.7,
        '順差': 156.6,
        '出口年增率': 65.2,
        '進口年增率': 21.3
    },
    '1-8月累計': {
        '出口': 1171.7,
        '進口': 318.1,
        '順差': 853.6,
        '出口年增率': 55.3,
        '進口年增率': -4.1,
        '出口占比': 29.4
    }
}

# 月度出口數據 (113年8月-114年8月)
monthly_export_data = pd.DataFrame({
    '月份': ['113/08', '113/09', '113/10', '113/11', '113/12',
            '114/01', '114/02', '114/03', '114/04', '114/05',
            '114/06', '114/07', '114/08'],
    '出口金額': [436.3, 405.6, 412.9, 410.8, 435.7,
                387.1, 413.0, 495.5, 486.4, 517.4,
                533.3, 566.8, 584.9],
    '年增率': [16.8, 4.5, 8.4, 9.7, 9.1,
              4.4, 31.4, 18.5, 29.9, 38.6,
              33.7, 42.0, 34.1]
})

# 月度進口數據
monthly_import_data = pd.DataFrame({
    '月份': ['114/01', '114/02', '114/03', '114/04',
            '114/05', '114/06', '114/07', '114/08'],
    '進口金額': [286.4, 346.7, 426.2, 412.5,
                391.2, 412.5, 423.4, 416.6],
    '年增率': [-17.2, 47.5, 28.8, 32.3,
              25.0, 17.2, 20.8, 29.7]
})

# 商品結構數據 (1-8月累計)
commodity_structure = pd.DataFrame({
    '商品類別': ['資通與視聽產品', '電子零組件', '基本金屬及其製品',
               '機械', '電機產品', '化學品', '塑橡膠及其製品', '其他'],
    '金額(億美元)': [1495.0, 1374.97, 191.36, 167.17, 97.98, 123.83, 123.16, 411.83],
    '占比(%)': [37.5, 34.5, 4.8, 4.2, 2.5, 3.1, 3.1, 10.3],
    '年增率(%)': [69.0, 25.4, 0.4, 5.1, 11.7, 0.2, -6.7, 8.5]
})

# 主要市場出口數據 (1-8月累計)
market_export_data = pd.DataFrame({
    '市場': ['美國', '中國大陸與香港', '東協', '歐洲', '日本', '南韓', '其他'],
    '金額(億美元)': [1171.7, 1087.3, 778.3, 245.9, 192.5, 163.54, 345.16],
    '占比(%)': [29.4, 27.3, 19.5, 6.2, 4.8, 4.1, 8.7],
    '年增率(%)': [55.3, 14.5, 38.2, -6.7, 13.3, 25.8, 18.5],
    '年增金額(億美元)': [417.4, 137.9, 215.2, -17.7, 22.6, 33.54, 54.4]
})

# 對美出口商品結構 (8月單月變化)
us_export_commodities = pd.DataFrame({
    '商品': ['資通與視聽產品', '電機產品', '運輸工具', '基本金屬及其製品', '化學品'],
    '變化(億美元)': [81.5, 0.5, -1.1, -1.0, -0.8],
    '年增率(%)': [110.0, 9.2, -28.7, -15.5, -38.7]
})

# 對美 vs 對陸港資通產品對比 (8月)
us_vs_china_comparison = pd.DataFrame({
    '市場': ['對美國', '對中國大陸與香港'],
    '資通產品變化(億美元)': [81.5, -5.7],
    '資通產品年增率(%)': [110.0, -26.7]
})

# 進口來源數據 (1-8月累計)
import_source_data = pd.DataFrame({
    '來源': ['中國大陸與香港', '南韓', '東協', '日本', '歐洲', '美國', '其他'],
    '金額(億美元)': [596.33, 399.20, 401.35, 356.10, 330.90, 318.08, 713.44],
    '占比(%)': [19.1, 12.8, 12.9, 11.4, 10.6, 10.2, 22.9],
    '年增率(%)': [15.3, 55.2, 24.3, 19.2, 10.4, -4.1, 20.5]
})

# AI相關商品數據 (8月)
ai_related_products = pd.DataFrame({
    '產品': ['電腦及其附屬單元', '電腦之零附件', '積體電路'],
    '變化(億美元)': [85.7, 14.6, 52.3],
    '年增率(%)': [100.0, 100.0, 37.4]
})

# 風險矩陣數據
risk_matrix_data = pd.DataFrame({
    '風險項目': ['貿易失衡', '產業集中', '傳統產業衰退', '關稅政策變化',
              '地緣政治', '市場集中', 'AI需求波動', '全球經濟放緩',
              '匯率波動', '供應鏈過剩'],
    '影響程度': [9, 9, 7, 8, 7, 7, 6, 7, 6, 5],
    '發生機率': [8, 9, 9, 7, 6, 8, 5, 6, 7, 5],
    '風險類別': ['政策', '產業', '產業', '政策', '政策', '產業', '產業', '經濟', '經濟', '經濟']
})

risk_matrix_data['風險值'] = risk_matrix_data['影響程度'] * risk_matrix_data['發生機率']

# ==================== 側邊欄 ====================
with st.sidebar:
    st.title("📊 導航選單")

    page = st.radio(
        "選擇分析模塊",
        ["🏠 執行摘要", "🇺🇸 對美貿易分析", "📦 商品結構分析",
         "🌏 市場比較分析", "⚠️ 風險評估", "📈 互動式探索"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### 📅 數據期間")
    st.info("**分析期間:** 114年1-8月  \n**發布日期:** 114年9月9日  \n**數據來源:** 財政部")

    st.divider()
    st.caption("© 2025 台灣貿易分析系統")

# ==================== 主要內容 ====================

# 🏠 執行摘要
if page == "🏠 執行摘要":
    st.title("中華民國114年受美國關稅調整影響之海關進出口貿易統計趨勢分析")
    st.markdown("### Interactive Dashboard")

    st.divider()

    st.markdown('<div class="section-header"><h2>核心發現</h2></div>', unsafe_allow_html=True)

    # 關鍵指標卡片
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="對美出口 (1-8月)",
            value=f"${us_trade_summary['1-8月累計']['出口']:.1f}B",
            delta=f"+{us_trade_summary['1-8月累計']['出口年增率']:.1f}%"
        )

    with col2:
        st.metric(
            label="對美順差 (1-8月)",
            value=f"${us_trade_summary['1-8月累計']['順差']:.1f}B",
            delta="創歷史新高"
        )

    with col3:
        st.metric(
            label="市場占比",
            value=f"{us_trade_summary['1-8月累計']['出口占比']:.1f}%",
            delta="35年新高"
        )

    with col4:
        st.metric(
            label="市場地位",
            value="第1大",
            delta="超越中國大陸"
        )

    st.divider()

    # 重要發現
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("### 正面發展")
        st.markdown("""
        - **對美出口創新高**: 8月達196.3億美元(+65.2%)
        - **美國成為第一大市場**: 占比29.4%,超越中國大陸
        - **科技產品主導**: 資通產品+69.0%,電子零組件+25.4%
        - **貿易轉移效應明顯**: 資通產品從對陸港轉向對美
        - **AI驅動成長**: 伺服器、AI晶片需求強勁
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("### 潛在風險")
        st.markdown("""
        - **貿易失衡**: 對美順差853.6億美元,可能引發壓力
        - **市場集中度高**: 對美出口占比快速提升至29.4%
        - **產業集中度高**: 科技產品占出口72.0%
        - **傳統產業衰退**: 塑橡膠-6.7%,紡織-6.3%
        - **自美進口下降**: 1-8月減4.1%,雙邊失衡擴大
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # 整體貿易概況
    st.markdown('<div class="section-header"><h2>整體貿易概況 (114年1-8月)</h2></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        overall_df = pd.DataFrame(overall_trade_data)
        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='金額(億美元)',
            x=overall_df['項目'],
            y=overall_df['金額(億美元)'],
            text=overall_df['金額(億美元)'].apply(lambda x: f'{x:.1f}'),
            textposition='outside',
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c']
        ))

        fig.update_layout(
            title='整體進出口貿易額',
            xaxis_title='',
            yaxis_title='金額 (億美元)',
            height=400,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 年增率表現")
        for idx, row in overall_df.iterrows():
            st.metric(
                label=row['項目'],
                value=f"{row['金額(億美元)']:.1f}億美元",
                delta=f"{row['年增率(%)']:+.1f}%"
            )

    st.divider()

    # 關鍵結論
    st.markdown('<div class="section-header"><h2>關鍵結論</h2></div>', unsafe_allow_html=True)

    st.markdown("""
    #### 1. 美國正式成為台灣第一大出口市場
    114年1-8月對美出口達**1,171.7億美元**,占總出口**29.4%**,創近35年新高,**首次超越中國大陸**(27.3%)。

    #### 2. 科技產品主導成長,AI是核心驅動力
    資通與視聽產品年增**69.0%**,電子零組件年增**25.4%**,兩者合計占出口**72.0%**。

    #### 3. 明顯的貿易轉移效應
    對美資通產品出口增**1.1倍**,對陸港資通產品出口減**26.7%**。

    #### 4. 貿易順差大幅擴大,集中於美國市場
    總順差**868.9億美元**(年增65.6%),其中對美順差**853.6億美元**。

    #### 5. 產業結構兩極化加劇
    科技產業大幅成長,傳統產業普遍衰退。
    """)

# 🇺🇸 對美貿易分析
elif page == "🇺🇸 對美貿易分析":
    st.markdown('<div class="section-header"><h1>對美貿易深度分析</h1></div>', unsafe_allow_html=True)

    st.markdown("## 對美貿易總覽")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 8月單月")
        st.metric("出口金額", f"${us_trade_summary['8月單月']['出口']:.1f}B",
                 f"+{us_trade_summary['8月單月']['出口年增率']:.1f}%")
        st.metric("進口金額", f"${us_trade_summary['8月單月']['進口']:.1f}B",
                 f"+{us_trade_summary['8月單月']['進口年增率']:.1f}%")

    with col2:
        st.markdown("### 1-8月累計")
        st.metric("出口金額", f"${us_trade_summary['1-8月累計']['出口']:.1f}B",
                 f"+{us_trade_summary['1-8月累計']['出口年增率']:.1f}%")
        st.metric("進口金額", f"${us_trade_summary['1-8月累計']['進口']:.1f}B",
                 f"{us_trade_summary['1-8月累計']['進口年增率']:+.1f}%")

    with col3:
        st.markdown("### 重要指標")
        st.metric("出口市場占比", f"{us_trade_summary['1-8月累計']['出口占比']:.1f}%",
                 "35年新高")
        st.metric("貿易順差", f"${us_trade_summary['1-8月累計']['順差']:.1f}B")

    st.divider()

    # 月度趨勢分析
    st.markdown("## 月度趨勢分析")

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=monthly_export_data['月份'],
            y=monthly_export_data['出口金額'],
            name='出口金額',
            marker_color='#1f77b4'
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=monthly_export_data['月份'],
            y=monthly_export_data['年增率'],
            name='年增率',
            mode='lines+markers',
            line=dict(color='#ff7f0e', width=3)
        ),
        secondary_y=True
    )

    fig.update_layout(
        title='近13個月出口金額與年增率趨勢',
        height=500
    )

    fig.update_xaxes(title_text="月份")
    fig.update_yaxes(title_text="出口金額 (億美元)", secondary_y=False)
    fig.update_yaxes(title_text="年增率 (%)", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # 對美出口商品分析
    st.markdown("## 對美出口商品結構 (8月單月變化)")

    fig = go.Figure()
    colors = ['#2ca02c' if x > 0 else '#d62728' for x in us_export_commodities['變化(億美元)']]

    fig.add_trace(go.Bar(
        x=us_export_commodities['商品'],
        y=us_export_commodities['變化(億美元)'],
        marker_color=colors,
        text=us_export_commodities['變化(億美元)'].apply(lambda x: f'{x:+.1f}')
    ))

    fig.update_layout(
        title='對美出口主要商品變化',
        xaxis_title='商品類別',
        yaxis_title='變化金額 (億美元)',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success("**資通與視聽產品**增加81.5億美元,年增率+110%,是對美出口成長的最大貢獻項目")

# 📦 商品結構分析
elif page == "📦 商品結構分析":
    st.markdown('<div class="section-header"><h1>出口商品結構深度分析</h1></div>', unsafe_allow_html=True)

    st.markdown("## 整體商品結構 (114年1-8月累計)")

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.pie(
            commodity_structure,
            values='金額(億美元)',
            names='商品類別',
            title='出口商品結構占比',
            hole=0.4
        )

        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 前三大商品")

        top3 = commodity_structure.nlargest(3, '金額(億美元)')

        for idx, row in top3.iterrows():
            st.metric(
                label=row['商品類別'],
                value=f"${row['金額(億美元)']:.1f}B ({row['占比(%)']:.1f}%)",
                delta=f"{row['年增率(%)']:+.1f}%"
            )

        st.success("前兩大類(資通+電子)合計占**72.0%**")

    st.divider()

    # 商品成長率分析
    st.markdown("## 商品年增率分析")

    commodity_sorted = commodity_structure.sort_values('年增率(%)', ascending=True)
    colors = ['#2ca02c' if x > 0 else '#d62728' for x in commodity_sorted['年增率(%)']]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=commodity_sorted['商品類別'],
        x=commodity_sorted['年增率(%)'],
        orientation='h',
        marker_color=colors,
        text=commodity_sorted['年增率(%)'].apply(lambda x: f'{x:+.1f}%')
    ))

    fig.update_layout(
        title='各類商品年增率排名',
        xaxis_title='年增率 (%)',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # AI相關產品
    st.markdown("## AI相關產品表現 (8月)")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=ai_related_products['產品'],
        y=ai_related_products['變化(億美元)'],
        marker_color='#9467bd',
        text=ai_related_products['變化(億美元)'].apply(lambda x: f'+{x:.1f}')
    ))

    fig.update_layout(
        title='AI相關產品出口變化',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

# 🌏 市場比較分析
elif page == "🌏 市場比較分析":
    st.markdown('<div class="section-header"><h1>全球市場比較分析</h1></div>', unsafe_allow_html=True)

    st.markdown("## 主要出口市場概覽 (114年1-8月累計)")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            market_export_data,
            values='金額(億美元)',
            names='市場',
            title='出口市場占比分布',
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        colors_market = ['#ff7f0e' if x == '美國' else '#1f77b4' for x in market_export_data['市場']]

        fig.add_trace(go.Bar(
            x=market_export_data['市場'],
            y=market_export_data['金額(億美元)'],
            marker_color=colors_market,
            text=market_export_data['金額(億美元)'].apply(lambda x: f'{x:.1f}')
        ))

        fig.update_layout(title='各市場出口金額', height=450)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # 市場成長率
    st.markdown("## 市場成長率排名")

    market_sorted = market_export_data.sort_values('年增率(%)', ascending=True)
    colors_growth = ['#2ca02c' if x > 0 else '#d62728' for x in market_sorted['年增率(%)']]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=market_sorted['市場'],
        x=market_sorted['年增率(%)'],
        orientation='h',
        marker_color=colors_growth,
        text=market_sorted['年增率(%)'].apply(lambda x: f'{x:+.1f}%')
    ))

    fig.update_layout(
        title='各市場出口年增率',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("**成長冠軍: 美國** (+55.3%)")

    with col2:
        st.info("**成長亞軍: 東協** (+38.2%)")

    with col3:
        st.error("**唯一衰退: 歐洲** (-6.7%)")

# ⚠️ 風險評估
elif page == "⚠️ 風險評估":
    st.markdown('<div class="section-header"><h1>風險因素與不確定性評估</h1></div>', unsafe_allow_html=True)

    st.warning("國際經貿活動依然受美國關稅政策發展、地緣政治風險等變數影響,全球景氣具高度不確定性")

    st.divider()

    st.markdown("## 風險評估儀表板")

    tab1, tab2, tab3 = st.tabs(["政策風險", "產業風險", "經濟風險"])

    with tab1:
        st.markdown("### 政策風險")
        col1, col2 = st.columns(2)

        with col1:
            st.error("""
            **美國關稅政策變化 (風險等級: 高)**
            - 新一輪關稅調整可能性
            - 對特定商品管制強化
            - 要求增加自美採購壓力
            """)

            st.error("""
            **貿易失衡壓力 (風險等級: 高)**
            - 對美順差853.6億美元過大
            - 可能成為談判議題
            - 匯率調整壓力
            """)

        with col2:
            st.warning("""
            **地緣政治風險 (風險等級: 中高)**
            - 台海局勢不確定性
            - 美中科技競爭加劇
            - 供應鏈安全議題
            """)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("對美順差", "853.6億美元", "歷史高位")

        with col2:
            st.metric("順差/總出口比", "21.4%", "過度集中")

        with col3:
            st.metric("對美依存度", "29.4%", "35年新高")

    with tab2:
        st.markdown("### 產業風險")

        col1, col2 = st.columns(2)

        with col1:
            st.error("""
            **產業集中度過高 (風險等級: 高)**
            - 電子及資通產品占出口72.0%
            - 對單一產業依賴度極高
            - 產業週期風險大
            """)

            st.error("""
            **傳統產業衰退 (風險等級: 高)**
            - 塑橡膠: -6.7%
            - 紡織品: -6.3%
            - 就業與區域經濟影響
            """)

        with col2:
            st.warning("""
            **市場集中度提升 (風險等級: 中高)**
            - 對美出口占比29.4%(35年高點)
            - 前三大市場占75.9%
            - 市場過度集中
            """)

            st.info("""
            **AI需求可持續性 (風險等級: 中)**
            - AI熱潮是否可持續?
            - 資本支出是否過度?
            - 庫存調整風險
            """)

        # 產業集中度視覺化
        col1, col2 = st.columns(2)

        with col1:
            fig = go.Figure(data=[go.Pie(
                labels=['科技產業', '傳統產業'],
                values=[72.0, 28.0],
                hole=.3,
                marker_colors=['#1f77b4', '#ff7f0e']
            )])
            fig.update_layout(title='產業結構集中度')
            st.plotly_chart(fig, use_container_width=True)
            st.error("產業過度集中於科技(72%)")

        with col2:
            top3_share = 76.2
            fig = go.Figure(data=[go.Pie(
                labels=['前三大市場', '其他市場'],
                values=[top3_share, 100-top3_share],
                hole=.3,
                marker_colors=['#2ca02c', '#d62728']
            )])
            fig.update_layout(title='市場結構集中度')
            st.plotly_chart(fig, use_container_width=True)
            st.warning(f"前3大市場占{top3_share:.1f}%")

    with tab3:
        st.markdown("### 經濟風險")

        col1, col2 = st.columns(2)

        with col1:
            st.warning("""
            **全球經濟放緩 (風險等級: 中高)**
            - 歐洲市場出口已轉負(-6.7%)
            - 主要國家通膨壓力
            - 消費需求可能走弱
            """)

            st.warning("""
            **匯率波動風險 (風險等級: 中高)**
            - 大量順差導致新台幣升值壓力
            - 影響出口價格競爭力
            - 廠商避險成本增加
            """)

        with col2:
            st.info("""
            **供應鏈過剩風險 (風險等級: 中)**
            - AI熱潮過後的調整
            - 半導體產能擴充過度?
            - 庫存去化壓力
            """)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("出超金額", "868.9億美元", "+65.6%")

        with col2:
            st.metric("歐洲市場", "-6.7%", "唯一衰退")

        with col3:
            st.metric("進口年增", "+21.7%", "需求強勁")

        with col4:
            st.metric("礦產品進口", "-10.7%", "能源價格")

    st.divider()

    # 風險矩陣
    st.markdown("## 風險評估矩陣")

    fig = px.scatter(
        risk_matrix_data,
        x='發生機率',
        y='影響程度',
        size='風險值',
        color='風險類別',
        text='風險項目',
        title='風險評估矩陣 (發生機率 vs 影響程度)',
        size_max=60
    )

    fig.update_traces(textposition='top center')
    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.error("**高風險區** (右上): 影響大且機率高")

    with col2:
        st.warning("**中風險區** (對角線): 需要監控")

    with col3:
        st.success("**低風險區** (左下): 影響小或機率低")

# 📈 互動式探索
elif page == "📈 互動式探索":
    st.markdown('<div class="section-header"><h1>互動式數據探索</h1></div>', unsafe_allow_html=True)

    st.info("使用左側側邊欄的篩選器來自訂您的分析視角")

    with st.sidebar:
        st.markdown("---")
        st.markdown("### 數據篩選器")

        analysis_type = st.selectbox(
            "選擇分析類型",
            ["市場比較", "商品分析", "趨勢分析"]
        )

        if analysis_type == "市場比較":
            selected_markets = st.multiselect(
                "選擇市場",
                market_export_data['市場'].tolist(),
                default=['美國', '中國大陸與香港', '東協']
            )

        elif analysis_type == "商品分析":
            selected_commodities = st.multiselect(
                "選擇商品",
                commodity_structure['商品類別'].tolist(),
                default=['資通與視聽產品', '電子零組件']
            )

        show_data_table = st.checkbox("顯示數據表格", value=False)

    if analysis_type == "市場比較" and 'selected_markets' in locals():
        st.markdown("## 市場深度比較")

        if selected_markets:
            filtered_data = market_export_data[market_export_data['市場'].isin(selected_markets)]

            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(filtered_data, x='市場', y='金額(億美元)',
                            title='選定市場出口金額對比', color='市場')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.bar(filtered_data, x='市場', y='年增率(%)',
                            title='選定市場年增率對比', color='年增率(%)',
                            color_continuous_scale='RdYlGn')
                st.plotly_chart(fig, use_container_width=True)

            if show_data_table:
                st.dataframe(filtered_data, use_container_width=True)

    elif analysis_type == "商品分析" and 'selected_commodities' in locals():
        st.markdown("## 商品深度分析")

        if selected_commodities:
            filtered_data = commodity_structure[commodity_structure['商品類別'].isin(selected_commodities)]

            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(filtered_data, x='商品類別', y='金額(億美元)',
                            title='選定商品出口金額對比', color='商品類別')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.bar(filtered_data, x='商品類別', y='年增率(%)',
                            title='選定商品年增率對比', color='年增率(%)',
                            color_continuous_scale='RdYlGn')
                st.plotly_chart(fig, use_container_width=True)

            if show_data_table:
                st.dataframe(filtered_data, use_container_width=True)

    else:  # 趨勢分析
        st.markdown("## 時間序列趨勢分析")

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=monthly_export_data['月份'], y=monthly_export_data['出口金額'],
                      name='出口金額', mode='lines+markers', fill='tozeroy'),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(x=monthly_export_data['月份'], y=monthly_export_data['年增率'],
                      name='年增率', mode='lines+markers', line=dict(dash='dash')),
            secondary_y=True
        )

        fig.update_layout(title='出口金額與年增率趨勢', height=500)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # 數據下載
    st.markdown("## 數據下載")

    col1, col2, col3 = st.columns(3)

    with col1:
        csv_markets = market_export_data.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="下載市場數據 (CSV)",
            data=csv_markets,
            file_name="market_export_data.csv",
            mime="text/csv"
        )

    with col2:
        csv_commodities = commodity_structure.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="下載商品數據 (CSV)",
            data=csv_commodities,
            file_name="commodity_structure.csv",
            mime="text/csv"
        )

    with col3:
        csv_monthly = monthly_export_data.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="下載月度數據 (CSV)",
            data=csv_monthly,
            file_name="monthly_export_data.csv",
            mime="text/csv"
        )

# ==================== 頁尾 ====================
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 數據來源")
    st.caption("財政部114年8月海關進出口貿易初步統計")

with col2:
    st.markdown("### 更新日期")
    st.caption("114年9月9日")

with col3:
    st.markdown("### 聯絡資訊")
    st.caption("殷英洳科長 (02)2322-8341")

st.markdown("---")
st.caption("© 2025 台灣海關進出口貿易分析系統 | Powered by Streamlit")
