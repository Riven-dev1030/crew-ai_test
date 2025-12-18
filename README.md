# CrewAI MVP: 動漫推薦系統

這是一個完整的 CrewAI 最小可行產品（MVP），展示了多個 Claude AI 代理如何協作完成複雜任務。
使用 Anthropic 的 Claude 大語言模型，建立智能動漫推薦系統。

## 功能概述

### 三個協作代理：
1. **用戶清單解析器** - 讀取並解析用戶提供的動漫清單，理解用戶品味
2. **維基百科研究員** - 查詢維基百科獲取年度優質動漫排名
3. **動漫推薦引擎** - 根據用戶清單和業界排名，生成個性化推薦

### 工作流程：
```
用戶清單 (anime_list.json)
    ↓
[用戶清單解析器] → 分析品味
    ↓
[維基百科研究員] → 獲取業界排名
    ↓
[動漫推薦引擎] → 生成個性化推薦
```

## 快速開始

### 1. 創建並啟用虛擬環境

```bash
# 進入項目目錄
cd crew-ai_test

# 創建虛擬環境
python3 -m venv venv

# 啟用虛擬環境
# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

啟用後終端會顯示：
```
(venv) user@host:~/crew-ai_test$
```

### 2. 安裝依賴

```bash
pip install -r requirements.txt
```

### 3. 配置 Claude API
```bash
# 複製示例配置文件
cp .env.example .env

# 編輯 .env 文件，添加您的 Anthropic API 密鑰
export ANTHROPIC_API_KEY='your-api-key-here'
```

**獲取 API 密鑰**：
1. 訪問 [Anthropic Console](https://console.anthropic.com)
2. 創建新的 API 密鑰
3. 將密鑰保存到 `.env` 文件

### 4. 編輯清單文件（可選）

程式支援三種清單格式，選擇最方便的方式編輯：

**JSON 格式** (`anime_list.json`)：
```json
[
  "進擊的巨人",
  "咒術回戰",
  "鬼滅之刃",
  "死亡筆記"
]
```

**純文本格式** (`anime_list.txt`)，每行一部動漫：
```
進擊的巨人
咒術回戰
鬼滅之刃
死亡筆記
```

**CSV 格式** (`anime_list.csv`)，支援帶有年份和類型（取第一列）：
```
進擊的巨人,2013,動作/懸疑
咒術回戰,2020,動作/超能力
鬼滅之刃,2019,動作/冒險
死亡筆記,2006,懸疑/心理
```

### 5. 運行程序

**完整版本**（需要 Claude API 密鑰）：
```bash
python main.py
```

程序會自動：
1. 讀取清單文件（自動偵測格式）
2. 查詢維基百科獲取年度動漫排名
3. 生成個性化推薦

**支援的清單文件名**（程式會自動偵測最新修改的文件）：
- `anime_list.json` - JSON 陣列格式
- `anime_list.txt` - 純文本格式（每行一部）
- `anime_list.csv` - CSV 格式（取第一欄）

**智能文件偵測**：
- 程式會自動檢查三個文件中哪個最新修改過
- 優先讀取最新修改的文件
- 你可以隨時編輯任何格式的文件，程式會自動使用最新的清單

**演示版本**（無需 API 密鑰）：
```bash
python demo.py
```

## 虛擬環境

### 什麼是虛擬環境？

虛擬環境是一個獨立的 Python 環境，讓妳的項目依賴不會影響系統 Python。

### 虛擬環境位置

```
crew-ai_test/
└── venv/              ← 虛擬環境目錄
    ├── bin/           ← Python 可執行文件
    ├── lib/           ← 已安裝的套件
    └── pyvenv.cfg    ← 配置文件
```

### 常用命令

```bash
# 啟用虛擬環境
source venv/bin/activate     # Linux / macOS
venv\Scripts\activate        # Windows

# 檢查已安裝的套件
pip list

# 安裝新套件
pip install <package-name>

# 退出虛擬環境
deactivate
```

### 為什麼虛擬環境在 GitHub 上看不到？

虛擬環境被添加到 `.gitignore`，所以不會上傳到 GitHub：
- ✅ **優點**：減少倉庫大小、避免環境衝突
- ✅ **方式**：別人可以透過 `pip install -r requirements.txt` 快速復現環境

## 項目結構

```
crew-ai_test/
├── main.py                 # 主程序（代理和任務定義）
├── anime_list.json        # JSON 格式清單（示例）
├── anime_list.txt         # 純文本格式清單（示例）
├── anime_list.csv         # CSV 格式清單（示例）
├── requirements.txt        # 依賴包列表
├── .env.example           # 環境變量示例
├── demo.py                # 演示版本（無需API）
└── README.md             # 本文件
```

### 清單文件格式

程式支援三種清單格式，自動偵測文件副檔名：

| 格式 | 文件名 | 特點 |
|------|--------|------|
| **JSON** | `anime_list.json` | 結構化格式，適合複雜資料 |
| **純文本** | `anime_list.txt` | 最簡單，每行一部動漫 |
| **CSV** | `anime_list.csv` | 支援多欄資料，取第一欄為動漫名稱 |

程式會自動偵測並解析對應格式的檔案。

## 代碼主要組件

### 自定義工具
- `read_user_list(json_string)` - 讀取和解析用戶提供的動漫清單
- `search_wikipedia_anime()` - 查詢維基百科的年度動漫排名清單
- `recommend_anime(user_list, wiki_list)` - 根據兩個清單生成個性化推薦

### 文件讀取函數
- `load_anime_list_from_file(filename=None)` - 從外部文件讀取動漫清單，支援 JSON、純文本、CSV 三種格式
  - 如果不指定文件名，自動偵測最新修改的清單文件
  - 自動偵測文件副檔名並使用對應的解析方式
  - 支援 UTF-8 編碼
  - 提供詳細的錯誤提示

- `find_latest_anime_list_file()` - 尋找最新修改的清單文件
  - 檢查三個文件的修改時間
  - 返回最新修改的文件名

### 代理配置
每個代理定義了：
- `role` - 角色名稱
- `goal` - 目標
- `backstory` - 背景故事
- `tools` - 可用工具
- `llm` - 使用的語言模型

### 任務配置
每個任務定義了：
- `description` - 任務描述
- `agent` - 負責的代理
- `expected_output` - 預期輸出

## 擴展建議

### 添加新代理：
```python
new_agent = Agent(
    role="角色名稱",
    goal="目標描述",
    backstory="背景故事",
    tools=[],
    llm=llm,
    verbose=True
)
```

### 添加新工具：
```python
@tool
def new_tool(param: str) -> str:
    """工具說明"""
    return "結果"
```

### 添加新任務：
```python
new_task = Task(
    description="任務描述",
    agent=assigned_agent,
    expected_output="預期輸出"
)
```

### 修改執行流程：
在 `run_crew()` 中修改 `Crew()` 的參數：
- `agents` - 參與的代理列表
- `tasks` - 執行的任務列表（按順序）

## 配置說明

### 模型配置
- 默認使用 `claude-haiku-4-5`（Claude Haiku 4.5 - 最新）
  - 速度比 Sonnet 4.5 快 4-5 倍
  - 成本僅需 1/3
  - 性能達到 Sonnet 4.5 的 90%
- 可在 `ChatAnthropic` 初始化時修改 `model_name`
- `temperature` 控制創意度（0-1，較低更確定性）
- 其他可用模型：`claude-opus-4-5`、`claude-sonnet-4-5`

### 執行控制
- `verbose=True` - 顯示詳細執行日誌
- `max_iter` - 每個任務的最大迭代次數

## 下一步

1. **編輯清單** - 修改 `anime_list.json` 來改變推薦的動漫清單
2. **改進維基百科爬取** - 優化 `search_wikipedia_anime()` 以獲取更精準的數據
3. **添加其他推薦來源** - 從 MyAnimeList、IMDb 等網站獲取數據
4. **保存推薦結果** - 將推薦結果存儲到數據庫或文件
5. **構建UI** - 使用 Streamlit 或 Flask 添加前端界面

## 故障排除

### 找不到 anime_list.json
```
解決方案：
1. 確保 anime_list.json 文件存在於項目根目錄
2. 檢查文件名是否正確（區分大小寫）
3. 如果文件丟失，程式會提示創建新文件
```

### 清單文件格式錯誤
```
解決方案：
1. 檢查文件格式是否正確
   - JSON：使用線上 JSON 驗證工具檢查語法
   - 純文本：確保每行一部動漫，無空行
   - CSV：確保第一欄是動漫名稱
2. 確保文件是 UTF-8 編碼
3. 檢查文件副檔名是否正確 (.json, .txt, .csv)
```

### 缺少 ANTHROPIC_API_KEY
```
解決方案：export ANTHROPIC_API_KEY='your-key-here'
```

### 模塊導入錯誤
```
解決方案：確保所有依賴已安裝：pip install -r requirements.txt
```

### API 連接錯誤
```
解決方案：
1. 檢查 ANTHROPIC_API_KEY 是否設置正確
2. 確認網絡連接是否正常
3. 訪問 https://console.anthropic.com 驗證 API 密鑰有效性
```

### 維基百科查詢失敗
```
如果維基百科查詢失敗，程式會直接中止並顯示錯誤信息：
- HTTP 錯誤：連線失敗
- 逾時：網絡連接過慢
- 提取失敗：無法找到動漫資訊

解決方案：
1. 檢查網絡連接是否正常
2. 檢查 URL 是否正確
3. 確認維基百科是否在線
4. 重新執行程式
```

## 許可證

MIT

## 聯繫方式

有問題或建議？歡迎反饋！
