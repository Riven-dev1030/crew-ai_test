#!/usr/bin/env python3
"""
CrewAI MVP 演示版本 - 無需 OpenAI API
展示 CrewAI 的核心概念和流程
"""

from dataclasses import dataclass
from typing import List

# ==================== 數據模型 ====================

@dataclass
class Agent:
    """代理類"""
    role: str
    goal: str
    backstory: str
    tools: List[str] = None

    def __post_init__(self):
        if self.tools is None:
            self.tools = []


@dataclass
class Task:
    """任務類"""
    description: str
    agent: Agent
    expected_output: str


class SimplifiedCrew:
    """簡化的 CrewAI 實現"""

    def __init__(self, agents: List[Agent], tasks: List[Task]):
        self.agents = agents
        self.tasks = tasks

    def kickoff(self, inputs: dict) -> str:
        """執行團隊任務"""
        results = []

        for i, task in enumerate(self.tasks, 1):
            print(f"\n{'='*70}")
            print(f"第 {i} 步: {task.agent.role} 執行任務")
            print(f"{'='*70}")

            # 格式化任務描述
            description = task.description.format(**inputs)
            print(f"\n📋 任務描述:")
            print(f"   {description}\n")

            # 執行任務（模擬）
            result = self._execute_task(task, inputs)

            print(f"\n✅ 任務完成！")
            print(f"\n📊 {task.agent.role} 的結果:")
            print(f"{'-'*70}")
            print(result)
            print(f"{'-'*70}")

            results.append(result)

        return "\n\n".join(results)

    def _execute_task(self, task: Task, inputs: dict) -> str:
        """模擬任務執行"""
        agent = task.agent
        topic = inputs.get("topic", "未知主題")

        # 根據代理角色生成不同的回應
        if "市場研究" in agent.role:
            return self._market_research_response(topic)
        elif "內容策略" in agent.role:
            return self._strategy_response(topic)
        elif "內容創作" in agent.role:
            return self._content_creation_response(topic)
        else:
            return f"{agent.role} 已處理關於 '{topic}' 的任務"

    def _market_research_response(self, topic: str) -> str:
        """市場研究回應"""
        return f"""
## {topic} 市場研究報告

### 市場規模與增長
- 全球市場規模：250億美元
- 年複合增長率（CAGR）：28%
- 預計 2030 年達到 800 億美元

### 主要市場驅動力
1. 企業數字化轉型需求
2. 成本優化壓力
3. 自動化技術成熟

### 競爭格局
- 領導者：3-4 家全球公司
- 中型供應商：約 50 家
- 初創企業：超 500 家

### 關鍵機遇
✨ 垂直行業解決方案
✨ 集成和互操作性
✨ 區域市場拓展

### 主要挑戰
⚠️ 數據隱私和安全
⚠️ 技術集成複雜性
⚠️ 人才短缺
"""

    def _strategy_response(self, topic: str) -> str:
        """內容策略回應"""
        return f"""
## {topic} 內容策略

### 目標受眾分析
1. **主要受眾**：企業決策者和技術領導者
   - 年齡：35-55 歲
   - 角色：CTO、VP 工程、產品經理

2. **次要受眾**：開發者和技術從業者
   - 年齡：25-40 歲
   - 需求：實踐技能和最佳實踐

### 內容支柱
📌 **教育內容** - 入門指南和教程
📌 **深度分析** - 技術洞察和趨勢
📌 **商業案例** - 成功故事和投資回報

### 發佈渠道
- LinkedIn 文章和專業見解
- 技術博客和白皮書
- YouTube 視頻教程
- 播客討論

### 內容日程
- 周一/周三/周五：短文章
- 每月：深度白皮書
- 季度：視頻系列

### 預期成果
🎯 品牌知名度提升 45%
🎯 潛在客戶增加 60%
🎯 行業影響力確立
"""

    def _content_creation_response(self, topic: str) -> str:
        """內容創作回應"""
        return f"""
## {topic} 內容集錦

---

### 內容 1：技術深度分析
# {topic} 技術深度解析

{topic} 代表了當今技術領域的重要發展方向。本文探討其核心機制、應用場景和實現方式。

**核心組件：**
- 分布式架構
- 實時數據處理
- 智能優化算法

**實現要點：**
1. 選擇合適的技術棧
2. 設計可擴展架構
3. 優化性能指標

---

### 內容 2：商業機會分析
# {topic} 商業機會與投資前景

在激烈的市場競爭中，{topic} 為企業創造了多種商業價值。

**商業價值主張：**
- 成本降低 30-50%
- 效率提升 2-3 倍
- 新收入機會

**投資建議：**
✅ 市場前景廣闊
✅ 技術成熟度高
✅ 競爭門檻逐步提高

---

### 內容 3：初學者指南
# {topic} 初學者入門完全指南

如果您是首次接觸 {topic}，本指南將幫助您快速建立基礎知識。

**第一步：理解基礎概念**
- 核心原理
- 主要優勢
- 應用場景

**第二步：動手實踐**
- 環境設置
- 簡單示例
- 調試技巧

**第三步：深入學習**
- 進階主題
- 最佳實踐
- 常見陷阱

**學習資源：**
- 官方文檔
- 開源項目
- 社區論壇
"""


# ==================== 定義代理 ====================

market_researcher = Agent(
    role="市場研究員",
    goal="分析市場趨勢和競爭環境，提供深入的市場洞察",
    backstory="擁有 10 年市場研究經驗，精通數據分析和趨勢預測",
    tools=["市場數據搜索", "競爭分析"]
)

content_strategist = Agent(
    role="內容策略師",
    goal="根據市場洞察制定內容策略，確保內容與目標受眾相符",
    backstory="資深內容營銷專家，擅長制定針對性的內容策略",
    tools=["受眾分析", "渠道規劃"]
)

content_creator = Agent(
    role="內容創作者",
    goal="生成高質量、吸引人的內容，符合策略要求",
    backstory="創意寫手，擁有豐富的多風格內容創作經驗",
    tools=["內容生成", "風格轉換"]
)

# ==================== 定義任務 ====================

task_research = Task(
    description="對以下主題進行深入的市場研究：{topic}\n請提供市場規模、增長率、主要競爭者和機遇",
    agent=market_researcher,
    expected_output="詳細的市場研究報告"
)

task_strategy = Task(
    description="基於市場研究結果，為主題 {topic} 制定內容策略\n請考慮目標受眾、內容類型和發佈渠道",
    agent=content_strategist,
    expected_output="完整的內容策略文檔"
)

task_content = Task(
    description="根據內容策略，為主題 {topic} 生成 3 個不同風格的內容片段",
    agent=content_creator,
    expected_output="3 個高質量的內容片段"
)


# ==================== 主程序 ====================

def run_demo(topic: str):
    """運行演示"""
    print(f"\n{'#'*70}")
    print(f"# CrewAI 演示版本：市場研究與內容生成系統")
    print(f"# 主題：{topic}")
    print(f"{'#'*70}")

    # 創建團隊
    crew = SimplifiedCrew(
        agents=[market_researcher, content_strategist, content_creator],
        tasks=[task_research, task_strategy, task_content]
    )

    # 執行任務
    result = crew.kickoff(inputs={"topic": topic})

    # 顯示最終結果
    print(f"\n{'#'*70}")
    print(f"# 最終結果")
    print(f"{'#'*70}")

    return result


if __name__ == "__main__":
    topic = "AI 助手市場"
    run_demo(topic)

    # 可以嘗試其他主題
    # topic = "區塊鏈技術"
    # run_demo(topic)
