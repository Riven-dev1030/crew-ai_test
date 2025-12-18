#!/usr/bin/env python3
"""
CrewAI MVP: 智能動漫推薦系統
這個示例展示了多個代理如何協作：
- 代理1: 讀取用戶提供的動漫清單並分析品味
- 代理2: 根據用戶品味搜尋並推薦類似動漫
- 代理3: 驗證推薦動漫的存在性和動畫化狀態，生成最終推薦文檔
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
def search_similar_anime(user_taste_summary: str) -> str:
    """根據用戶品味搜尋類似的動漫推薦"""
    print("\n[動漫推薦搜尋] 正在分析用戶品味並搜尋推薦...")
    print(f"[動漫推薦搜尋] 用戶品味: {user_taste_summary[:100]}...")

    # 這個工具會由 LLM 調用，LLM 會基於用戶品味和它的知識庫來推薦動漫
    # 返回提示，讓 LLM 知道應該如何使用它的知識
    return """請根據用戶的動漫品味，推薦 10-15 部類似風格的動漫。

要求：
1. 分析用戶清單中動漫的共同特點（類型、主題、風格）
2. 推薦相似但用戶可能沒看過的動漫
3. 包含不同年代的作品（經典+新番）
4. 列出每部動漫的名稱和簡短推薦理由
5. 優先推薦已完結或正在連載的熱門作品

請以清單格式返回推薦結果。"""

@tool
def verify_anime_info(anime_list: str) -> str:
    """驗證動漫清單中每部作品的存在性和動畫化狀態"""
    print("\n[動漫驗證] 正在驗證推薦清單中的動漫信息...")
    print(f"[動漫驗證] 待驗證清單: {anime_list[:150]}...")

    # 這個工具會由 LLM 調用，LLM 會使用它的知識來驗證動漫信息
    return """請對推薦清單中的每部動漫進行驗證，提供以下信息：

驗證要求：
1. **動漫是否存在**: 確認這是真實存在的動漫作品
2. **動畫化狀態**: 確認是否已經動畫化（TV動畫/劇場版/OVA）
   - 如果只有漫畫/小說，標註「未動畫化」並從推薦中移除
3. **基本信息**: 年份、類型、簡介
4. **評分/人氣**: 大致的評價和人氣程度
5. **觀看建議**: 適合什麼類型的觀眾

請只保留已動畫化的作品，並以結構化格式輸出驗證結果。"""

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

# 代理2: 動漫推薦專家
recommendation_researcher = Agent(
    role="動漫推薦專家",
    goal="根據用戶的動漫品味，搜尋並推薦類似風格的優質動漫作品",
    backstory="資深動漫評論家和推薦系統專家，擁有豐富的動漫知識庫，擅長分析用戶品味並提供個性化推薦",
    tools=[search_similar_anime],
    llm=llm,
    verbose=False
)

# 代理3: 動漫資訊驗證專家
anime_verifier = Agent(
    role="動漫資訊驗證專家",
    goal="驗證推薦動漫的存在性和動畫化狀態，生成經過驗證的推薦清單並保存為 Markdown 文件",
    backstory="動漫數據庫專家，精通各類動漫作品信息，能夠快速驗證動漫的存在性、動畫化狀態、評分和人氣，並將結果專業地輸出為文檔",
    tools=[verify_anime_info, save_recommendation_to_file],
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

# 任務2: 基於品味搜尋推薦
task_search_recommendations = Task(
    description="根據用戶清單分析其動漫品味偏好，搜尋並推薦 10-15 部類似風格的動漫作品。\n要求推薦的動漫風格與用戶清單相似，但避免重複用戶已提及的作品。\n包含不同年代的作品（經典+新番），並簡要說明推薦理由。",
    agent=recommendation_researcher,
    expected_output="基於用戶品味的 10-15 部動漫推薦清單，包含推薦理由"
)

# 任務3: 驗證推薦並生成文檔
task_verify_and_save = Task(
    description="驗證推薦清單中每部動漫的存在性和動畫化狀態。\n要求：\n1. 確認動漫是否真實存在\n2. 確認是否已經動畫化（TV/劇場版/OVA）\n3. 移除未動畫化的作品（僅漫畫/小說）\n4. 提供基本信息（年份、類型、評分）\n5. 生成完整的推薦文檔\n\n最後，將驗證後的推薦結果以 Markdown 格式保存到 recommendation.md 文件。",
    agent=anime_verifier,
    expected_output="經過驗證的動漫推薦清單（僅已動畫化作品），包含詳細信息和觀看建議，並已保存為 Markdown 文件"
)

# ==================== 創建團隊並執行 ====================

def run_crew(user_anime_list: str):
    """運行CrewAI推薦系統"""
    print(f"\n{'='*60}")
    print(f"開始動漫推薦流程")
    print(f"{'='*60}\n")

    # 創建團隊，定義任務順序
    crew = Crew(
        agents=[list_reader, recommendation_researcher, anime_verifier],
        tasks=[task_read_list, task_search_recommendations, task_verify_and_save],
        verbose=False,  # 關閉詳細日誌輸出
        max_iter=2  # 每個任務最多重試2次
    )

    # 執行流程
    try:
        print("正在執行推薦任務...")
        print("\n[步驟 1/3] 解析用戶清單，分析品味...")
        print("[步驟 2/3] 基於品味搜尋推薦...")
        print("[步驟 3/3] 驗證動漫信息並生成文檔...")
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
