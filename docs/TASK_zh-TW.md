# 台灣出口分析專案 - 任務實施計畫

**專案名稱**：台灣對美資通產品出口激增與貿易轉移模式分析
**建立日期**：2025-10-11
**最後更新**：2025-10-11
**專案負責人**：AI 分析團隊
**預期時程**：5-6 週

---

## 階段一：資料管道開發

### [ ] **任務編號**：PHASE1-TASK1
- **任務名稱**：Excel 資料載入模組開發
- **工作說明**：
    - **為何**：目前的 Excel 檔案具有不規則結構（中文標題、合併儲存格、格式化），無法直接載入 Python。我們需要強健的解析器從 16 個 Excel 表格中提取乾淨資料。
    - **如何**：
        1. 建立 `src/data_processing/excel_loader.py` 模組
        2. 實作函數以偵測標題列（跳過中文標題）
        3. 使用 `openpyxl` 函式庫解析合併儲存格
        4. 擷取元資料（表格名稱、日期、來源）
        5. 處理多工作表 Excel 檔案
        6. 回傳包含原始資料的 pandas DataFrame
- **所需資源**：
    - **材料**：
        - `data/August2025_PreliminaryStatistics_on_CustomsImports_and_Exports/` 中的 16 個 Excel 檔案
        - Python 函式庫：`pandas`、`openpyxl`、`xlrd`
    - **人員**：
        - 1 位 Python 開發者（資料工程專長）
    - **參考程式碼/文件**：
        - Pandas Excel I/O 文件：https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
        - Openpyxl 文件：https://openpyxl.readthedocs.io/
        - `docs/TaiwanExport_Transform.md`（章節：資料轉換管道架構）
- **交付成果**：
    - [ ] `src/data_processing/excel_loader.py`（< 200 行）
    - [ ] 函數：`load_excel_table(file_path: str, table_id: str) -> pd.DataFrame`
    - [ ] `tests/test_excel_loader.py` 中的單元測試
    - [ ] 包含使用範例的文件
- **依賴項**：
    - 無（管道中的第一個任務）
- **限制條件**：
    - 必須處理所有 16 個不同結構的表格
    - 必須保留資料型別（數值、日期、文字）
    - 每個表格處理時間 < 5 秒
- **完成狀態**：⬜ 未開始
- **備註**：
    - 優先表格：表 2、4、8、10、11（主題一與主題二所需）
    - 如果結構差異顯著，考慮建立特定表格的解析器

---

### [ ] **任務編號**：PHASE1-TASK2
- **任務名稱**：資料清理與標準化模組
- **工作說明**：
    - **為何**：原始 Excel 資料包含不一致的格式（如千/百萬單位、百分比、缺失值）。我們需要標準化、乾淨的資料進行分析。
    - **如何**：
        1. 建立 `src/data_processing/data_cleaner.py` 模組
        2. 實作欄位重新命名：中文 → 英文 snake_case（出口金額 → export_value_usd_billion）
        3. 移除格式符號並轉換為數值
        4. 以適當策略處理缺失值（NaN、-、空白儲存格）
        5. 單位正規化（全部轉換為十億美元、百分比轉小數）
        6. 標準化日期格式（YYYY-MM）
- **所需資源**：
    - **材料**：
        - 任務 PHASE1-TASK1 的輸出（原始 DataFrames）
        - 欄位對應字典（中英文）
    - **人員**：
        - 1 位 Python 開發者（資料清理專長）
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（章節：欄位命名慣例）
        - Pandas 資料清理指南
        - `src/data_processing/schema_definitions.py`（待建立）
- **交付成果**：
    - [ ] `src/data_processing/data_cleaner.py`（< 250 行）
    - [ ] `src/data_processing/schema_definitions.py`（所有表格的 schema 規格）
    - [ ] 函數：`clean_dataframe(df: pd.DataFrame, table_id: str) -> pd.DataFrame`
    - [ ] 欄位對應配置檔：`config/column_mappings.json`
    - [ ] `tests/test_data_cleaner.py` 中的單元測試
- **依賴項**：
    - PHASE1-TASK1（Excel 載入器必須完成）
- **限制條件**：
    - 清理過程中不得遺失資料
    - 欄位名稱必須遵循 snake_case 慣例
    - 所有數值必須為 float64 型別
- **完成狀態**：⬜ 未開始
- **備註**：
    - 為常見模式建立可重複使用的清理函數
    - 記錄所有清理操作以供稽核追蹤

---

### [ ] **任務編號**：PHASE1-TASK3
- **任務名稱**：資料轉換與豐富化模組
- **工作說明**：
    - **為何**：除了清理，我們還需要計算欄位（成長率、市場占比、貿易平衡）以及豐富化的元資料供分析使用。
    - **如何**：
        1. 建立 `src/data_processing/data_transformer.py` 模組
        2. 計算衍生指標：
            - 年增率
            - 市場占比百分比
            - 貿易平衡（出口 - 進口）
            - 累計總和
        3. 新增元資料欄位（source_table、processing_date、data_month）
        4. 建立聚合視圖（例如季度摘要）
        5. 連結相關表格（用於 join 的外鍵）
- **所需資源**：
    - **材料**：
        - PHASE1-TASK2 清理後的 DataFrames
        - `docs/TaiwanExport_Transform.md` 的商業邏輯規格
    - **人員**：
        - 1 位資料分析師/開發者（理解商業邏輯）
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（附錄 B：計算公式）
        - 領域專家諮詢商業規則
- **交付成果**：
    - [ ] `src/data_processing/data_transformer.py`（< 300 行）
    - [ ] 函數：`transform_dataframe(df: pd.DataFrame, table_id: str) -> pd.DataFrame`
    - [ ] 商業邏輯文件
    - [ ] `tests/test_data_transformer.py` 中的單元測試
- **依賴項**：
    - PHASE1-TASK2（資料清理器必須完成）
- **限制條件**：
    - 計算必須準確（與來源資料測試）
    - 效能：每個表格轉換 < 2 秒
- **完成狀態**：⬜ 未開始
- **備註**：
    - 確保成長率公式符合官方計算方法
    - 新增驗證以在可用時對照來源檢查計算值

---

### [ ] **任務編號**：PHASE1-TASK4
- **任務名稱**：Parquet 格式轉換器與多格式匯出
- **工作說明**：
    - **為何**：Parquet 格式提供 10 倍快的讀取效能與 50% 更小的檔案大小（相較於 CSV），對 Streamlit 儀表板效能至關重要。
    - **如何**：
        1. 建立 `src/data_processing/format_converter.py` 模組
        2. 實作 Parquet 匯出（snappy 壓縮）
        3. 實作 CSV 匯出（UTF-8 with BOM 以相容 Excel）
        4. 實作 JSON 匯出（供 API 使用）
        5. 建立包含所有表格的 SQLite 資料庫（用於複雜查詢）
        6. 為 Parquet 檔案新增 schema 保存
- **所需資源**：
    - **材料**：
        - PHASE1-TASK3 轉換後的 DataFrames
        - Python 函式庫：`pyarrow`、`fastparquet`
    - **人員**：
        - 1 位 Python 開發者（資料工程）
    - **參考程式碼/文件**：
        - Apache Parquet 文件
        - `docs/TaiwanExport_Transform.md`（章節：為何選用 Parquet 格式？）
- **交付成果**：
    - [ ] `src/data_processing/format_converter.py`（< 150 行）
    - [ ] 函數：`export_to_parquet(df: pd.DataFrame, output_path: str)`
    - [ ] 函數：`export_to_csv(df: pd.DataFrame, output_path: str)`
    - [ ] 函數：`export_to_sqlite(dfs: Dict[str, pd.DataFrame], db_path: str)`
    - [ ] 目錄結構：`data/processed/{parquet,csv,json,database}/`
    - [ ] `tests/test_format_converter.py` 中的單元測試
- **依賴項**：
    - PHASE1-TASK3（資料轉換器必須完成）
- **限制條件**：
    - Parquet 檔案必須可被 Streamlit 讀取
    - CSV 必須相容 Excel（UTF-8 with BOM）
    - 檔案大小減少目標：相較 CSV 減少 50%
- **完成狀態**：⬜ 未開始
- **備註**：
    - 使用 snappy 壓縮 Parquet（速度/大小良好平衡）
    - 測試跨平台相容性（Windows/Linux/Mac）

---

### [ ] **任務編號**：PHASE1-TASK5
- **任務名稱**：資料驗證與品質保證模組
- **工作說明**：
    - **為何**：在分析前確保資料完整性與準確性。及早發現錯誤以防止錯誤見解。
    - **如何**：
        1. 建立 `src/data_processing/data_validator.py` 模組
        2. 實作值範圍檢查（最小/最大界限）
        3. 實作一致性檢查（貿易平衡 = 出口 - 進口）
        4. 驗證總和限制（市場占比 ≈ 100%）
        5. 檢查缺失的關鍵資料
        6. 依商業規則驗證
        7. 產生驗證報告
- **所需資源**：
    - **材料**：
        - 先前任務處理的資料
        - `docs/TaiwanExport_Transform.md` 的驗證規則
    - **人員**：
        - 1 位 QA 分析師/開發者
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（章節：資料品質保證）
        - Great Expectations 函式庫（選用）
- **交付成果**：
    - [ ] `src/data_processing/data_validator.py`（< 200 行）
    - [ ] 驗證規則配置：`config/validation_rules.yaml`
    - [ ] 函數：`validate_dataframe(df: pd.DataFrame, rules: dict) -> ValidationReport`
    - [ ] 驗證報告產生器（HTML/JSON 輸出）
    - [ ] `tests/test_data_validator.py` 中的單元測試
- **依賴項**：
    - PHASE1-TASK4（格式轉換器必須完成）
- **限制條件**：
    - 所有表格驗證必須在 < 10 秒內完成
    - 必須捕捉至少 95% 的資料品質問題
- **完成狀態**：⬜ 未開始
- **備註**：
    - 考慮使用 Great Expectations 進行進階驗證
    - 為關鍵驗證失敗建立警示

---

### [ ] **任務編號**：PHASE1-TASK6
- **任務名稱**：資料管道編排與 CLI 工具
- **工作說明**：
    - **為何**：需要自動化管道以在每月處理新資料時無需人工介入。CLI 工具能輕鬆執行與排程。
    - **如何**：
        1. 建立 `src/data_processing/run_pipeline.py` 編排器
        2. 整合所有模組（載入器 → 清理器 → 轉換器 → 轉換器 → 驗證器）
        3. 使用 argparse 新增 CLI 介面（--month、--all、--validate-only、--format）
        4. 實作錯誤處理與記錄
        5. 建立進度指示器
        6. 新增失敗時的回滾功能
- **所需資源**：
    - **材料**：
        - PHASE1-TASK1 至 PHASE1-TASK5 的所有模組
        - Python 函式庫：`argparse`、`logging`、`tqdm`
    - **人員**：
        - 1 位 Python 開發者（管道/DevOps 專長）
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（章節：資料更新工作流程）
        - Python Click 或 argparse 文件
- **交付成果**：
    - [ ] `src/data_processing/run_pipeline.py`（< 300 行）
    - [ ] CLI 使用文件：`docs/pipeline_usage.md`
    - [ ] 記錄配置：`config/logging.yaml`
    - [ ] README 中的範例指令
    - [ ] 自動執行的 Shell 腳本：`scripts/run_monthly_update.sh`
- **依賴項**：
    - 所有 PHASE1 任務（TASK1-5）必須完成
- **限制條件**：
    - 所有 16 個表格的管道必須在 < 2 分鐘內完成
    - 必須優雅地處理失敗（非關鍵錯誤時繼續）
    - 記錄必須足夠詳細以供除錯
- **完成狀態**：⬜ 未開始
- **備註**：
    - 新增 dry-run 模式（--dry-run）供測試
    - 考慮新增完成/失敗時的電子郵件通知

---

## 階段二：Streamlit 儀表板重構

### [ ] **任務編號**：PHASE2-TASK1
- **任務名稱**：多頁面 Streamlit 應用程式設定
- **工作說明**：
    - **為何**：現有單一檔案儀表板（895 行）超過最佳實務（500 行上限）。多頁面結構提升可維護性與聚焦度。
    - **如何**：
        1. 建立新目錄結構：`streamlit_app/` 包含 pages、components、utils
        2. 設定 `app.py` 為主要入口點（< 200 行）
        3. 配置 Streamlit 多頁面設定
        4. 實作導覽側邊欄
        5. 設定頁面路由
        6. 將主題/樣式遷移至 `config/theme.py`
- **所需資源**：
    - **材料**：
        - 現有 `code/streamlit_analyze.py`（供參考）
        - Streamlit 多頁面應用程式文件
    - **人員**：
        - 1 位前端開發者（Streamlit 經驗）
    - **參考程式碼/文件**：
        - Streamlit 多頁面應用程式：https://docs.streamlit.io/library/get-started/multipage-apps
        - `docs/TaiwanExport_Transform.md`（章節：新儀表板結構）
- **交付成果**：
    - [ ] 新目錄結構：`streamlit_app/{app.py, config/, pages/, components/, utils/, data/}`
    - [ ] `streamlit_app/app.py` - 主要入口點
    - [ ] `streamlit_app/config/settings.py` - 應用程式配置
    - [ ] `streamlit_app/config/theme.py` - UI 主題
    - [ ] 導覽側邊欄實作
    - [ ] `.streamlit/config.toml` - Streamlit 配置
- **依賴項**：
    - 無（可與階段一平行開始）
- **限制條件**：
    - 每個頁面檔案必須 < 300 行
    - 必須維持現有 UI/UX 品質
    - 頁面載入時間 < 2 秒
- **完成狀態**：⬜ 未開始
- **備註**：
    - 使用 Streamlit 原生多頁面功能（st.pages）
    - 考慮為頁面新增圖示以提升 UX

---

### [ ] **任務編號**：PHASE2-TASK2
- **任務名稱**：Parquet 資料載入器與快取系統
- **工作說明**：
    - **為何**：Parquet 提供 10 倍快於 CSV 的載入速度。Streamlit 快取防止冗餘載入，提升效能。
    - **如何**：
        1. 建立 `streamlit_app/data/loader.py` 模組
        2. 使用 `@st.cache_data` 實作 Parquet 載入函數
        3. 新增缺失檔案的錯誤處理
        4. 建立資料重新整理機制（快取失效）
        5. 實作延遲載入（僅在需要時載入）
        6. 新增資料版本支援
- **所需資源**：
    - **材料**：
        - `data/processed/parquet/` 的 Parquet 檔案
        - Python 函式庫：`pandas`、`pyarrow`、`streamlit`
    - **人員**：
        - 1 位 Python 開發者（效能優化專長）
    - **參考程式碼/文件**：
        - Streamlit 快取文件：https://docs.streamlit.io/library/advanced-features/caching
        - `docs/TaiwanExport_Transform.md`（章節：Parquet 整合）
- **交付成果**：
    - [ ] `streamlit_app/data/loader.py`（< 150 行）
    - [ ] 函數：`load_parquet_data(table_name: str) -> pd.DataFrame` 包含快取
    - [ ] `streamlit_app/data/cache.py` - 快取工具
    - [ ] 資料載入效能測試
    - [ ] 包含使用範例的文件
- **依賴項**：
    - PHASE1-TASK4（Parquet 檔案必須存在）
    - PHASE2-TASK1（應用程式結構必須設定）
- **限制條件**：
    - 每個表格載入時間 < 500ms
    - 快取 TTL：1 小時（可配置）
    - 所有快取資料的記憶體使用 < 500MB
- **完成狀態**：⬜ 未開始
- **備註**：
    - 使用大型資料集測試以確保效能
    - 在側邊欄新增快取統計顯示（供除錯）

---

### [ ] **任務編號**：PHASE2-TASK3
- **任務名稱**：可重複使用圖表元件函式庫
- **工作說明**：
    - **為何**：避免程式碼重複。所有頁面視覺化一致。更容易維護與更新。
    - **如何**：
        1. 建立 `streamlit_app/components/charts.py` 模組
        2. 實作可重複使用的 Plotly 圖表函數：
            - 折線圖（時間序列）
            - 長條圖（比較）
            - 圓餅圖（市場占比）
            - 瀑布圖（貿易平衡）
            - 桑基圖（貿易流動）
            - 熱圖（相關性矩陣）
        3. 新增自訂參數（顏色、標題、註解）
        4. 確保響應式設計（行動裝置友善）
- **所需資源**：
    - **材料**：
        - Plotly 文件
        - `docs/TaiwanExport_Transform.md` 的設計指南（附錄 C：配色方案）
    - **人員**：
        - 1 位資料視覺化專家
    - **參考程式碼/文件**：
        - Plotly 文件：https://plotly.com/python/
        - `code/streamlit_analyze.py`（現有圖表供參考）
        - `docs/TaiwanExport_Transform.md`（配色方案章節）
- **交付成果**：
    - [ ] `streamlit_app/components/charts.py`（< 400 行）
    - [ ] 所有圖表類型的函數（8+ 個圖表函數）
    - [ ] `streamlit_app/components/metrics.py` - KPI 顯示元件
    - [ ] `streamlit_app/components/tables.py` - 資料表元件
    - [ ] 圖表畫廊頁面（供測試/展示）
    - [ ] 元件文件
- **依賴項**：
    - PHASE2-TASK2（資料載入器必須就緒）
- **限制條件**：
    - 所有圖表必須使用一致的配色方案
    - 圖表渲染時間 < 1 秒
    - 必須在行動螢幕上運作（響應式）
- **完成狀態**：⬜ 未開始
- **備註**：
    - 較簡單的圖表使用 Plotly Express
    - 考慮新增匯出功能（PNG、SVG）

---

### [ ] **任務編號**：PHASE2-TASK4
- **任務名稱**：商業邏輯與計算工具
- **工作說明**：
    - **為何**：將商業邏輯與呈現分離。能在頁面間測試與重複使用。
    - **如何**：
        1. 建立 `streamlit_app/utils/calculations.py` 模組
        2. 實作計算函數：
            - 成長率計算
            - 市場占比計算
            - 貿易平衡計算
            - 趨勢分析（移動平均等）
            - 統計摘要
        3. 在 `streamlit_app/utils/formatters.py` 新增格式化器：
            - 數字格式化（十億、百分比）
            - 日期格式化
            - 貨幣格式化
- **所需資源**：
    - **材料**：
        - `docs/TaiwanExport_Transform.md` 的商業邏輯（附錄 B）
        - `code/streamlit_analyze.py` 中的現有計算
    - **人員**：
        - 1 位 Python 開發者
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（計算公式）
- **交付成果**：
    - [ ] `streamlit_app/utils/calculations.py`（< 200 行）
    - [ ] `streamlit_app/utils/formatters.py`（< 100 行）
    - [ ] `tests/test_calculations.py` 中的單元測試
    - [ ] 工具函數文件
- **依賴項**：
    - PHASE2-TASK2（資料載入器）
- **限制條件**：
    - 所有計算必須進行單元測試
    - 效能：任何計算 < 100ms
- **完成狀態**：⬜ 未開始
- **備註**：
    - 考慮使用 numpy 進行向量化運算（更快）

---

### [ ] **任務編號**：PHASE2-TASK5
- **任務名稱**：頁面 1 - 執行摘要（數據 + 資訊層）
- **工作說明**：
    - **為何**：第一頁必須以關鍵事實與趨勢吸引觀眾。代表 DIKW 的數據與資訊層。
    - **如何**：
        1. 建立 `streamlit_app/pages/1_📊_Executive_Summary.py`
        2. 顯示英雄指標：對美出口成長（+110%）、貿易順差（853.6B）
        3. 互動時間軸：月度出口趨勢（13 個月）
        4. 市場占比演變圖表（美國 vs 陸港 vs 東協）
        5. 產品結構分解（資通 vs 電子 vs 其他）
        6. 重點發現摘要
- **所需資源**：
    - **材料**：
        - `table01_overall_trade.parquet`、`table02_export_commodities.parquet`、`table08_export_by_country.parquet` 的資料
        - PHASE2-TASK3 的圖表元件
    - **人員**：
        - 1 位前端開發者（Streamlit）
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（頁面 1 規格）
        - `code/streamlit_analyze.py` 中的現有執行摘要
- **交付成果**：
    - [ ] `streamlit_app/pages/1_📊_Executive_Summary.py`（< 250 行）
    - [ ] 4 個英雄指標（KPI 卡片）
    - [ ] 互動時間軸圖表
    - [ ] 市場占比圓餅圖
    - [ ] 產品結構視覺化
- **依賴項**：
    - PHASE2-TASK2（資料載入器）
    - PHASE2-TASK3（圖表元件）
    - PHASE2-TASK4（計算）
- **限制條件**：
    - 頁面載入時間 < 2 秒
    - 所有資料必須來自 Parquet 檔案（無硬編碼）
- **完成狀態**：⬜ 未開始
- **備註**：
    - 這是登陸頁面 - 必須留下強烈第一印象

---

### [ ] **任務編號**：PHASE2-TASK6
- **任務名稱**：頁面 2 - 對美貿易激增分析（主題一深入探討）
- **工作說明**：
    - **為何**：主題一（對美資通產品出口激增）的核心分析頁面。必須顯示詳細分解與比較。
    - **如何**：
        1. 建立 `streamlit_app/pages/2_🇺🇸_US_Trade_Surge.py`
        2. 顯示資通產品詳細分解（伺服器、IC、電腦）
        3. 對美 vs 對陸港並排比較圖表
        4. AI 相關產品焦點區塊
        5. 月度趨勢分析（13 個月互動圖表）
        6. 出口驅動因素分析（哪些產品驅動成長）
- **所需資源**：
    - **材料**：
        - `table02_export_commodities.parquet`、`table04_export_items_detail.parquet`、`table08_export_by_country.parquet`、`table11_export_to_china_hk.parquet` 的資料
        - 圖表元件
    - **人員**：
        - 1 位前端開發者 + 1 位資料分析師（提供洞察）
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（頁面 2 規格、主題一章節）
- **交付成果**：
    - [ ] `streamlit_app/pages/2_🇺🇸_US_Trade_Surge.py`（< 300 行）
    - [ ] 資通產品分解儀表板
    - [ ] 對美 vs 對陸港比較區塊
    - [ ] AI 產品焦點視覺化
    - [ ] 含篩選器的月度趨勢互動圖表
- **依賴項**：
    - PHASE2-TASK2、PHASE2-TASK3、PHASE2-TASK4
- **限制條件**：
    - 必須清楚呈現 110% 成長故事
    - 互動篩選器必須順暢運作
- **完成狀態**：⬜ 未開始
- **備註**：
    - 此頁面講述主要故事 - 投資時間於 UX

---

### [ ] **任務編號**：PHASE2-TASK7
- **任務名稱**：頁面 3 - 貿易轉移模式分析（主題二深入探討）
- **工作說明**：
    - **為何**：主題二（貿易從中國轉向美國）的核心分析頁面。必須視覺化市場動態。
    - **如何**：
        1. 建立 `streamlit_app/pages/3_🔄_Trade_Diversion.py`
        2. 市場比較儀表板（美國 vs 陸港 vs 東協 vs 歐盟 vs 日本）
        3. 顯示貿易流動轉移的桑基圖
        4. 相關性分析：顯示反向關係（美國 ↑ 當陸港 ↓）
        5. 各國貿易平衡視覺化
        6. 顯示市場占比演變的時間序列
- **所需資源**：
    - **材料**：
        - `table08_export_by_country.parquet`、`table09_import_by_country.parquet`、`table10_trade_balance_by_country.parquet` 的資料
        - 桑基圖元件（Plotly）
    - **人員**：
        - 1 位前端開發者 + 1 位資料視覺化專家
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（頁面 3 規格、主題二章節）
        - Plotly 桑基圖：https://plotly.com/python/sankey-diagram/
- **交付成果**：
    - [ ] `streamlit_app/pages/3_🔄_Trade_Diversion.py`（< 300 行）
    - [ ] 市場比較儀表板（5 個市場）
    - [ ] 貿易流動桑基圖
    - [ ] 相關性分析視覺化
    - [ ] 貿易平衡圖表
- **依賴項**：
    - PHASE2-TASK2、PHASE2-TASK3、PHASE2-TASK4
- **限制條件**：
    - 桑基圖必須清楚顯示轉移模式
    - 所有 5 個市場必須在相同尺度上可比較
- **完成狀態**：⬜ 未開始
- **備註**：
    - 桑基圖是關鍵 - 徹底測試清晰度

---

### [ ] **任務編號**：PHASE2-TASK8
- **任務名稱**：頁面 4 - DIKW 分析架構（方法論展示）
- **工作說明**：
    - **為何**：教育頁面展示資料分析方法論。顯示我們如何從數據 → 資訊 → 知識 → 智慧。
    - **如何**：
        1. 建立 `streamlit_app/pages/4_📈_DIKW_Analysis.py`
        2. 互動 DIKW 金字塔視覺化（點擊展開每一層）
        3. 逐層探索：
            - 數據層：顯示原始表格
            - 資訊層：顯示處理後的趨勢/圖表
            - 知識層：顯示因果分析
            - 智慧層：顯示建議
        4. 每一層的實際資料範例
        5. 含說明的教育性演練
- **所需資源**：
    - **材料**：
        - `docs/TaiwanExport_Transform.md` 的 DIKW 架構文件
        - 所有處理後的資料
    - **人員**：
        - 1 位前端開發者 + 1 位教育內容設計師
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（DIKW 原則應用章節）
        - DIKW 金字塔參考資料
- **交付成果**：
    - [ ] `streamlit_app/pages/4_📈_DIKW_Analysis.py`（< 250 行）
    - [ ] 互動 DIKW 金字塔元件
    - [ ] 層級切換功能（單選按鈕）
    - [ ] 每個 DIKW 層級的範例
    - [ ] 教育性說明
- **依賴項**：
    - PHASE2-TASK5、PHASE2-TASK6、PHASE2-TASK7（需要其他頁面的內容）
- **限制條件**：
    - 必須具教育性且吸引人
    - 每個 DIKW 層級間明確區別
- **完成狀態**：⬜ 未開始
- **備註**：
    - 此頁面展示方法論 - 對學術報告很重要

---

### [ ] **任務編號**：PHASE2-TASK9
- **任務名稱**：頁面 5 - 洞察與智慧（知識 + 智慧層）
- **工作說明**：
    - **為何**：最終頁面提供可行見解與建議。代表 DIKW 的知識與智慧層。
    - **如何**：
        1. 建立 `streamlit_app/pages/5_💡_Insights_Wisdom.py`
        2. 因果因素分析區塊（AI 熱潮、供應鏈、地緣政治）
        3. 互動風險評估矩陣（2D 散佈圖）
        4. 政策建議儀表板
        5. 含假設滑桿的情境分析（例如，若對美進口增加 X%）
        6. 永續性評估（短/中/長期展望）
- **所需資源**：
    - **材料**：
        - `docs/TaiwanExport_Transform.md` 的分析洞察（知識與智慧章節）
        - 風險矩陣資料
    - **人員**：
        - 1 位前端開發者 + 1 位政策分析師（提供內容）
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（層級 3 與 4：知識與智慧）
        - 風險矩陣的互動 Plotly 散佈圖
- **交付成果**：
    - [ ] `streamlit_app/pages/5_💡_Insights_Wisdom.py`（< 300 行）
    - [ ] 因果因素分析視覺化
    - [ ] 互動風險評估矩陣
    - [ ] 政策建議區塊
    - [ ] 情境分析工具（滑桿 + 反應式圖表）
    - [ ] 永續性展望儀表板
- **依賴項**：
    - 所有先前的階段二任務
- **限制條件**：
    - 建議必須以資料驅動（連結至圖表）
    - 情境分析必須即時更新（< 500ms）
- **完成狀態**：⬜ 未開始
- **備註**：
    - 這是「所以呢？」頁面 - 對展示價值至關重要

---

## 階段三：DIKW 架構整合

### [ ] **任務編號**：PHASE3-TASK1
- **任務名稱**：DIKW 層級切換系統實作
- **工作說明**：
    - **為何**：允許使用者在 DIKW 層級間切換以理解分析深度。作為方法論展示的教育工具。
    - **如何**：
        1. 建立 DIKW 層級選擇的全域狀態管理
        2. 實作側邊欄切換（單選按鈕：數據、資訊、知識、智慧）
        3. 讓所有頁面回應層級選擇
        4. 依選定層級顯示/隱藏內容
        5. 在每頁新增層級指示器
- **所需資源**：
    - **材料**：
        - Streamlit session state
        - 階段二的所有頁面檔案
    - **人員**：
        - 1 位前端開發者（Streamlit 狀態管理）
    - **參考程式碼/文件**：
        - Streamlit session state：https://docs.streamlit.io/library/api-reference/session-state
        - `docs/TaiwanExport_Transform.md`（DIKW 層級切換章節）
- **交付成果**：
    - [ ] `streamlit_app/app.py` 中的全域 DIKW 狀態管理
    - [ ] 側邊欄 DIKW 層級選擇器
    - [ ] 所有 5 頁中的層級響應內容
    - [ ] 目前層級的視覺指示器
- **依賴項**：
    - PHASE2-TASK5 至 TASK9（所有頁面必須建立）
- **限制條件**：
    - 層級切換必須即時（< 100ms）
    - 狀態必須在頁面導覽期間保持
- **完成狀態**：⬜ 未開始
- **備註**：
    - 在所有頁面徹底測試一致性

---

### [ ] **任務編號**：PHASE3-TASK2
- **任務名稱**：互動分析工具開發
- **工作說明**：
    - **為何**：讓使用者自行探索資料。增加參與度與理解。
    - **如何**：
        1. 新增日期範圍選擇器（依月份篩選）
        2. 新增國家/地區選擇器（多選）
        3. 新增產品類別篩選器
        4. 實作下鑽功能（點擊圖表查看詳情）
        5. 新增比較模式（並排市場比較）
        6. 建立資料匯出工具（下載篩選後資料）
- **所需資源**：
    - **材料**：
        - Streamlit 小工具（selectbox、multiselect、date_input）
        - Plotly 點擊事件
    - **人員**：
        - 1 位前端開發者（互動專長）
    - **參考程式碼/文件**：
        - Streamlit 小工具：https://docs.streamlit.io/library/api-reference/widgets
        - Plotly 事件：https://plotly.com/python/click-events/
- **交付成果**：
    - [ ] 側邊欄中的全域篩選面板
    - [ ] 所有圖表的下鑽功能
    - [ ] 比較模式切換
    - [ ] 資料匯出元件（CSV、JSON、Excel）
    - [ ] 篩選狀態管理
- **依賴項**：
    - PHASE3-TASK1（DIKW 層級系統必須就位）
- **限制條件**：
    - 篩選器必須在 < 1 秒內更新圖表
    - 匯出必須適用所有資料大小
- **完成狀態**：⬜ 未開始
- **備註**：
    - 考慮新增「重設所有篩選器」按鈕

---

### [ ] **任務編號**：PHASE3-TASK3
- **任務名稱**：知識庫與因果分析元件
- **工作說明**：
    - **為何**：代表知識層 - 解釋「為何」模式發生。與僅顯示資料做區別。
    - **如何**：
        1. 建立因果圖元件（流程圖）
        2. 實作因素分析視覺化（貢獻因素長條圖）
        3. 新增相關性分析工具（熱圖）
        4. 建立證據呈現格式（資料 → 結論連結）
        5. 建立知識卡片（可展開區塊含說明）
- **所需資源**：
    - **材料**：
        - `docs/TaiwanExport_Transform.md` 的因果關係（知識章節）
        - Plotly 網路圖
    - **人員**：
        - 1 位資料視覺化專家 + 1 位內容撰寫者
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（層級 3：知識）
        - Plotly 網路圖
- **交付成果**：
    - [ ] `streamlit_app/components/` 中的因果圖元件
    - [ ] 因素分析視覺化
    - [ ] 相關性熱圖工具
    - [ ] 知識卡片元件（可重複使用）
    - [ ] 證據連結系統（資料 → 結論）
- **依賴項**：
    - PHASE2-TASK3（圖表元件）
    - PHASE3-TASK1（DIKW 層級系統）
- **限制條件**：
    - 因果圖必須清晰且不雜亂
    - 知識必須有資料支持（可驗證）
- **完成狀態**：⬜ 未開始
- **備註**：
    - 此元件將我們的分析與簡單報告區別開來

---

### [ ] **任務編號**：PHASE3-TASK4
- **任務名稱**：智慧儀表板與建議系統
- **工作說明**：
    - **為何**：最高 DIKW 層級 - 提供可行見解與策略建議。
    - **如何**：
        1. 建立建議卡片元件
        2. 實作風險評估矩陣視覺化
        3. 建立優先順序排名系統（依影響/緊急程度排序建議）
        4. 新增情境模擬器（假設分析）
        5. 建立永續性展望時間軸（短/中/長期）
        6. 實作行動計畫產生器
- **所需資源**：
    - **材料**：
        - `docs/TaiwanExport_Transform.md` 的建議（智慧章節）
        - 風險矩陣資料
    - **人員**：
        - 1 位前端開發者 + 1 位政策/策略分析師
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（層級 4：智慧、戰略意涵）
        - 風險矩陣範本
- **交付成果**：
    - [ ] 頁面 5 中的建議儀表板
    - [ ] 風險評估矩陣（互動 2D 圖）
    - [ ] 優先順序排名系統
    - [ ] 情境模擬器元件
    - [ ] 永續性時間軸視覺化
    - [ ] 可下載的行動計畫（PDF）
- **依賴項**：
    - PHASE3-TASK3（知識元件）
- **限制條件**：
    - 建議必須具體且可行
    - 風險分數必須以資料驅動（非主觀）
- **完成狀態**：⬜ 未開始
- **備註**：
    - 這是「價值交付」元件 - 對影響至關重要

---

## 階段四：測試與優化

### [ ] **任務編號**：PHASE4-TASK1
- **任務名稱**：所有模組的單元測試
- **工作說明**：
    - **為何**：確保程式碼正確性並防止迴歸。維護性必需。
    - **如何**：
        1. 為所有資料處理模組撰寫單元測試
        2. 為所有工具函數撰寫單元測試
        3. 達成最低 80% 程式碼覆蓋率
        4. 測試邊緣案例（空資料、缺失值、極端值）
        5. 設定 pytest 框架
        6. 配置持續測試
- **所需資源**：
    - **材料**：
        - 階段一與階段二的所有模組
        - Python 函式庫：`pytest`、`pytest-cov`、`pytest-mock`
    - **人員**：
        - 1 位 QA 工程師 / 測試開發者
    - **參考程式碼/文件**：
        - Pytest 文件：https://docs.pytest.org/
        - 測試最佳實務
- **交付成果**：
    - [ ] `tests/` 目錄中的完整測試套件
    - [ ] 測試覆蓋率報告（>80% 覆蓋率）
    - [ ] `pytest.ini` 配置
    - [ ] 測試文件：`tests/README.md`
    - [ ] CI/CD 整合（GitHub Actions / GitLab CI）
- **依賴項**：
    - PHASE1（所有資料處理模組）
    - PHASE2（所有工具函數）
- **限制條件**：
    - 最低 80% 程式碼覆蓋率
    - 所有測試必須在部署前通過
    - 測試執行時間 < 30 秒
- **完成狀態**：⬜ 未開始
- **備註**：
    - 使用 fixtures 作為測試資料
    - Mock 外部依賴（檔案 I/O）

---

### [ ] **任務編號**：PHASE4-TASK2
- **任務名稱**：端對端管道整合測試
- **工作說明**：
    - **為何**：確保所有元件正確協同運作。在生產前捕捉整合問題。
    - **如何**：
        1. 建立整合測試情境（Excel → Parquet → Streamlit）
        2. 測試完整管道執行
        3. 測試 Streamlit 應用程式載入與功能
        4. 驗證所有元件間的資料一致性
        5. 測試錯誤處理與復原
- **所需資源**：
    - **材料**：
        - 階段一的完整管道
        - 階段二與三的完整儀表板
        - 測試資料（範例 Excel 檔案）
    - **人員**：
        - 1 位 QA 工程師
    - **參考程式碼/文件**：
        - 整合測試最佳實務
        - Streamlit 測試指南
- **交付成果**：
    - [ ] `tests/integration/` 中的整合測試套件
    - [ ] 端對端測試情境
    - [ ] Streamlit 應用程式測試（使用 Playwright 或 Selenium）
    - [ ] 資料一致性驗證測試
    - [ ] 整合測試報告
- **依賴項**：
    - PHASE4-TASK1（單元測試必須通過）
    - 所有先前階段完成
- **限制條件**：
    - 完整管道測試必須在 < 5 分鐘內完成
    - 所有整合測試必須通過
- **完成狀態**：⬜ 未開始
- **備註**：
    - 考慮使用 Docker 建立一致的測試環境

---

### [ ] **任務編號**：PHASE4-TASK3
- **任務名稱**：效能優化與分析
- **工作說明**：
    - **為何**：確保儀表板快速載入並高效處理資料。使用者體驗取決於效能。
    - **如何**：
        1. 分析資料載入效能（識別瓶頸）
        2. 優化 Streamlit 快取策略
        3. 減少記憶體使用（延遲載入、資料取樣）
        4. 優化 Plotly 圖表渲染
        5. 為大型資料集實作漸進式載入
        6. 新增效能監控
- **所需資源**：
    - **材料**：
        - 階段二與三的完整儀表板
        - Python 分析工具：`cProfile`、`memory_profiler`、`line_profiler`
    - **人員**：
        - 1 位效能工程師
    - **參考程式碼/文件**：
        - Streamlit 效能技巧：https://docs.streamlit.io/library/advanced-features/performance
        - Python 分析指南
- **交付成果**：
    - [ ] 效能分析報告
    - [ ] 優化的資料載入（目標：每表格 < 500ms）
    - [ ] 優化的圖表渲染（目標：每圖表 < 1s）
    - [ ] 記憶體使用優化（目標：< 500MB）
    - [ ] 效能監控儀表板（選用）
- **依賴項**：
    - PHASE4-TASK2（整合測試必須通過）
- **限制條件**：
    - 頁面載入時間 < 2 秒（目標）
    - 記憶體使用 < 500MB（目標）
    - 功能不得降級
- **完成狀態**：⬜ 未開始
- **備註**：
    - 聚焦於 Parquet 載入與快取 - 影響最大的領域

---

### [ ] **任務編號**：PHASE4-TASK4
- **任務名稱**：使用者驗收測試（UAT）與回饋收集
- **工作說明**：
    - **為何**：驗證儀表板符合使用者需求與期望。在最終部署前收集回饋。
    - **如何**：
        1. 招募 3-5 位測試使用者（同學、教師）
        2. 準備 UAT 測試計畫與情境
        3. 進行使用者測試會議
        4. 收集回饋（問卷、訪談）
        5. 識別可用性問題
        6. 優先處理並實作修正
- **所需資源**：
    - **材料**：
        - 完整的儀表板（生產就緒）
        - UAT 測試計畫
        - 回饋收集表單
    - **人員**：
        - 1 位 UX 研究員 / 產品經理
        - 3-5 位測試使用者
    - **參考程式碼/文件**：
        - UAT 最佳實務
        - 可用性測試指南
- **交付成果**：
    - [ ] UAT 測試計畫文件
    - [ ] 使用者測試會議（可能的話錄製影片）
    - [ ] 回饋收集報告
    - [ ] 優先處理的改進待辦清單
    - [ ] 關鍵修正的實作
- **依賴項**：
    - PHASE4-TASK3（效能優化完成）
- **限制條件**：
    - 最少 3 位使用者必須測試
    - 必須在發布前處理關鍵問題（嚴重度 1-2）
- **完成狀態**：⬜ 未開始
- **備註**：
    - 考慮與技術與非技術使用者測試
    - 聚焦於課堂報告可用性

---

## 階段五：文件與部署

### [ ] **任務編號**：PHASE5-TASK1
- **任務名稱**：使用者文件與指南建立
- **工作說明**：
    - **為何**：讓使用者能理解並有效使用儀表板。對課堂報告與交接至關重要。
    - **如何**：
        1. 建立使用者指南：`docs/user_guide.md`
        2. 撰寫每頁的功能文件
        3. 建立快速入門指南
        4. 新增疑難排解區塊
        5. 建立影片演練（選用但推薦）
        6. 在儀表板中新增內嵌說明提示
- **所需資源**：
    - **材料**：
        - 完整的儀表板
        - 螢幕截圖與螢幕錄影
    - **人員**：
        - 1 位技術撰寫者
    - **參考程式碼/文件**：
        - 技術撰寫最佳實務
        - Streamlit 文件範例
- **交付成果**：
    - [ ] 使用者指南：`docs/user_guide.md`
    - [ ] 快速入門指南：`docs/quick_start.md`
    - [ ] 每頁的功能文件
    - [ ] 疑難排解指南
    - [ ] 影片演練（5-10 分鐘，選用）
    - [ ] 儀表板中的內嵌說明提示
- **依賴項**：
    - PHASE4-TASK4（UAT 完成，所有功能最終確定）
- **限制條件**：
    - 文件必須對非技術使用者清楚
    - 必須包含所有主要功能的螢幕截圖
- **完成狀態**：⬜ 未開始
- **備註**：
    - 考慮為課堂報告技巧建立單獨指南

---

### [ ] **任務編號**：PHASE5-TASK2
- **任務名稱**：API 與開發者文件
- **工作說明**：
    - **為何**：讓未來開發者能維護與擴充系統。良好的文件對永續性至關重要。
    - **如何**：
        1. 建立所有模組的 API 文件
        2. 記錄資料管道架構
        3. 建立程式碼貢獻指南
        4. 記錄部署程序
        5. 為所有函數新增 docstrings（Google 風格）
        6. 使用 Sphinx 或 MkDocs 產生 API 文件
- **所需資源**：
    - **材料**：
        - 所有原始碼
        - 架構圖
    - **人員**：
        - 1 位開發者 + 1 位技術撰寫者
    - **參考程式碼/文件**：
        - Sphinx 文件：https://www.sphinx-doc.org/
        - Google Python 風格指南：https://google.github.io/styleguide/pyguide.html
- **交付成果**：
    - [ ] API 文件（從 docstrings 自動產生）
    - [ ] 架構文件：`docs/architecture.md`
    - [ ] 程式碼貢獻指南：`CONTRIBUTING.md`
    - [ ] 部署指南：`docs/deployment.md`
    - [ ] 所有函數的 Docstrings（Google 風格）
    - [ ] 產生的 API 文件網站（Sphinx/MkDocs）
- **依賴項**：
    - 階段一至三的所有程式碼必須完成
- **限制條件**：
    - 所有公開函數必須有 docstrings
    - API 文件必須自動產生（非手動）
- **完成狀態**：⬜ 未開始
- **備註**：
    - 考慮使用 Read the Docs 託管文件

---

### [ ] **任務編號**：PHASE5-TASK3
- **任務名稱**：雲端部署設定
- **工作說明**：
    - **為何**：讓儀表板可線上存取以供課堂報告與分享。啟用遠端存取。
    - **如何**：
        1. 選擇部署平台（Streamlit Cloud / AWS / Heroku）
        2. 設定部署配置
        3. 配置環境變數與機密
        4. 設定自動部署的 CI/CD 管道
        5. 配置自訂網域（選用）
        6. 設定 SSL 憑證（HTTPS）
        7. 監控部署健康狀況
- **所需資源**：
    - **材料**：
        - 完整的儀表板程式碼
        - 部署平台帳號（推薦 Streamlit Cloud）
        - CI/CD 工具（GitHub Actions）
    - **人員**：
        - 1 位 DevOps 工程師
    - **參考程式碼/文件**：
        - Streamlit Cloud 文件：https://docs.streamlit.io/streamlit-community-cloud
        - GitHub Actions：https://docs.github.com/en/actions
- **交付成果**：
    - [ ] 已部署的儀表板（公開 URL）
    - [ ] 部署配置檔（例如 `.streamlit/config.toml`）
    - [ ] CI/CD 管道（git push 時自動部署）
    - [ ] 環境變數設定
    - [ ] SSL 憑證（HTTPS）
    - [ ] 監控設定（正常運作時間、錯誤）
- **依賴項**：
    - PHASE4（所有測試完成）
    - PHASE5-TASK1、TASK2（文件完成）
- **限制條件**：
    - 必須支援 HTTPS（安全連線）
    - 正常運作時間目標：99%（需監控）
    - 免費層級可接受（若符合需求）
- **完成狀態**：⬜ 未開始
- **備註**：
    - 推薦 Streamlit Cloud（免費層級、易設定）
    - 將 API 金鑰與機密保存在環境變數（不在程式碼中）

---

### [ ] **任務編號**：PHASE5-TASK4
- **任務名稱**：課堂報告教材準備
- **工作說明**：
    - **為何**：最終目標是成功的課堂報告。需要精緻的教材與練習。
    - **如何**：
        1. 建立報告投影片（15-20 張）
        2. 準備展示腳本（逐步）
        3. 建立講義教材（摘要頁）
        4. 準備問答預期問題
        5. 排練報告（2-3 次練習）
        6. 設定備用計畫（離線展示、影片錄製）
- **所需資源**：
    - **材料**：
        - 完整的儀表板（已部署）
        - 分析的主要發現
        - 報告軟體（PowerPoint、Google Slides）
    - **人員**：
        - 報告者
        - 1 位報告教練（選用）
    - **參考程式碼/文件**：
        - `docs/TaiwanExport_Transform.md`（章節：課堂報告策略）
        - 報告最佳實務
- **交付成果**：
    - [ ] 報告投影片（15-20 張，PDF + 原始檔）
    - [ ] 含時間控制的展示腳本：`docs/presentation_script.md`
    - [ ] 講義教材（1 頁摘要）
    - [ ] 問答準備文件（預期問題 + 答案）
    - [ ] 備用教材（影片錄製、離線展示）
    - [ ] 排練回饋報告
- **依賴項**：
    - PHASE5-TASK3（儀表板必須已部署）
    - 所有文件完成
- **限制條件**：
    - 報告必須為 15 分鐘 ± 2 分鐘
    - 必須展示現場儀表板（不只是投影片）
    - 必須明確涵蓋 DIKW 架構
- **完成狀態**：⬜ 未開始
- **備註**：
    - 使用計時器練習 - 15 分鐘過得很快
    - 為技術問題準備（有備用影片/螢幕截圖）

---

### [ ] **任務編號**：PHASE5-TASK5
- **任務名稱**：最終審查與品質保證
- **工作說明**：
    - **為何**：報告前的最終檢查點。確保一切完美運作。
    - **如何**：
        1. 進行最終程式碼審查
        2. 驗證所有交付成果已完成
        3. 測試已部署的儀表板（生產環境）
        4. 審查所有文件的準確性
        5. 驗證報告教材
        6. 建立交接檢查清單
        7. 封存專案資產
- **所需資源**：
    - **材料**：
        - 所有專案交付成果
        - 已部署的儀表板
        - 文件
    - **人員**：
        - 1 位專案經理 + 1 位 QA 主管
    - **參考程式碼/文件**：
        - 品質保證檢查清單
        - 專案結案最佳實務
- **交付成果**：
    - [ ] 最終程式碼審查報告
    - [ ] 交付成果完成檢查清單（所有任務已驗證）
    - [ ] 生產環境測試報告
    - [ ] 文件準確性驗證
    - [ ] 報告教材最終審查
    - [ ] 專案交接套件（包含所有資產的 ZIP）
    - [ ] 經驗學習文件
- **依賴項**：
    - 所有先前任務（PHASE5-TASK1 至 TASK4）
- **限制條件**：
    - 所有任務必須 100% 完成
    - 生產環境無關鍵錯誤
    - 所有文件必須是最新的
- **完成狀態**：⬜ 未開始
- **備註**：
    - 這是報告前的最終關卡
    - 要徹底 - 最後一次發現問題的機會

---

## 專案時程摘要

| 階段 | 時程 | 任務數 | 關鍵路徑 |
|-------|----------|-------|---------------|
| **階段一：資料管道** | 2 週 | 6 個任務 | TASK1 → TASK2 → TASK3 → TASK4 → TASK5 → TASK6 |
| **階段二：儀表板重構** | 2 週 | 9 個任務 | TASK1 → TASK2 → (TASK3,TASK4) → (TASK5-9 平行) |
| **階段三：DIKW 整合** | 1 週 | 4 個任務 | TASK1 → (TASK2,TASK3,TASK4 平行) |
| **階段四：測試與優化** | 1 週 | 4 個任務 | TASK1 → TASK2 → TASK3 → TASK4 |
| **階段五：文件與部署** | 1 週 | 5 個任務 | (TASK1,TASK2 平行) → TASK3 → TASK4 → TASK5 |
| **總計** | **5-6 週** | **28 個任務** | - |

---

## 風險減緩

| 風險 | 影響 | 機率 | 減緩策略 |
|------|--------|-------------|---------------------|
| 資料品質問題 | 高 | 中 | 全面驗證（PHASE1-TASK5） |
| 效能問題 | 高 | 低 | Parquet 格式 + 快取 + 分析（PHASE4-TASK3） |
| 範圍蔓延 | 中 | 高 | 嚴格遵守僅主題一與二 |
| 報告時技術故障 | 高 | 低 | 備用教材（影片、離線展示） |
| 時程延誤 | 中 | 中 | 盡可能平行執行任務 |
| 缺失需求 | 中 | 中 | 及早 UAT（PHASE4-TASK4） |

---

## 成功標準

### 技術成功
- [ ] 所有 16 個 Excel 表格成功轉換為 Parquet 格式
- [ ] 儀表板載入時間 < 2 秒
- [ ] 所有資料視覺化正確渲染
- [ ] DIKW 架構清楚展示
- [ ] 達成 80%+ 測試覆蓋率
- [ ] 生產環境零關鍵錯誤

### 學術成功
- [ ] 清楚展示主題一（資通產品出口激增）
- [ ] 清楚展示主題二（貿易轉移）
- [ ] DIKW 方法論明確顯示
- [ ] 報告在 15 分鐘時限內
- [ ] 觀眾參與與理解
- [ ] 問答成功處理

### 專案管理成功
- [ ] 所有 28 個任務按時完成
- [ ] 文件完整且準確
- [ ] 已部署的儀表板線上可存取
- [ ] 交接套件已交付
- [ ] 經驗學習已記錄

---

## 附錄：關鍵指令

### 資料管道
```bash
# 執行完整管道
python src/data_processing/run_pipeline.py --month 2025-08

# 僅驗證資料
python src/data_processing/run_pipeline.py --validate-only

# 匯出特定格式
python src/data_processing/run_pipeline.py --format parquet,csv
```

### 測試
```bash
# 執行所有測試
pytest tests/ -v

# 含覆蓋率執行
pytest tests/ --cov=src --cov-report=html

# 執行特定測試
pytest tests/test_excel_loader.py -v
```

### Streamlit
```bash
# 在本地執行儀表板
streamlit run streamlit_app/app.py

# 使用特定埠執行
streamlit run streamlit_app/app.py --server.port 8502
```

### 部署
```bash
# 部署到 Streamlit Cloud（透過 git push）
git push origin main

# 檢查部署狀態
streamlit cloud logs
```

---

**文件結束**

*此任務清單提供實施台灣出口分析專案的全面路線圖，包含清楚的交付成果、依賴項與成功標準。*
