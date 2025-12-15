#!/usr/bin/env python3
"""
CrewAI MVP: 動漫介紹與推薦系統
這個示例展示了多個代理如何協作完成複雜任務
"""

import os
from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic

# ==================== 自定義工具 ====================

@tool
def search_anime_info(anime_name: str) -> str:
    """搜索動漫的詳細信息"""
    # 在實際應用中，這裡可以連接真實的API（如MyAnimeList、AniDB等）
    anime_data = {
        "進擊的巨人": "日本漫畫改編，2013年開始連載。故事背景在被巨人圍困的世界，主角艾倫決心消滅所有巨人。評分8.5/10，共4季。",
        "咒術回戰": "2018年漫畫開始連載，2020年動畫化。講述少年虎杖悠仁與詛咒對抗的故事。評分8.7/10，是當前最受歡迎的動漫之一。",
        "死亡筆記": "經典懸疑動漫，2006年播出。主角撿到死亡筆記，與一位天才偵探L展開博弈。評分9.0/10，共37集。",
        "鬼滅之刃": "2019年動畫化，2020年推出劇場版。故事講述少年炭治郎為拯救妹妹而加入鬼殺隊。評分8.8/10，極高人氣。"
    }
    return anime_data.get(anime_name, f"關於{anime_name}的信息：這是一部受歡迎的日本動漫作品，故事精彩，值得觀看。")

@tool
def generate_recommendation(anime_name: str, style: str) -> str:
    """生成指定風格的推薦文章"""
    styles = {
        "劇情分析": f"## {anime_name}劇情深度解析\n\n{anime_name}以其精巧的故事結構而聞名。劇情發展層層遞進，人物塑造深邃而複雜...",
        "觀影指南": f"## {anime_name}新手觀影指南\n\n如果您是第一次觀看{anime_name}，本指南將幫助您快速上手。首先應該了解背景設定...",
        "推薦理由": f"## 為什麼要看{anime_name}\n\n{anime_name}是一部不容錯過的傑作。它兼具視覺震撼和情感深度，能夠引發觀眾的思考..."
    }
    return styles.get(style, f"關於{anime_name}的{style}推薦文章")

# ==================== 設置LLM ====================

llm = ChatAnthropic(
    model_name="claude-haiku-4-5",
    temperature=0.7,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# ==================== 定義代理 ====================

# 代理1: 動漫評論家
anime_critic = Agent(
    role="動漫評論家",
    goal="深入分析動漫作品，提供專業的評論和洞察",
    backstory="資深動漫愛好者，擁有15年動漫觀看和評論經驗，熟悉各類型動漫的優缺點",
    tools=[search_anime_info],
    llm=llm,
    verbose=True
)

# 代理2: 推薦策略專家
recommendation_specialist = Agent(
    role="推薦策略專家",
    goal="根據動漫特點制定推薦策略，匹配不同類型的觀眾",
    backstory="內容營銷和推薦系統專家，擅長為不同受眾群體制定針對性的推薦計劃",
    tools=[],
    llm=llm,
    verbose=True
)

# 代理3: 內容創作者
content_creator = Agent(
    role="文案創作者",
    goal="生成高質量、引人入勝的動漫推薦文章",
    backstory="資深文案寫手，擅長用各種風格創作引人入勝的內容，曾為多家動漫網站和平台創作推薦文章",
    tools=[generate_recommendation],
    llm=llm,
    verbose=True
)

# ==================== 定義任務 ====================

# 任務1: 動漫分析
task_analysis = Task(
    description="對動漫 {topic} 進行深入的分析和評論：\n請提供劇情概述、角色評價、視覺風格、評分和推薦指數",
    agent=anime_critic,
    expected_output="詳細的動漫分析報告，包括劇情、角色、畫風和整體評價"
)

# 任務2: 推薦策略
task_strategy = Task(
    description="基於動漫分析結果，為 {topic} 制定推薦策略\n請考慮目標觀眾、最佳觀影順序和推薦重點",
    agent=recommendation_specialist,
    expected_output="完整的推薦策略文檔，包括受眾分析和推薦重點"
)

# 任務3: 推薦文章生成
task_content = Task(
    description="根據推薦策略，為 {topic} 生成3個不同風格的推薦文章\n風格包括：劇情分析、觀影指南、推薦理由",
    agent=content_creator,
    expected_output="3篇高質量的推薦文章，每篇風格不同"
)

# ==================== 創建團隊並執行 ====================

def run_crew(topic: str):
    """運行CrewAI團隊"""
    print(f"\n{'='*60}")
    print(f"開始為您分析動漫: {topic}")
    print(f"{'='*60}\n")

    # 創建團隊，定義任務順序
    crew = Crew(
        agents=[anime_critic, recommendation_specialist, content_creator],
        tasks=[task_analysis, task_strategy, task_content],
        verbose=True,
        max_iter=3  # 每個任務的最大迭代次數
    )

    # 執行流程
    result = crew.kickoff(inputs={"topic": topic})

    print(f"\n{'='*60}")
    print("推薦結果:")
    print(f"{'='*60}")
    print(result)

    return result

# ==================== 主程序 ====================

if __name__ == "__main__":
    # 檢查API密鑰
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("警告: 未設置 ANTHROPIC_API_KEY 環境變量")
        print("請設置: export ANTHROPIC_API_KEY='your-key-here'")
        print("\n將使用本地模擬模式運行...")

    # 運行示例 - 分析經典動漫
    topic = "鬼滅之刃"
    run_crew(topic)
