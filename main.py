#!/usr/bin/env python3
"""
CrewAI MVP: 動漫推薦系統 (增強版)
這個示例展示了多個代理如何協作：
- 代理1: 讀取用戶提供的動漫清單
- 代理2: 查詢維基百科的年度動漫排名
- 代理3: 根據兩個清單推薦動漫
"""

import os
import json
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import tool
from langchain_anthropic import ChatAnthropic
from bs4 import BeautifulSoup

# 加載 .env 文件
load_dotenv()

# ==================== 自定義工具 ====================

@tool
def read_user_list(json_string: str) -> str:
    """讀取和解析用戶提供的動漫清單 (JSON格式)"""
    try:
        anime_list = json.loads(json_string)
        if isinstance(anime_list, list):
            formatted_list = "\n".join([f"- {anime}" for anime in anime_list])
            return f"成功解析用戶清單，包含以下動漫：\n{formatted_list}"
        else:
            return "錯誤：清單格式不正確，應該是 JSON 陣列"
    except json.JSONDecodeError:
        return f"錯誤：無法解析 JSON。收到的內容：{json_string}"

@tool
def search_wikipedia_anime() -> str:
    """查詢維基百科的年度動漫排名清單（失敗時使用內置數據）"""
    print("\n[維基百科查詢] 正在查詢維基百科...")

    # 內置的熱門動漫數據（降級方案）
    fallback_anime_list = [
        "進擊的巨人", "咒術回戰", "鬼滅之刃", "死亡筆記", "東京喰種",
        "我的英雄學院", "JOJO的奇妙冒險", "Re:從零開始的異世界生活",
        "約定的夢幻島", "86－不存在的戰區－", "SPY×FAMILY間諜家家酒",
        "葬送的芙莉蓮", "電鋸人", "藍色監獄", "無職轉生"
    ]

    try:
        # 查詢維基百科中文版本的動漫列表
        url = "https://zh.wikipedia.org/zh-tw/%E5%90%84%E5%B9%B4%E6%97%A5%E6%9C%AC%E5%8B%95%E7%95%AB%E5%88%97%E8%A1%A8"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

        response = requests.get(url, headers=headers, timeout=5)

        # 查詢失敗直接返回錯誤並停止
        if response.status_code != 200:
            error_msg = f"❌ 維基百科查詢失敗 (HTTP {response.status_code})"
            print(f"[維基百科查詢] {error_msg}")
            print("[維基百科查詢] 工作流將停止執行")
            raise Exception(error_msg)

        soup = BeautifulSoup(response.content, 'html.parser')

        # 提取分類中的動漫標題
        print(f"[維基百科查詢] 正在解析網頁內容...")
        categories = soup.find_all('div', {'class': 'mw-category'})
        print(f"[維基百科查詢] 找到 {len(categories)} 個分類區塊")

        anime_list = []

        for category in categories:
            links = category.find_all('a')
            for link in links[:20]:  # 限制前20個
                title = link.get_text(strip=True)
                if title and not title.startswith('Category'):
                    anime_list.append(title)

        print(f"[維基百科查詢] 總共提取到 {len(anime_list)} 部動漫")

        if not anime_list:
            print("[維基百科查詢] ⚠️  無法從維基百科提取數據")
            print("[維基百科查詢] 使用內置熱門動漫數據作為降級方案")
            anime_list = fallback_anime_list

        formatted_list = "\n".join([f"- {anime}" for anime in anime_list[:15]])
        result = f"從維基百科獲得的年度優質動漫清單：\n{formatted_list}"

        print(f"[維基百科查詢] ✅ 成功抓取 {len(anime_list[:15])} 部動漫")
        print(f"[維基百科查詢] 資料預覽：{', '.join(anime_list[:5])}...")

        return result

    except requests.exceptions.Timeout:
        print("[維基百科查詢] ⚠️  查詢逾時，使用內置數據")
        anime_list = fallback_anime_list
    except requests.exceptions.ConnectionError:
        print("[維基百科查詢] ⚠️  無法連線到維基百科，使用內置數據")
        anime_list = fallback_anime_list
    except requests.exceptions.RequestException as e:
        print(f"[維基百科查詢] ⚠️  網絡錯誤 ({e})，使用內置數據")
        anime_list = fallback_anime_list
    except Exception as e:
        print(f"[維基百科查詢] ⚠️  發生錯誤 ({e})，使用內置數據")
        anime_list = fallback_anime_list

    # 如果執行到這裡，說明使用了 fallback 數據
    if anime_list == fallback_anime_list:
        formatted_list = "\n".join([f"- {anime}" for anime in anime_list])
        result = f"使用內置熱門動漫清單（維基百科不可用）：\n{formatted_list}"

        print(f"[維基百科查詢] ✅ 使用內置數據，包含 {len(anime_list)} 部熱門動漫")
        print(f"[維基百科查詢] 資料預覽：{', '.join(anime_list[:5])}...")

        return result

@tool
def recommend_anime(user_list: str, wiki_list: str) -> str:
    """根據用戶清單和維基百科清單推薦動漫"""
    recommendation = f"""## 動漫推薦結果

### 分析
- **用戶清單**: {user_list}
- **維基百科熱門作品**: {wiki_list}

### 推薦策略
1. **用戶已知作品**: 根據用戶提供的清單，理解其品味偏好
2. **維基熱門作品**: 考慮業界認可的優質動漫
3. **交集推薦**: 優先推薦兩個清單中都出現的作品
4. **補充推薦**: 基於用戶品味，推薦維基百科熱門但用戶未提及的作品

### 推薦清單 (按優先級排序)
1. **頂級推薦**: 在用戶清單和維基百科都有提及的作品
   - 這些作品既符合您的品味，也獲得了廣泛認可

2. **補充推薦**: 維基百科推薦但您未提及的優質作品
   - 基於您現有品味的擴展推薦

3. **發現推薦**: 小眾但高評價的作品
   - 適合尋求新鮮內容的觀眾

### 建議
- 按照推薦順序觀看可以最大化觀影滿意度
- 可根據您的時間和心情調整觀看順序
- 歡迎提供反饋以優化推薦
"""
    return recommendation

@tool
def save_recommendation_to_file(recommendation_content: str, filename: str = "recommendation.md") -> str:
    """將推薦結果保存為 Markdown 文件"""
    try:
        # 獲取當前腳本所在的目錄
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)

        # 確保文件名以 .md 結尾
        if not filename.endswith('.md'):
            filename = filename + '.md'
            file_path = os.path.join(script_dir, filename)

        # 寫入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(recommendation_content)

        return f"✓ 推薦結果已保存到: {filename}"

    except Exception as e:
        return f"❌ 保存文件失敗: {str(e)}"

# ==================== 設置LLM ====================

llm = ChatAnthropic(
    model_name="claude-haiku-4-5",
    temperature=0.7,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# ==================== 定義代理 ====================

# 代理1: 用戶清單解析器
list_reader = Agent(
    role="用戶清單解析器",
    goal="準確讀取和解析用戶提供的動漫清單，理解用戶的品味偏好",
    backstory="資深數據分析師，擅長解析各種格式的數據和信息，能夠準確理解用戶意圖",
    tools=[read_user_list],
    llm=llm,
    verbose=False
)

# 代理2: 維基百科研究員
wiki_researcher = Agent(
    role="維基百科研究員",
    goal="查詢維基百科獲取年度優質動漫排名和業界認可的優秀作品",
    backstory="知識庫管理員，熟悉如何從各大百科全書和數據庫中提取有用信息，了解動漫行業趨勢",
    tools=[search_wikipedia_anime],
    llm=llm,
    verbose=True  # 開啟以便查看查詢進度
)

# 代理3: 動漫推薦引擎
recommender = Agent(
    role="動漫推薦引擎",
    goal="根據用戶清單和業界排名，生成個性化的動漫推薦，並保存結果為 Markdown 文件",
    backstory="資深推薦系統專家，擅長結合多個信息源進行智能推薦，以最大化用戶滿意度，並能將結果專業地輸出為文檔",
    tools=[recommend_anime, save_recommendation_to_file],
    llm=llm,
    verbose=False
)

# ==================== 定義任務 ====================

# 任務1: 解析用戶清單
task_read_list = Task(
    description="讀取和解析用戶提供的動漫清單。用戶清單為：{user_anime_list}\n請確保準確解析清單內容，並提取用戶的動漫品味偏好",
    agent=list_reader,
    expected_output="用戶清單的解析結果和其所反映的品味特徵"
)

# 任務2: 查詢維基百科
task_wiki = Task(
    description="查詢維基百科獲取年度優質動漫排名清單和業界認可的優秀作品。請獲取當前年度最受歡迎和評價最高的動漫作品",
    agent=wiki_researcher,
    expected_output="維基百科提供的優質動漫清單和相關排名信息"
)

# 任務3: 生成推薦並保存
task_recommend = Task(
    description="基於用戶清單和維基百科的優質動漫排名，為用戶生成個性化推薦。\n請分析兩個清單的交集和差異，推薦最適合用戶的動漫作品。\n最後，將推薦結果以 Markdown 格式保存到 recommendation.md 文件。",
    agent=recommender,
    expected_output="個性化的動漫推薦清單，包含推薦理由和觀影建議，並已保存為 Markdown 文件"
)

# ==================== 創建團隊並執行 ====================

def run_crew(user_anime_list: str):
    """運行CrewAI推薦系統"""
    print(f"\n{'='*60}")
    print(f"開始動漫推薦流程")
    print(f"{'='*60}\n")

    # 創建團隊，定義任務順序（優先查詢維基百科）
    crew = Crew(
        agents=[wiki_researcher, list_reader, recommender],
        tasks=[task_wiki, task_read_list, task_recommend],
        verbose=False,  # 關閉詳細日誌輸出
        max_iter=1  # 減少重試次數，失敗快速停止
    )

    # 執行流程
    try:
        print("正在執行推薦任務...")
        print("\n[步驟 1/3] 查詢維基百科... (優先檢查)")
        print("[步驟 2/3] 解析用戶清單...")
        print("[步驟 3/3] 生成推薦並保存...")
        print("\n請稍候，代理正在工作中...\n")
        result = crew.kickoff(inputs={"user_anime_list": user_anime_list})

        print(f"\n{'='*60}")
        print("✅ 推薦完成！結果已保存到 recommendation.md")
        print(f"{'='*60}\n")

        return result

    except Exception as e:
        print(f"\n{'='*60}")
        print("❌ 工作流執行失敗")
        print(f"{'='*60}")
        print(f"\n錯誤原因: {str(e)}")
        print("\n程序已終止。")
        print(f"{'='*60}\n")
        return None

# ==================== 主程序 ====================

def find_latest_anime_list_file():
    """自動偵測最新修改的動漫清單文件"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    supported_files = ["anime_list.json", "anime_list.txt", "anime_list.csv"]

    # 檢查哪些文件存在並獲取其修改時間
    existing_files = {}
    for filename in supported_files:
        file_path = os.path.join(script_dir, filename)
        if os.path.exists(file_path):
            mtime = os.path.getmtime(file_path)
            existing_files[filename] = (file_path, mtime)

    if not existing_files:
        return None

    # 找出最新修改的文件
    latest_file = max(existing_files.items(), key=lambda x: x[1][1])
    return latest_file[0], latest_file[1][0]

def load_anime_list_from_file(filename: str = None) -> str:
    """從外部文件讀取動漫清單，支援多種格式 (JSON、純文本、CSV)

    如果沒有指定文件名，會自動偵測最新修改的清單文件
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # 如果沒有指定文件名，自動偵測最新修改的文件
        if filename is None:
            result = find_latest_anime_list_file()
            if result is None:
                print("錯誤: 找不到任何清單文件")
                print("\n請創建一個清單文件，支援的格式有：")
                print('''
1. JSON 格式 (anime_list.json):
[
  "進擊的巨人",
  "咒術回戰",
  "鬼滅之刃"
]

2. 純文本格式 (anime_list.txt)，每行一部動漫：
進擊的巨人
咒術回戰
鬼滅之刃

3. CSV 格式 (anime_list.csv)：
進擊的巨人
咒術回戰
鬼滅之刃
''')
                return None
            filename, file_path = result
            print(f"✓ 自動偵測到最新清單文件: {filename}")
        else:
            file_path = os.path.join(script_dir, filename)

        if not os.path.exists(file_path):
            print(f"錯誤: 找不到清單文件 '{filename}'")
            print(f"預期位置: {file_path}")
            return None

        # 根據文件副檔名判斷格式
        file_extension = os.path.splitext(filename)[1].lower()
        anime_list = []

        with open(file_path, 'r', encoding='utf-8') as f:
            if file_extension == '.json':
                # JSON 格式
                anime_list = json.load(f)
                if not isinstance(anime_list, list):
                    print(f"錯誤: {filename} 的 JSON 格式不正確，應該是陣列")
                    return None

            elif file_extension == '.txt':
                # 純文本格式，每行一部動漫
                anime_list = [line.strip() for line in f if line.strip()]

            elif file_extension == '.csv':
                # CSV 格式，支援單列或多列（取第一列）
                import csv
                reader = csv.reader(f)
                anime_list = [row[0].strip() for row in reader if row and row[0].strip()]

            else:
                print(f"錯誤: 不支援的文件格式 '{file_extension}'")
                print("支援的格式: .json, .txt, .csv")
                return None

        if not anime_list:
            print(f"錯誤: {filename} 中沒有找到任何動漫")
            return None

        # 轉換為 JSON 字符串供 CrewAI 使用
        json_string = json.dumps(anime_list, ensure_ascii=False)
        print(f"✓ 成功讀取清單 ({file_extension} 格式)，包含 {len(anime_list)} 部動漫")
        return json_string

    except json.JSONDecodeError as e:
        print(f"錯誤: 無法解析 {filename} 的 JSON 格式: {e}")
        return None
    except Exception as e:
        print(f"錯誤: 讀取清單文件失敗: {e}")
        return None

if __name__ == "__main__":
    # 檢查API密鑰
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("警告: 未設置 ANTHROPIC_API_KEY 環境變量")
        print("請設置: export ANTHROPIC_API_KEY='your-key-here'")
        print("\n將使用本地模擬模式運行...")

    # 從外部文件讀取用戶清單（自動偵測最新修改的文件）
    user_anime_list = load_anime_list_from_file()

    if user_anime_list:
        # 運行推薦系統
        run_crew(user_anime_list)
    else:
        print("\n無法加載清單，程式終止。")
