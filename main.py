#!/usr/bin/env python3
"""
CrewAI MVP: 市場研究與內容生成系統
這個示例展示了多個代理如何協作完成複雜任務
"""

import os
from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_openai import ChatOpenAI

# ==================== 自定義工具 ====================

@tool
def search_market_data(topic: str) -> str:
    """搜索市場數據和趨勢信息"""
    # 在實際應用中，這裡可以連接真實的API
    data = {
        "AI助手": "目前市場增長率30%，主要應用在客服和內容生成",
        "軟件開發工具": "DevOps和低代碼平台增長快速，市場規模100億美元",
        "數據分析": "實時分析工具需求量大，市場預期年複合增長率25%"
    }
    return data.get(topic, f"關於{topic}的市場信息：市場持續增長中")

@tool
def generate_content(topic: str, style: str) -> str:
    """生成指定風格的內容"""
    styles = {
        "技術": f"## {topic}技術深度解析\n\n{topic}是當今技術領域的重要方向...",
        "商業": f"## {topic}商業機會分析\n\n在競爭激烈的市場中，{topic}提供了新的商業價值...",
        "教育": f"## {topic}初學者指南\n\n如果您是第一次接觸{topic}，本指南將幫助您快速入門..."
    }
    return styles.get(style, f"關於{topic}的{style}內容")

# ==================== 設置LLM ====================

llm = ChatOpenAI(
    model_name="gpt-4-turbo",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# ==================== 定義代理 ====================

# 代理1: 市場研究員
market_researcher = Agent(
    role="市場研究員",
    goal="分析市場趨勢和競爭環境，提供深入的市場洞察",
    backstory="擁有10年市場研究經驗，精通數據分析和趨勢預測",
    tools=[search_market_data],
    llm=llm,
    verbose=True
)

# 代理2: 內容策略師
content_strategist = Agent(
    role="內容策略師",
    goal="根據市場洞察制定內容策略，確保內容與目標受眾相符",
    backstory="資深內容營銷專家，擅長制定針對性的內容策略",
    tools=[],
    llm=llm,
    verbose=True
)

# 代理3: 內容創作者
content_creator = Agent(
    role="內容創作者",
    goal="生成高質量、吸引人的內容，符合策略要求",
    backstory="創意寫手，擁有豐富的多風格內容創作經驗",
    tools=[generate_content],
    llm=llm,
    verbose=True
)

# ==================== 定義任務 ====================

# 任務1: 市場研究
task_research = Task(
    description="對以下主題進行深入的市場研究：{topic}\n請提供市場規模、增長率、主要競爭者和機遇",
    agent=market_researcher,
    expected_output="詳細的市場研究報告，包括市場規模、增長趨勢和機遇分析"
)

# 任務2: 內容策略
task_strategy = Task(
    description="基於市場研究結果，為主題 {topic} 制定內容策略\n請考慮目標受眾、內容類型和發佈渠道",
    agent=content_strategist,
    expected_output="完整的內容策略文檔，包括受眾分析和內容計劃"
)

# 任務3: 內容生成
task_content = Task(
    description="根據內容策略，為主題 {topic} 生成3個不同風格的內容片段\n風格包括：技術、商業、教育",
    agent=content_creator,
    expected_output="3個高質量的內容片段，每個不同風格"
)

# ==================== 創建團隊並執行 ====================

def run_crew(topic: str):
    """運行CrewAI團隊"""
    print(f"\n{'='*60}")
    print(f"開始處理主題: {topic}")
    print(f"{'='*60}\n")

    # 創建團隊，定義任務順序
    crew = Crew(
        agents=[market_researcher, content_strategist, content_creator],
        tasks=[task_research, task_strategy, task_content],
        verbose=True,
        max_iter=3  # 每個任務的最大迭代次數
    )

    # 執行流程
    result = crew.kickoff(inputs={"topic": topic})

    print(f"\n{'='*60}")
    print("最終結果:")
    print(f"{'='*60}")
    print(result)

    return result

# ==================== 主程序 ====================

if __name__ == "__main__":
    # 檢查API密鑰
    if not os.getenv("OPENAI_API_KEY"):
        print("警告: 未設置 OPENAI_API_KEY 環境變量")
        print("請設置: export OPENAI_API_KEY='your-key-here'")
        print("\n將使用本地模擬模式運行...")

    # 運行示例
    topic = "AI助手市場"
    run_crew(topic)
