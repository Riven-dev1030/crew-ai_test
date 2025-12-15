# CrewAI MVP: 動漫介紹與推薦系統

這是一個完整的 CrewAI 最小可行產品（MVP），展示了多個 Claude AI 代理如何協作完成複雜任務。
使用 Anthropic 的 Claude 大語言模型，建立智能動漫推薦和分析系統。

## 功能概述

### 三個協作代理：
1. **動漫評論家** - 分析動漫作品特點，提供專業評論
2. **推薦策略專家** - 根據動漫特點制定推薦策略
3. **文案創作者** - 生成高質量的推薦文章

### 三個順序執行的任務：
1. 分析動漫 → 2. 制定推薦策略 → 3. 生成推薦文章

## 快速開始

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 配置 Claude API
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

### 3. 運行程序
```bash
python main.py
```

## 項目結構

```
crew-ai_test/
├── main.py                 # 主程序（代理和任務定義）
├── requirements.txt        # 依賴包列表
├── .env.example           # 環境變量示例
└── README.md             # 本文件
```

## 代碼主要組件

### 自定義工具
- `search_anime_info()` - 搜索動漫的詳細信息
- `generate_recommendation()` - 生成指定風格的推薦文章

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
- 默認使用 `claude-3-5-haiku-20241022`（Claude Haiku 3.5）
- 可在 `ChatAnthropic` 初始化時修改 `model_name`
- `temperature` 控制創意度（0-1，較低更確定性）
- 其他可用模型：`claude-3-5-sonnet-20241022`、`claude-opus-4-1-20250805`

### 執行控制
- `verbose=True` - 顯示詳細執行日誌
- `max_iter` - 每個任務的最大迭代次數

## 下一步

1. **自定義主題** - 在 `if __name__ == "__main__"` 中修改 `topic` 變量
2. **連接真實API** - 在自定義工具中添加實際的 API 調用
3. **添加存儲** - 保存結果到數據庫或文件
4. **構建UI** - 使用 Streamlit 或 Flask 添加前端界面

## 故障排除

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

## 許可證

MIT

## 聯繫方式

有問題或建議？歡迎反饋！
