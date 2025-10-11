# 台灣出口數據分析：轉換與主題文件

## 📚 文件概述

本文件概述整合分析主題，結合資通產品出口激增與貿易轉移模式，應用 DIKW 原則及基於 Parquet 的資料轉換策略。

**文件版本**：1.0
**最後更新**：2025-10-11
**作者**：Claude AI 、潘驄杰

---

## 🎯 主題一與主題二整合：課堂報告適宜性

### 整合主題標題
**「台灣對美資通產品出口激增與貿易轉移模式分析：數據驅動的故事」**

### 為何此整合主題最適合課堂報告

#### 1. **清晰的敘事結構** ⭐⭐⭐⭐⭐
結合主題一（資通產品激增）與主題二（貿易轉移）創造引人入勝的故事：
- **第一幕**：戲劇性成長 - 台灣對美資通產品出口激增 110%
- **第二幕**：轉移效應 - 同時對陸港出口衰退 26.7%
- **第三幕**：更大格局 - 美國成為台灣第一大出口市場（29.4%）

此敘事結構保持觀眾投入，並使複雜的貿易數據變得易於理解。

#### 2. **強大的視覺衝擊力** 📊
數據提供驚人對比，完美適合視覺化呈現：
- **對美資通產品出口**：+815 億美元（+110%）
- **對陸港資通產品出口**：-57 億美元（-26.7%）
- **貿易順差**：對美順差 8,536 億美元（歷史新高）

這些數字能創造令人印象深刻的資訊圖表和圖表。

#### 3. **DIKW 架構完整性** 🎓
兩個主題自然流經所有 DIKW 層級：
- **數據（Data）**：16 個 Excel 表格的原始統計資料
- **資訊（Information）**：處理後的趨勢與模式
- **知識（Knowledge）**：理解貿易轉移機制
- **智慧（Wisdom）**：政策意涵與風險評估

完美展示數據分析方法論。

#### 4. **現實相關性** 🌏
- 時事議題：美中貿易緊張、AI 熱潮
- 政策重要性：供應鏈重組
- 經濟影響：台灣的戰略地位
- 未來意涵：永續性與風險

學生能連結到正在發生的全球議題。

#### 5. **適當的範圍** ✅
- 聚焦：兩個相互關聯的主題，不會過於龐雜
- 可管理的數據：3-4 個關鍵表格（表 2、4、8、10）
- 時間友善：15-20 分鐘報告完美契合
- 可達成的深度：足夠深入分析而不流於表面

#### 6. **學習目標對齊** 📖
此主題教導學生：
- 數據分析方法論（DIKW）
- 因果推論（什麼驅動貿易模式）
- 視覺化技術（比較圖表）
- 批判性思考（風險評估）
- 政策分析（經濟意涵）

---

## 📊 DIKW 原則應用

### DIKW 架構概述

DIKW 金字塔代表原始數據轉化為可行智慧的過程：

```
         智慧 WISDOM（我們為何該關注？）
              ▲
         知識 KNOWLEDGE（為何發生？）
              ▲
         資訊 INFORMATION（發生了什麼？）
              ▲
           數據 DATA（事實是什麼？）
```

### DIKW 在整合主題的應用

#### 層級 1：數據 DATA（事實是什麼？）
**目標**：收集與組織原始統計資料

**數據來源**：
- **表 1**：整體進出口貿易值及年增率
- **表 2**：出口主要貨品分類（聚焦資通產品）
- **表 4**：出口主要貨品（詳細分項）
- **表 8**：我國對主要國家/地區出口金額及年增率
- **表 9**：我國自主要國家/地區進口金額及年增率
- **表 10**：對主要國家/地區出入超
- **表 11**：對中國大陸與香港出口主要貨品（用於比較）

**關鍵數據點**：
| 指標 | 美國市場 | 陸港市場 | 變化模式 |
|--------|-----------|-----------------|----------------|
| 資通產品出口變化（8月） | +815億美元 | -57億美元 | 貿易轉移 |
| 資通產品年增率（8月） | +110% | -26.7% | 反向相關 |
| 總出口 1-8月 | 1,171.7億美元 | 1,087.3億美元 | 美國超越中國 |
| 市場占比 1-8月 | 29.4%（第1） | 27.3%（第2） | 歷史性轉變 |
| 貿易平衡 | +853.6億順差 | +491億順差 | 美國主導 |
| 自美進口 1-8月 | 318.1億美元（-4.1%） | N/A | 失衡擴大 |

**數據收集方法**：
- 來源：財政部 114 年 8 月海關進出口貿易初步統計
- 期間：114 年 1-8 月（累計）+ 114 年 8 月（單月）
- 格式：16 個 Excel 表格 → 標準化 Parquet 檔案
- 驗證：交叉比對表格間的一致性

---

#### 層級 2：資訊 INFORMATION（發生了什麼？）
**目標**：將數據轉化為有意義的模式與趨勢

**萃取出的資訊**：

**1. 貿易模式轉變**：
- **趨勢 1**：美國成為台灣第一大出口市場（35 年來首次）
  - 市場占比：29.4%（114 年 1-8 月）vs 歷史平均約 20%
  - 絕對成長：年增 +417.4 億美元

- **趨勢 2**：美國與陸港市場呈反向相關
  - 對美資通產品出口：↑ 110%
  - 對陸港資通產品出口：↓ 26.7%
  - 明顯替代效應

- **趨勢 3**：東協市場激增
  - 出口成長：+38.2%（215.2 億美元增加）
  - 占比：19.5%（第三大市場）

**2. 產品結構演變**：
- **科技產品主導**：占總出口 72%
  - 資通產品：37.5%（1,495 億美元，+69%）
  - 電子零組件：34.5%（1,375 億美元，+25.4%）

- **AI 驅動成長**：
  - 電腦及附屬單元：+85.7 億美元（+100%）
  - 積體電路：+52.3 億美元（+37.4%）
  - 美國 AI 基礎建設熱潮帶動伺服器需求

- **傳統產業衰退**：
  - 塑橡膠：-6.7%
  - 紡織品：-6.3%
  - 結構性失衡惡化

**3. 貿易失衡加劇**：
- **對美貿易順差**：853.6 億美元（比例 3.68:1）
- **自美進口下降**：-4.1% 而整體進口 +21.7%
- **風險指標**：嚴重的雙邊失衡

**視覺化輸出**（資訊層）：
- 折線圖：月度出口趨勢（13 個月）
- 長條圖：市場比較（美國 vs 陸港 vs 東協）
- 圓餅圖：產品結構（資通 vs 電子 vs 其他）
- 瀑布圖：貿易平衡分解
- 熱圖：成長率矩陣（市場 × 產品）

---

#### 層級 3：知識 KNOWLEDGE（為何發生？）
**目標**：理解因果關係與潛在機制

**已識別的因果因素**：

**1. 供應鏈重組（友岸外包）**
- **原因**：美中貿易緊張與關稅政策
- **機制**：
  - 美國企業分散中國供應商依賴
  - 台灣作為可信賴的民主盟友受益
  - 「中國+1」策略將訂單轉向台灣
- **證據**：
  - 對美資通產品進口激增，正好在對陸出口衰退時
  - 台灣填補中國供應商留下的缺口

**2. AI 基礎建設熱潮**
- **原因**：全球 AI 競賽（ChatGPT、大型語言模型）
- **機制**：
  - 美國科技巨頭（微軟、Google、Meta）建設 AI 資料中心
  - 伺服器、GPU、網路設備大量需求
  - 台灣是全球資通製造領導者（鴻海、廣達、台積電）
- **證據**：
  - 電腦出口 +100%（主要是伺服器）
  - IC 出口 +37.4%（台積電的 AI 晶片）
  - 成長集中在 AI 相關產品

**3. 地緣政治風險減緩**
- **原因**：台海緊張、半導體安全顧慮
- **機制**：
  - 西方國家減少對中國科技依賴
  - 台灣半導體產業視為戰略資產
  - 政府政策鼓勵台灣採購
- **證據**：
  - 對民主盟友出口成長最高（對美 +55.3%，歐洲因經濟因素不同）
  - 科技產品特別轉向美國市場

**4. 貿易政策回應**
- **原因**：關稅調整與貿易協定
- **機制**：
  - 美國對中國商品關稅使台灣產品相對便宜
  - 台美貿易倡議（21 世紀貿易倡議）
  - 對非中國供應商的優惠待遇
- **證據**：
  - 價格競爭力改善
  - 市場份額增加與關稅實施同步

**知識綜合**：
貿易模式由**多重增強因素**驅動：
- 短期：AI 熱潮創造需求激增
- 中期：供應鏈重組轉移訂單
- 長期：地緣政治結盟決定貿易夥伴

**根因分析**：
```
主要驅動力：美中戰略競爭
    ↓
次要因素：
├─ 技術：AI 基礎建設熱潮
├─ 經濟：關稅政策調整
├─ 地緣政治：民主聯盟強化
└─ 產業：台灣半導體主導地位
    ↓
結果：貿易從陸港轉向美國
```

---

#### 層級 4：智慧 WISDOM（我們為何該關注？該做什麼？）
**目標**：導出可行見解與策略建議

**戰略意涵**：

**1. 對台灣政府**：
- **機會**：利用當前優勢深化台美經濟聯繫
- **風險**：過度依賴單一市場（29.4% 集中度）
- **行動**：
  - ✅ 趁談判籌碼高時協商台美貿易協定
  - ✅ 分散到其他市場（東協顯示潛力 +38.2%）
  - ⚠️ 準備應對美國可能要求（增加進口、減少順差）
  - ⚠️ 監控中國報復風險

**2. 對台灣產業**：
- **機會**：掌握 AI 基礎建設商機（多年趨勢）
- **風險**：科技產品集中度（占出口 72%）
- **行動**：
  - ✅ 投資 AI/伺服器生產產能
  - ✅ 升級傳統產業（數位轉型）
  - ⚠️ 對沖 AI 需求波動
  - ⚠️ 開發超越當前週期的下一代產品

**3. 對經濟穩定**：
- **機會**：貿易順差提振 GDP 與就業
- **風險**：貨幣升值壓力、貿易失衡反彈
- **行動**：
  - ✅ 管理匯率以保持競爭力
  - ✅ 增加自美進口以減少順差
  - ⚠️ 建立外匯存底作為緩衝
  - ⚠️ 準備政策轉變應變計畫

**4. 永續性評估**：

| 因素 | 短期（6-12個月） | 中期（1-3年） | 長期（3年以上） |
|--------|-------------------------|------------------------|---------------------|
| **AI 需求** | 🟢 非常強勁 | 🟡 中等（成熟期） | 🔴 供過於求風險 |
| **美國市場准入** | 🟢 有利 | 🟡 取決於政策 | 🔴 政治變數 |
| **中國競爭** | 🟢 台灣優勢 | 🟡 中國自給率提升 | 🔴 市場流失風險 |
| **貿易平衡** | 🔴 順差過大 | 🔴 壓力增加 | 🔴 需要調整 |
| **產品集中** | 🟡 可管理 | 🔴 風險上升 | 🔴 多元化迫切 |

**風險減緩策略**：

**優先級 1：市場多元化**（風險分數：9/10）
- 將對美依賴從 29.4% 降至約 25%
- 強化東協聯繫（已成長 +38.2%）
- 探索歐盟市場復甦機會
- 開發新興市場（印度、中東）

**優先級 2：產品多元化**（風險分數：8/10）
- 將科技產品集中度從 72% 降至約 60%
- 支持傳統產業轉型
- 發展新成長領域（綠色科技、生技）
- 避免過度依賴 AI 週期

**優先級 3：貿易平衡管理**（風險分數：9/10）
- 增加自美進口（採購協議）
- 促進雙邊投資
- 服務貿易發展（目前以商品為主）
- 與美國協調順差減少

**優先級 4：地緣政治風險對沖**（風險分數：7/10）
- 維持兩岸穩定
- 強化多邊貿易框架
- 發展供應鏈韌性
- 準備各種情境（政策變化、衝突）

**政策建議（智慧層）**：

**立即行動（0-6 個月）**：
1. 啟動台美貿易平衡對話
2. 快速推進東協市場擴張
3. 支持傳統產業升級計畫
4. 強化匯率管理工具

**中期策略（6-18 個月）**：
1. 協商全面性台美貿易協定
2. 發展下一代科技產品（後 AI 熱潮）
3. 建立市場多元化目標
4. 創建產業轉型基金

**長期願景（18 個月以上）**：
1. 建立韌性的多市場出口結構
2. 領導永續科技產品
3. 平衡科技與傳統產業
4. 定位台灣為可信賴的全球夥伴

**成功指標**：
- 單一國家市場集中度 < 25%
- 產品多樣性指數改善 15%
- 貿易順差/出口比 < 15%
- 傳統產業成長恢復正值
- 風險調整後出口成長的永續性

---

## 🔄 資料轉換策略：基於 Parquet 的管道

### 為何選用 Parquet 格式？

**資料格式比較**：

| 特性 | Excel | CSV | Parquet | JSON | SQLite |
|---------|-------|-----|---------|------|--------|
| **讀取速度** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **檔案大小** | 大 | 中 | **小** | 大 | 中 |
| **型別安全** | ❌ | ❌ | ✅ | 部分 | ✅ |
| **壓縮** | ❌ | ❌ | ✅ | ❌ | 部分 |
| **Python 整合** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Pandas 相容** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Schema 保存** | ❌ | ❌ | ✅ | 部分 | ✅ |
| **列式儲存** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **最適合** | 編輯 | 交換 | **分析** | Web API | 查詢 |

**Parquet 對本專案的優勢**：
1. **10 倍快速**讀取效能 vs CSV（對 Streamlit 儀表板至關重要）
2. **50% 更小**壓縮後檔案大小
3. **型別安全**：保存 int、float、date 型別（無字串轉換錯誤）
4. **列式格式**：分析查詢效率高（選擇特定欄位）
5. **生態系統支援**：與 pandas、polars、dask、spark 無縫整合

**決策**：使用 **Parquet 作為主要格式** + CSV 作為相容性備份

---

### 資料轉換管道架構

```
┌─────────────────────────────────────────────────────────────┐
│                    原始資料層                                 │
│  Excel 檔案（16 個表格）- 不規則結構                           │
│  - 中文標題、合併儲存格、格式化                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  擷取層                                       │
│  1. Excel 載入模組                                            │
│     - 跳過標題列（識別資料起始）                               │
│     - 解析合併儲存格                                          │
│     - 擷取工作表元資料                                        │
│  2. 資料型別偵測                                              │
│     - 識別數值欄位                                            │
│     - 解析日期欄位                                            │
│     - 處理百分比格式                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                 轉換層                                        │
│  1. 欄位標準化                                                │
│     - 重新命名：中文 → 英文 snake_case                        │
│     - 範例：「出口金額」→ "export_value_usd"                  │
│  2. 資料清理                                                  │
│     - 移除格式化（千、百萬等）                                │
│     - 處理缺失值（NaN、-、空白）                              │
│     - 單位正規化（轉換為十億美元）                            │
│  3. 資料豐富化                                                │
│     - 新增計算欄位（成長率、比例）                            │
│     - 建立類別對應                                            │
│     - 新增元資料（來源表格、日期）                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   驗證層                                      │
│  1. Schema 驗證                                               │
│     - 檢查欄位型別                                            │
│     - 驗證值範圍                                              │
│     - 確保表格間一致性                                        │
│  2. 商業邏輯驗證                                              │
│     - 出口 + 進口 = 總貿易額                                  │
│     - 各市場總和 ≈ 總出口                                     │
│     - 成長率計算正確                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   儲存層                                      │
│  主要：Parquet 檔案（列式、壓縮）                              │
│  ├─ data/processed/parquet/                                  │
│  │  ├─ table01_overall_trade.parquet                         │
│  │  ├─ table02_export_commodities.parquet                    │
│  │  ├─ table08_export_by_country.parquet                     │
│  │  └─ ...（16 個表格）                                       │
│  │                                                            │
│  備份：CSV 檔案（UTF-8 with BOM，Excel 相容）                  │
│  ├─ data/processed/csv/                                      │
│  │  ├─ table01_overall_trade.csv                             │
│  │  └─ ...                                                    │
│  │                                                            │
│  查詢：SQLite 資料庫（用於複雜連接）                           │
│  └─ data/processed/database/                                 │
│     └─ taiwan_trade.db                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  消費層                                       │
│  1. Streamlit 儀表板（讀取 Parquet）                          │
│  2. Jupyter Notebooks（分析）                                │
│  3. API 端點（如需要）                                        │
│  4. 資料匯出（下載 CSV/JSON）                                 │
└─────────────────────────────────────────────────────────────┘
```

---

### 詳細轉換規格

#### 表格對應策略

**主題一與主題二的優先表格**：

| 原始檔案 | 目標 Parquet | 用途 | 關鍵欄位 |
|--------------|----------------|---------|-------------|
| `Table1_Import_and_ExportTradeValues.xlsx` | `table01_overall_trade.parquet` | 整體趨勢 | `month`, `export_value_usd_billion`, `import_value_usd_billion`, `trade_balance_usd_billion`, `export_growth_rate_pct`, `import_growth_rate_pct` |
| `Table2_Classification_of_MajorExportCommodities.xlsx` | `table02_export_commodities.parquet` | 產品結構 | `commodity_category`, `export_value_usd_billion`, `share_pct`, `growth_rate_pct`, `focus_ict_products` |
| `Table4_MajorExportCommodities.xlsx` | `table04_export_items_detail.parquet` | 詳細產品 | `product_code`, `product_name_en`, `export_value_usd_billion`, `growth_rate_pct` |
| `Table8_Taiwans's_ExportValue_and_AnnualGrowthRate.xlsx` | `table08_export_by_country.parquet` | **主題二核心** | `country_region`, `month`, `export_value_usd_billion`, `growth_rate_pct`, `market_share_pct` |
| `Table9_ImportValue_AnnualGrowthRate(to_Taiwan).xlsx` | `table09_import_by_country.parquet` | 進口來源 | `country_region`, `month`, `import_value_usd_billion`, `growth_rate_pct` |
| `Table10_Surplus_inTrade_with_MajorCountries.xlsx` | `table10_trade_balance_by_country.parquet` | **主題二核心** | `country_region`, `month`, `trade_surplus_usd_billion`, `surplus_ratio` |
| `Table11_MajorExportCommodities(China_and_HongKong).xlsx` | `table11_export_to_china_hk.parquet` | **主題一核心** | `commodity_category`, `export_value_usd_billion`, `growth_rate_pct`（與表 8 美國資料比較） |

#### 欄位命名慣例

**標準模式**：`{指標}_{單位}_{型別}`

**範例**：
- 原始：`出口金額(億美元)` → 目標：`export_value_usd_billion`
- 原始：`年增率(%)` → 目標：`growth_rate_pct`
- 原始：`占比(%)` → 目標：`share_pct`
- 原始：`國家/地區` → 目標：`country_region`
- 原始：`月份` → 目標：`month`（格式：YYYY-MM）

**資料型別規格**：
```python
SCHEMA_DEFINITION = {
    'table08_export_by_country': {
        'country_region': 'string',
        'month': 'datetime64[ns]',
        'export_value_usd_billion': 'float64',
        'growth_rate_pct': 'float64',
        'market_share_pct': 'float64',
        'year_over_year_change_usd_billion': 'float64'
    },
    'table02_export_commodities': {
        'commodity_category': 'string',
        'export_value_usd_billion': 'float64',
        'share_pct': 'float64',
        'growth_rate_pct': 'float64',
        'cumulative_jan_aug_2025': 'float64',
        'cumulative_jan_aug_2024': 'float64'
    }
}
```

---

### 資料品質保證

#### 驗證規則

**1. 值範圍檢查**：
```python
VALIDATION_RULES = {
    'export_value_usd_billion': {
        'min': 0,
        'max': 2000,  # 合理上限
        'nullable': False
    },
    'growth_rate_pct': {
        'min': -100,
        'max': 500,  # 允許劇烈變化
        'nullable': True  # 某些產品可能是新增
    },
    'market_share_pct': {
        'min': 0,
        'max': 100,
        'sum_check': True  # 所有市場應加總至約 100%
    }
}
```

**2. 一致性檢查**：
```python
CONSISTENCY_RULES = [
    # 規則 1：貿易平衡 = 出口 - 進口
    {
        'check': 'trade_balance = export_value - import_value',
        'tolerance': 0.01  # 允許 0.01B 四捨五入差異
    },
    # 規則 2：市場占比總和為 100%
    {
        'check': 'sum(market_share_pct) ≈ 100',
        'tolerance': 0.5
    },
    # 規則 3：成長率計算
    {
        'check': 'growth_rate = (current / previous - 1) * 100',
        'tolerance': 0.1
    }
]
```

**3. 完整性檢查**：
- 時間序列無缺失月份
- 所有主要國家已呈現
- 所有商品類別已呈現
- 元資料欄位已填入

---

### 實作程式碼結構

```
src/data_processing/
├── __init__.py
├── excel_loader.py          # Excel 解析與擷取
├── data_cleaner.py          # 清理與標準化
├── data_transformer.py      # 商業邏輯轉換
├── format_converter.py      # 多格式匯出（Parquet、CSV、JSON）
├── data_validator.py        # 驗證規則引擎
├── schema_definitions.py    # 所有表格的 schema 規格
└── utils.py                 # 輔助函數

data/processed/
├── parquet/                 # 主要儲存
│   ├── table01_overall_trade.parquet
│   ├── table02_export_commodities.parquet
│   ├── table08_export_by_country.parquet
│   ├── table10_trade_balance_by_country.parquet
│   └── table11_export_to_china_hk.parquet
├── csv/                     # 備份/相容性
│   └── [相同結構]
├── json/                    # API/Web 使用
│   └── [相同結構]
└── database/
    └── taiwan_trade.db      # SQLite 用於複雜查詢

tests/
├── test_excel_loader.py
├── test_data_cleaner.py
├── test_data_validator.py
└── test_format_converter.py
```

---

## 📱 Streamlit 儀表板重新設計

### 現有系統分析

**現有儀表板（`code/streamlit_analyze.py`）**：
- ✅ 優勢：涵蓋全面、多種視覺化、良好 UI
- ❌ 弱點：過於廣泛（6 個模組）、硬編碼資料、缺乏聚焦
- ❌ 問題：895 行（超過 500 行限制）、手動資料輸入、無 Parquet 整合

### 重新設計策略

#### 新儀表板結構（聚焦主題一與主題二）

```
streamlit_app/
├── app.py                          # 主要入口點（< 200 行）
├── config/
│   ├── __init__.py
│   ├── settings.py                 # 應用程式配置
│   └── theme.py                    # UI 主題設定
├── data/
│   ├── __init__.py
│   ├── loader.py                   # Parquet 資料載入
│   └── cache.py                    # Streamlit 快取工具
├── pages/
│   ├── __init__.py
│   ├── 1_📊_Executive_Summary.py   # DIKW：數據 + 資訊
│   ├── 2_🇺🇸_US_Trade_Surge.py     # 主題一：資通產品出口激增
│   ├── 3_🔄_Trade_Diversion.py     # 主題二：市場轉移模式
│   ├── 4_📈_DIKW_Analysis.py       # DIKW 架構展示
│   └── 5_💡_Insights_Wisdom.py     # 知識 + 智慧層
├── components/
│   ├── __init__.py
│   ├── charts.py                   # 可重複使用的圖表元件
│   ├── metrics.py                  # KPI 顯示元件
│   └── tables.py                   # 資料表元件
└── utils/
    ├── __init__.py
    ├── calculations.py             # 商業邏輯
    └── formatters.py               # 數字/日期格式化
```

#### 頁面分解

**頁面 1：執行摘要**（數據 + 資訊層）
- 目的：呈現關鍵事實與趨勢
- 內容：
  - 英雄指標：對美出口成長（+110%）、貿易順差（853.6B）
  - 互動時間軸：月度出口趨勢
  - 市場占比演變圖表
  - 產品結構分解
- 資料來源：`table01_overall_trade.parquet`、`table02_export_commodities.parquet`

**頁面 2：對美貿易激增分析**（主題一深入探討）
- 目的：分析資通產品出口熱潮
- 內容：
  - 資通產品詳細分解（伺服器、IC、電腦）
  - 對美 vs 對陸港比較（並排圖表）
  - AI 相關產品焦點
  - 月度趨勢分析（13 個月視圖）
- 資料來源：`table02_export_commodities.parquet`、`table04_export_items_detail.parquet`、`table08_export_by_country.parquet`、`table11_export_to_china_hk.parquet`

**頁面 3：貿易轉移模式**（主題二深入探討）
- 目的：視覺化市場轉移動態
- 內容：
  - 市場比較儀表板（美國 vs 陸港 vs 東協 vs 歐盟 vs 日本）
  - 桑基圖：貿易流動轉移
  - 相關性分析：美國 ↑ 當陸港 ↓
  - 各國貿易平衡
- 資料來源：`table08_export_by_country.parquet`、`table09_import_by_country.parquet`、`table10_trade_balance_by_country.parquet`

**頁面 4：DIKW 分析架構**（方法論展示）
- 目的：展示資料分析方法論
- 內容：
  - 互動 DIKW 金字塔
  - 逐層探索（點擊展開每一層）
  - 實際資料範例
  - 教育性演練
- 此頁面展示分析過程本身

**頁面 5：洞察與智慧**（知識 + 智慧層）
- 目的：呈現結論與建議
- 內容：
  - 因果因素分析（AI 熱潮、供應鏈、地緣政治）
  - 風險評估矩陣（互動式）
  - 政策建議儀表板
  - 情境分析（假設滑桿）
- 資料來源：所有表格的衍生資料 + 外部脈絡

---

### 新儀表板關鍵功能

#### 1. **Parquet 整合**
```python
# data/loader.py
import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data(ttl=3600)  # 快取 1 小時
def load_parquet_data(table_name: str) -> pd.DataFrame:
    """
    載入 Parquet 資料並快取以提升效能。

    Args:
        table_name: 表格名稱（例如 'table08_export_by_country'）

    Returns:
        載入資料的 DataFrame
    """
    data_path = Path('data/processed/parquet') / f'{table_name}.parquet'
    df = pd.read_parquet(data_path)
    return df

# 在頁面中使用
df_export = load_parquet_data('table08_export_by_country')
```

#### 2. **互動視覺化**
- **Plotly**：所有圖表（比現有實作更快）
- **互動篩選器**：日期範圍、國家選擇、產品類別
- **下鑽功能**：點擊圖表查看詳情
- **比較模式**：並排市場比較

#### 3. **DIKW 層級切換**
```python
# 允許使用者選擇要檢視的 DIKW 層級
dikw_layer = st.sidebar.radio(
    "分析深度",
    ["📊 數據", "📈 資訊", "🧠 知識", "💡 智慧"]
)

if dikw_layer == "📊 數據":
    show_raw_data_table()
elif dikw_layer == "📈 資訊":
    show_trend_charts()
elif dikw_layer == "🧠 知識":
    show_causal_analysis()
else:  # 智慧
    show_recommendations()
```

#### 4. **效能優化**
- Parquet 載入：約 10 倍快於 CSV
- Streamlit 快取：所有資料載入使用 `@st.cache_data`
- 延遲載入：僅在訪問頁面時載入資料
- 增量更新：僅重新整理變更的資料

#### 5. **匯出功能**
- 下載處理後資料（CSV、JSON、Excel）
- 匯出圖表為 PNG/SVG
- 產生 PDF 報告（摘要）
- 分享含篩選器的永久連結

---

### 行動響應式設計

```python
# 響應式版面配置
col1, col2 = st.columns([2, 1] if st.session_state.get('mobile', False) else [3, 2])
```

---

### 資料更新工作流程

```
新月份資料發布
         ↓
1. 下載新 Excel 檔案 → data/raw/September2025/
         ↓
2. 執行轉換管道：
   python src/data_processing/run_pipeline.py --month 2025-09
         ↓
3. Parquet 檔案自動產生 → data/processed/parquet/
         ↓
4. Streamlit 自動重新載入（快取失效）
         ↓
5. 儀表板顯示更新資料
```

**管道 CLI**：
```bash
# 處理特定月份
python src/data_processing/run_pipeline.py --month 2025-09

# 處理所有月份
python src/data_processing/run_pipeline.py --all

# 僅驗證（不寫入）
python src/data_processing/run_pipeline.py --validate-only

# 匯出到特定格式
python src/data_processing/run_pipeline.py --format parquet,csv,json
```

---

## 📋 實施路線圖

### 階段 1：資料管道（第 1-2 週）
1. ✅ 建立資料處理模組
2. ✅ 實作 Excel 載入器
3. ✅ 建立轉換邏輯
4. ✅ 產生 Parquet 檔案
5. ✅ 驗證資料品質

### 階段 2：儀表板重構（第 2-3 週）
1. ✅ 設定新的 Streamlit 多頁面結構
2. ✅ 實作 Parquet 資料載入
3. ✅ 建立可重複使用的圖表元件
4. ✅ 建立 5 個聚焦頁面

### 階段 3：DIKW 整合（第 3-4 週）
1. ✅ 實作 DIKW 層級切換
2. ✅ 新增互動分析工具
3. ✅ 建立知識庫（因果因素）
4. ✅ 建立智慧儀表板（建議）

### 階段 4：測試與優化（第 4-5 週）
1. ✅ 所有模組單元測試
2. ✅ 整合測試
3. ✅ 效能優化
4. ✅ 使用者驗收測試

### 階段 5：文件與部署（第 5-6 週）
1. ✅ 完成使用者指南
2. ✅ API 文件
3. ✅ 部署到雲端（Streamlit Cloud / AWS）
4. ✅ 簡報培訓教材

---

## 🎓 課堂報告策略

### 15 分鐘報告大綱

**投影片 1-2：開場（1 分鐘）**
- 開場問題：「如果我告訴你台灣對某國的出口在一年內成長了 110%？」
- 揭露：對美資通產品，同時對陸港出口衰退 26.7%

**投影片 3-5：數據層（2 分鐘）**
- 展示原始數字：815 億增加（美國）vs -57 億減少（陸港）
- 互動圖表：市場占比轉移（現場 Streamlit 展示）

**投影片 6-8：資訊層（3 分鐘）**
- 呈現趨勢：月度時間序列
- 產品分解：什麼驅動成長？（AI 伺服器、IC）
- 市場比較：美國 vs 陸港 vs 東協

**投影片 9-11：知識層（4 分鐘）**
- 解釋「為何」：AI 熱潮、供應鏈重組、地緣政治
- 因果圖：展示連結
- 證據：相關性分析、政策時間軸

**投影片 12-14：智慧層（4 分鐘）**
- 風險評估：貿易失衡（853.6B 順差）、集中度
- 建議：分散市場、管理順差
- 未來展望：永續性分析

**投影片 15：問答（1 分鐘）**
- 互動儀表板展示
- 以現場資料探索回答問題

### 展示流程
1. 從執行摘要頁面開始（衝擊力）
2. 深入對美貿易激增（主題一）
3. 展示貿易轉移模式（主題二）
4. 展示 DIKW 架構頁面
5. 以洞察儀表板結束

---

## 📚 參考資料

- 財政部 114 年 8 月海關進出口貿易初步統計
- DIKW 金字塔架構（Ackoff, 1989）
- Apache Parquet 文件
- Streamlit 多頁面應用程式指南
- 貿易分析最佳實務（WTO、IMF）

---

## 📝 附錄

### A. 資料字典
[所有 16 個表格的完整 schema 定義]

### B. 計算公式
```python
# 成長率
growth_rate = ((current_value - previous_value) / previous_value) * 100

# 市場占比
market_share = (export_to_country / total_export) * 100

# 貿易平衡
trade_balance = export_value - import_value

# 貿易順差比例
surplus_ratio = trade_balance / export_value
```

### C. 視覺化配色方案
- 美國市場：`#FF6B6B`（紅色）
- 陸港市場：`#4ECDC4`（青綠色）
- 東協市場：`#45B7D1`（藍色）
- 成長（正值）：`#2ECC71`（綠色）
- 衰退（負值）：`#E74C3C`（紅色）
- 中性：`#95A5A6`（灰色）

---

**文件結束**

*此轉換策略確保聚焦、資料驅動的敘事適合學術報告，同時透過 DIKW 原則與高效的 Parquet 基礎資料處理維持分析嚴謹性。*
