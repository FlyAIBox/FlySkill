# Agent Skill 驱动的企业 SOP 重构：营销活动分析案例

## 1. 从 Copilot 到 Agent Skill 的范式转变

在企业应用大模型的过程中，我们正在经历从 "Chat Copilot"（对话式副驾驶）向 "Agent Skill"（智能体技能）的转变。
传统的 Copilot 模式依赖于 **Prompt Engineering（提示词工程）**，即用户需要在一个长 Prompt 中详细描述任务背景、逻辑步骤和输出要求。
而 Agent Skill 模式则将核心业务逻辑（SOP）固化为 **Code（代码技能）**，由 Agent 根据意图自动调用。

本文以**“每周营销活动分析与预算调整”**为例，展示如何通过 Agent Skill 重构企业标准作业程序（SOP）。

## 2. 重构前：基于 Prompt 的传统 SOP

在传统模式下，营销分析师使用 LLM 的方式通常是“投喂数据 + 复杂提示词”。

### 2.1 传统工作流
1.  **数据准备**：人工下载 CSV，手动清理异常值。
2.  **编写提示词**：用户需要编写（或复制）一个长达 50 行的 Prompt（如 `material/prompts_initial_conversation_zh.md`），明确定义：
    *   漏斗计算公式 (CTR = Clicks/Impressions)
    *   业务基准 (微信 CTR 目标 2.5%)
    *   预算调整的复杂规则 (ROAS > 4 且 CPA < 50 方可增加预算)
3.  ** LLM 推理**：LLM 像一个“实习生”一样，基于 Prompt 尝试进行计算。
4.  **人工复核**：由于 LLM 的数学计算能力不稳定（幻觉问题），分析师必须人工复核 Excel 结果。

### 2.2 痛点
*   **不稳定**：相同的 Prompt 每次运行可能产生不同格式的结果。
*   **不可靠**：LLM 直接进行数值计算（尤其是除法和复杂逻辑判断）容易出错。
*   **难以维护**：业务逻辑通过自然语言描述，一旦基准值（如 ROAS 目标）变更，需要修改所有人的 Prompt 模板。

## 3. 重构后：Agent Skill 驱动的新 SOP

在 Agent 模式下，我们将 SOP 的核心步骤转化为 **Python 函数技能**。SOP 不再是文档或 Prompt，而是**代码**。

### 3.1 核心技能拆解

#### 技能一：自动化数据清洗与质量质检 (`analyze_campaign.py`)
Agent 不再依赖 LLM “看”数据，而是直接调用 Python 代码读取 CSV。
*   **代码体现**：
    ```python
    # 自动检测缺失值
    missing_impr = sum(1 for r in parsed_rows if not r.get('展示次数'))
    print(f'缺失值检查: 展示次数 {missing_impr} 个缺失')
    ```
*   **SOP 价值**：强制执行数据质量门槛，不再有人为疏漏。

#### 技能二：标准化的指标计算 (`analyze_campaign.py`)
所有的业务定义（Metric Definition）被封装在代码中，不再依赖 LLM 的“理解”。
*   **代码体现**：
    ```python
    # 固化的业务基准字典
    benchmarks = {
        '微信广告': {'ctr': 2.5, 'cvr': 3.8},
        '百度推广': {'ctr': 5.0, 'cvr': 4.5},
        # ...
    }
    # 确定性的计算逻辑
    ctr = (metrics['clicks'] / metrics['impressions']) * 100
    if ctr >= benchmark_ctr: print('✓ 达标')
    ```
*   **SOP 价值**：确保全公司使用统一的计算口径。

#### 技能三：算法驱动的决策引擎 (`budget_reallocation.py`)
最复杂的预算调整逻辑被转化为确定性的算法，而非自然语言建议。
*   **业务规则代码化**：
    1.  **门槛检查**：转化数 < 50 的渠道自动失去调整资格。
    2.  **分类逻辑**：
        *   `DECREASE_HEAVY` (-45%): ROAS < 目标的一半 且 亏损。
        *   `INCREASE` (+15%): ROAS > 目标 1.15 倍 且 盈利。
    3.  **资金池逻辑**：计算所有减少的预算作为“资金池”，按权重重新分配给优质渠道。
*   **SOP 价值**：将复杂的“经验判断”转化为可复用的“算法资产”。

### 3.2 新的工作流
用户只需简单的意图表达：
> “分析本周数据并建议预算调整。”（参考 `material/prompts_with_skills_zh.md`）

Agent **自主编排**：
1.  调用 `Analyze Data` 技能 -> 产出分析报告。
2.  调用 `Budget Reallocation` 技能 -> 产出具体的金额调整表。

## 4. 效益对比：Code as SOP

| 维度 | 传统 Prompt 模式 | Agent Skill 模式 |
| :--- | :--- | :--- |
| **执行载体** | 自然语言 (Prompt) | Python 代码 (Tools) |
| **准确性** | 低 (LLM 可能算错) | 100% (代码计算) |
| **一致性** | 依赖用户 Prompt 质量 | 强制一致 (代码固化) |
| **可维护性** | 分散 (每个人存自己的 Prompt) | 集中 (统一维护 Git 仓库) |
| **交互体验** | 复杂 (用户需懂业务逻辑) | 简单 (用户只需提需求) |

## 5. 结论

**Agent Skill 是企业 SOP 的数字化终极形态。**

通过将 SOP 重构为 Skill，企业实现了：
1.  **知识资产化**：将“老员工的经验”变成“可执行的代码”。
2.  **决策自动化**：在预算分配等高频场景实现零人工干预的初步筛选。
3.  **交互自然化**：让业务人员用最自然的语言调用最专业的分析能力。

未来的企业 SOP 不再是 PDF 文档，而是一组挂载在 Agent 上的**工具库（Tool Libraries）**。
