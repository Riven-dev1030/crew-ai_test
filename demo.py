#!/usr/bin/env python3
"""
CrewAI MVP 演示版本 - 動漫介紹與推薦系統
無需任何 API，即刻體驗 CrewAI 的核心概念和流程
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
        if "評論家" in agent.role:
            return self._anime_analysis_response(topic)
        elif "推薦策略" in agent.role:
            return self._recommendation_strategy_response(topic)
        elif "文案創作" in agent.role or "創作者" in agent.role:
            return self._content_creation_response(topic)
        else:
            return f"{agent.role} 已處理關於 '{topic}' 的任務"

    def _anime_analysis_response(self, topic: str) -> str:
        """動漫分析回應"""
        return f"""
## {topic} 詳細分析報告

### 基本信息
- 原著：日本漫畫
- 動畫化年份：2019-2024
- 總季數：多季 + 劇場版
- 總體評分：8.8/10

### 故事背景
{topic} 設定在鬼怪橫行的世界。故事主角為來自貧困鄉村的少年，為了拯救被鬼怪詛咒的妹妹，決心加入鬼殺隊，踏上成為強者的道路。

### 角色評價
✨ **主角群**：人物塑造深入，成長弧線完整
✨ **反派角色**：每個反派都有獨特的動機和故事
✨ **配角設定**：充滿個性，互動精彩

### 視覺藝術評價
🎨 **畫風**：獨特的水彩風格，視覺效果震撼
🎨 **戰鬥場景**：極具動感，特效精良
🎨 **人物表情**：細節豐富，情感表達生動

### 核心主題
📖 友誼與羈絆
📖 堅持與夢想
📖 人性與救贖

### 推薦指數：⭐⭐⭐⭐⭐
必看經典作品，強烈推薦所有動漫愛好者觀看！
"""

    def _recommendation_strategy_response(self, topic: str) -> str:
        """推薦策略回應"""
        return f"""
## {topic} 推薦策略方案

### 目標觀眾分析
1. **核心觀眾**：動漫愛好者和日本文化迷
   - 年齡：16-35 歲
   - 特點：追求劇情深度和視覺美感

2. **潛在觀眾**：普通電視劇愛好者
   - 年齡：18-50 歲
   - 需求：精彩故事和情感代入

3. **新手觀眾**：首次接觸動漫的人
   - 年齡：所有年齡段
   - 需求：入門友好的推薦

### 推薦重點
✅ **視覺衝擊** - 突出電影級別的畫風和特效
✅ **情感代入** - 強調人物深度塑造和人性探討
✅ **故事品質** - 展示完整的劇情弧線和伏筆設計
✅ **文化獨特性** - 介紹日本文化和傳統元素

### 推薦渠道
- 動漫評測網站和平台
- 短視頻平台（抖音、B站等）
- 社交媒體話題和討論
- 流媒體平台推薦榜單

### 最佳觀影路徑
1️⃣ 第一季 - 建立世界觀和角色認同
2️⃣ 第二季 - 深化故事和人物發展
3️⃣ 劇場版 - 體驗電影級視覺盛宴
4️⃣ 後續季數 - 完整體驗完整故事

### 預期效果
🎬 觀眾滿意度：95%+
🎬 推薦轉化率：80%+
🎬 社交媒體熱度：持續增長
"""

    def _content_creation_response(self, topic: str) -> str:
        """推薦文章創作回應"""
        return f"""
## {topic} 推薦文章集錦

---

### 文章 1：劇情深度分析
# {topic} 劇情深度解析：探尋人性的光芒

{topic} 以其精巧的故事結構和深邃的人性探討而聞名。劇情發展層層遞進，在充滿戰鬥的場景中穿插著溫暖的人物互動。

**劇情核心支柱：**
- 主角的成長蛻變
- 家族與羈絆的主題
- 善惡對立的複雜性

**值得深思的要點：**
1. 人物如何在絕望中尋找希望
2. 不同角色立場的碰撞與理解
3. 故事如何呈現日本傳統與現代的融合

🎬 **推薦度**：★★★★★ 必看經典！

---

### 文章 2：新手觀影完全指南
# {topic} 新手入門觀影指南

如果您是第一次接觸 {topic}，本指南將幫助您快速上手，獲得最佳觀影體驗。

**觀看前需要了解的：**
- 故事背景設定
- 主要角色介紹
- 世界觀基礎知識

**最佳觀看方式：**
1. 字幕 vs 配音選擇建議
2. 推薦的觀看順序
3. 如何理解日本文化元素

**常見疑問解答：**
- 故事節奏如何？（不拖沓，高潮迭起）
- 需要漫畫基礎嗎？（不需要，動畫完全獨立）
- 全劇有多長？（約50-60集+劇場版）

🌟 **新手評分**：★★★★★ 十分友好！

---

### 文章 3：為什麼你一定要看這部動漫
# {topic}：一部改變動漫業的傑作

{topic} 不僅是一部優秀的動漫，更是整個動漫產業的里程碑作品。它為何值得您投入時間觀看？

**視覺藝術的革新：**
🎨 水彩風格畫面的大膽嘗試
🎨 戰鬥場景的動感與美感結合
🎨 細節刻畫的精緻程度

**情感價值的呈現：**
❤️ 兄妹之情的感人刻畫
❤️ 友誼與信任的重要性
❤️ 為他人而戰的高尚品質

**文化影響力：**
🌏 帶動日本傳統文化的全球認知
🌏 掀起新一代動漫浪潮
🌏 創造社會文化現象

**總體推薦**：⭐⭐⭐⭐⭐ 不容錯過的傑作！
"""


# ==================== 定義代理 ====================

anime_critic = Agent(
    role="動漫評論家",
    goal="深入分析動漫作品，提供專業的評論和洞察",
    backstory="資深動漫愛好者，擁有 15 年動漫觀看和評論經驗，熟悉各類型動漫的優缺點",
    tools=["動漫數據庫查詢", "評分系統分析"]
)

recommendation_specialist = Agent(
    role="推薦策略專家",
    goal="根據動漫特點制定推薦策略，匹配不同類型的觀眾",
    backstory="內容營銷和推薦系統專家，擅長為不同受眾群體制定針對性的推薦計劃",
    tools=["受眾分析", "渠道規劃"]
)

content_creator = Agent(
    role="文案創作者",
    goal="生成高質量、引人入勝的動漫推薦文章",
    backstory="資深文案寫手，擅長用各種風格創作引人入勝的內容，曾為多家動漫網站和平台創作推薦文章",
    tools=["內容生成", "風格轉換"]
)

# ==================== 定義任務 ====================

task_analysis = Task(
    description="對動漫 {topic} 進行深入的分析和評論：\n請提供劇情概述、角色評價、視覺風格、評分和推薦指數",
    agent=anime_critic,
    expected_output="詳細的動漫分析報告"
)

task_strategy = Task(
    description="基於動漫分析結果，為 {topic} 制定推薦策略\n請考慮目標觀眾、最佳觀影順序和推薦重點",
    agent=recommendation_specialist,
    expected_output="完整的推薦策略文檔"
)

task_content = Task(
    description="根據推薦策略，為 {topic} 生成 3 個不同風格的推薦文章\n風格包括：劇情分析、觀影指南、推薦理由",
    agent=content_creator,
    expected_output="3 篇高質量的推薦文章"
)


# ==================== 主程序 ====================

def run_demo(topic: str):
    """運行演示"""
    print(f"\n{'#'*70}")
    print(f"# CrewAI 演示版本：動漫介紹與推薦系統")
    print(f"# 分析動漫：{topic}")
    print(f"{'#'*70}")

    # 創建團隊
    crew = SimplifiedCrew(
        agents=[anime_critic, recommendation_specialist, content_creator],
        tasks=[task_analysis, task_strategy, task_content]
    )

    # 執行任務
    result = crew.kickoff(inputs={"topic": topic})

    # 顯示最終結果
    print(f"\n{'#'*70}")
    print(f"# 推薦結果")
    print(f"{'#'*70}")

    return result


if __name__ == "__main__":
    topic = "鬼滅之刃"
    run_demo(topic)

    # 可以嘗試其他動漫主題
    # topic = "進擊的巨人"
    # run_demo(topic)

    # topic = "咒術回戰"
    # run_demo(topic)
