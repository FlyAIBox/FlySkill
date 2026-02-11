# FlySkill 常见问题解答 (FAQ)

本文档回答了使用 FlySkill 过程中的常见问题。

## 📋 目录

- [基础概念](#基础概念)
- [安装和配置](#安装和配置)
- [使用问题](#使用问题)
- [创建 Skill](#创建-skill)
- [故障排除](#故障排除)
- [高级话题](#高级话题)

---

## 基础概念

### Q1: Agent Skill 和传统 Prompt 有什么区别？

**传统 Prompt（"临时工"模式）：**
- 每次使用都需要重新输入或复制粘贴
- 质量依赖于用户的 Prompt 编写能力
- 不同人使用会有不同结果
- 难以维护和更新
- 知识分散，无法积累

**Agent Skill（"专业技能"模式）：**
- 一次创建，永久可用
- 标准化的工作流程和输出
- 所有人使用都能得到一致的结果
- 集中维护，版本控制
- 知识沉淀为团队资产

**类比**：
- Prompt 就像每次都手写食谱
- Skill 就像把食谱编成标准化的烹饪程序

### Q2: Skill 适合什么样的场景？

**✅ 适合的场景：**
1. **高频重复的任务**
   - 每周的数据分析
   - 定期的代码审查
   - 常规的报告生成

2. **有明确标准的工作**
   - 营销数据分析（有固定的计算公式）
   - 代码规范检查（有编码标准）
   - 文档格式化（有模板要求）

3. **容易出错的任务**
   - 复杂的计算（如 ROAS、CPA）
   - 多步骤的流程（容易遗漏）
   - 需要记住很多规则的工作

4. **需要团队统一的流程**
   - 需求澄清标准
   - 代码提交规范
   - 文档编写格式

**❌ 不适合的场景：**
1. 一次性的临时任务
2. 极度灵活、无固定模式的创造性工作
3. 过于简单、无需指导的任务
4. 高度依赖上下文的任务

### Q3: 使用 Skill 需要付费吗？

FlySkill 本身是**完全免费和开源**的（MIT 许可证）。

但是，你需要：
- 一个支持 Skill 的 AI Agent 框架（如 Claude Code）
- AI 服务的使用费用（如 Claude API 的 Token 费用）

**好消息**：使用 Skill 后，由于提示词更短、交互轮次更少，实际上会**减少 Token 消耗**，降低成本。

### Q4: Skill 会自动触发吗？还是需要手动调用？

**自动触发**。

Skill 会在 Agent 启动时加载，当你的请求符合 Skill 的触发条件时，它会自动生效。

**示例：**
```
你说："在设置页面加一个夜间模式开关"

Agent 检测到需求模糊（触发 clarify-demand-uncertainty Skill）

Agent 自动提出澄清问题（而不是直接开始编码）
```

你不需要说："请使用 XXX Skill"。Agent 会智能判断何时使用哪个 Skill。

---

## 安装和配置

### Q5: 如何安装 FlySkill？

**方式 1：全局安装（适用于所有项目）**
```bash
git clone https://github.com/FlyAlBox/FlySkill.git
mkdir -p ~/.claude/skills
cp -r FlySkill/skills/* ~/.claude/skills/
```

**方式 2：项目安装（仅当前项目）**
```bash
cd your-project
mkdir -p .claude/skills
cp -r /path/to/FlySkill/skills/* .claude/skills/
```

**方式 3：选择性安装（只安装需要的 Skill）**
```bash
# 只安装营销分析 Skill
cp -r FlySkill/skills/analyzing-marketing-campaign ~/.claude/skills/

# 只安装需求澄清 Skill
cp FlySkill/skills/clarify-demand-uncertainty/SKILL.md ~/.claude/skills/
```

### Q6: 支持哪些 AI Agent 框架？

目前主要针对 **Claude Code** 优化，但理论上支持任何基于提示词的 Agent 框架：

**已测试：**
- ✅ Claude Code（推荐）
- ✅ Claude API

**理论上支持（需要适配路径）：**
- LangChain
- AutoGen
- CrewAI
- 其他自定义 Agent 框架

**适配方法**：
查看你的 Agent 框架的文档，找到"System Prompt"或"Custom Instructions"的加载方式，将 SKILL.md 的内容加载进去即可。

### Q7: 项目 Skill 和全局 Skill 冲突了怎么办？

**加载优先级：**
```
项目 Skill > 全局 Skill
```

如果项目目录（`.claude/skills/`）和全局目录（`~/.claude/skills/`）中有同名 Skill，项目版本会覆盖全局版本。

**建议：**
- 全局：通用的 Skill（如 `clarify-demand-uncertainty`）
- 项目：特定领域的 Skill（如 `analyzing-marketing-campaign`）

### Q8: 如何更新 Skill？

**更新全局 Skill：**
```bash
cd /path/to/FlySkill
git pull
cp -r skills/* ~/.claude/skills/
```

**更新项目 Skill：**
```bash
cd your-project
cp -r /path/to/FlySkill/skills/specific-skill .claude/skills/
git add .claude/skills/specific-skill
git commit -m "Update skill to v1.2.0"
```

**注意**：重大版本更新时，查看 CHANGELOG.md 了解破坏性变更。

---

## 使用问题

### Q9: 为什么 Skill 没有触发？

**可能的原因和解决方法：**

1. **Skill 文件路径不正确**
   ```bash
   # 检查文件是否存在
   ls -la .claude/skills/
   ls -la ~/.claude/skills/
   ```

2. **Skill 文件格式错误**
   - 确保文件是 `.md` 格式
   - 确保包含正确的 YAML front matter：
     ```yaml
     ---
     name: skill-name
     description: 描述
     ---
     ```

3. **触发条件不匹配**
   - 你的请求可能不符合 Skill 的触发条件
   - 试试更明确地描述你的需求

4. **Agent 需要重启**
   - 某些 Agent 框架需要重启才能加载新 Skill
   - 重启 Claude Code 或重新加载配置

5. **Agent 选择了不使用 Skill**
   - Agent 判断当前场景不适合使用 Skill
   - 这是正常的，不是所有请求都需要 Skill

### Q10: 如何知道 Skill 是否已经生效？

**测试方法：**

**测试 `clarify-demand-uncertainty`：**
```
输入："在设置页面加一个开关"

预期：Agent 会先提问（开关的具体功能、位置、样式等）而不是直接写代码

如果直接开始写代码 → Skill 未生效
如果先提问 → Skill 已生效 ✅
```

**测试 `analyzing-marketing-campaign`：**
```
输入：上传营销数据 CSV，说"请分析这个数据"

预期：Agent 会执行完整的分析流程（数据质量检查、漏斗分析、效率分析、预算建议）

如果只是简单总结 → Skill 未生效
如果执行标准化分析流程 → Skill 已生效 ✅
```

### Q11: Skill 的输出可以自定义吗？

**可以部分自定义。**

你可以在提示词中添加额外要求：

```
我上传了本周的营销活动数据。请分析数据，帮助我了解各渠道的表现情况。

额外要求：
- 请以图表形式展示趋势
- 重点关注抖音和小程序渠道
- 提供 Top 3 优化建议
```

Skill 会执行标准流程，同时满足你的额外要求。

**如果需要深度自定义**：
- 复制 Skill 文件到你的项目目录
- 修改 SKILL.md 的内容
- 保存后 Agent 会使用你的自定义版本

### Q12: 多个 Skill 会不会冲突？

**不会冲突。**

Agent 会智能判断使用哪个（些）Skill：

1. **单个 Skill 场景**：
   ```
   用户："写一个登录接口"
   → 触发 clarify-demand-uncertainty（需求不明确）
   ```

2. **多个 Skill 协同**：
   ```
   用户："分析营销数据并优化策略"
   → 先触发 clarify-demand-uncertainty（澄清优化目标）
   → 再触发 analyzing-marketing-campaign（执行分析）
   ```

3. **不触发任何 Skill**：
   ```
   用户："帮我把这个文件里的所有 TODO 改成 FIXME"
   → 明确的指令，无需 Skill 辅助
   ```

### Q13: Skill 的执行速度会比传统方式慢吗？

**实际上更快。**

虽然 Skill 会执行标准化的流程，但因为：
1. **减少交互轮次**：1 轮 vs 3-5 轮
2. **减少 Token**：80 字 vs 650 字
3. **无需等待用户输入**：Agent 知道所有步骤

**实测对比（营销分析案例）：**
- 传统方式：15 分钟（3 轮对话 + 用户思考和输入时间）
- Skill 方式：3 分钟（1 轮对话）

**提速 80%！**

---

## 创建 Skill

### Q14: 我没有编程经验，可以创建 Skill 吗？

**可以！**

创建 Skill 不需要编程经验。你只需要：
1. 清楚描述你的工作流程
2. 会使用 Markdown 格式（很简单）
3. 能用自然语言表达逻辑

**推荐方式：使用 skill-creator**

```bash
# 安装 skill-creator
cp skills/skill-creator/SKILL.md .claude/skills/

# 告诉 Agent
"我想创建一个 Skill，用于 [你的场景]。请使用 skill-creator 引导我。"

# Agent 会引导你回答 4 个问题，然后自动生成 SKILL.md
```

10 分钟即可创建第一个 Skill！

### Q15: Skill 可以包含代码吗？

**可以。**

有两种方式：

**方式 1：在 SKILL.md 中包含代码示例**
```markdown
## 计算 CTR 的标准方式

```python
def calculate_ctr(clicks, impressions):
    """点击率 = 点击次数 / 展示次数 × 100"""
    if impressions == 0:
        return 0
    return (clicks / impressions) * 100
```
```

**方式 2：创建独立的脚本文件**
```
skills/your-skill/
├── SKILL.md
└── scripts/
    └── calculate.py
```

在 SKILL.md 中引用：
```markdown
## 工作流程

### 步骤 2：执行计算
使用 `scripts/calculate.py` 执行标准化计算。
```

**建议**：
- 简单逻辑：直接写在 SKILL.md 中
- 复杂计算：使用独立脚本文件

### Q16: 如何测试我创建的 Skill？

**测试清单：**

**1. 触发准确性测试**

创建测试用例表格：

| 测试用例 | 预期结果 | 实际结果 | 通过? |
|---------|---------|---------|-------|
| "写一个登录接口"（模糊） | 应该触发 | ✅ 触发了 | ✅ |
| "在 auth.py 第 25 行添加 login 函数"（明确） | 不应该触发 | ✅ 没触发 | ✅ |

**2. 工作流完整性测试**

- [ ] 是否执行了所有必要的步骤？
- [ ] 是否在正确的时机暂停等待用户输入？
- [ ] 是否提供了清晰的输出？

**3. 边界情况测试**

- 缺失数据如何处理？
- 异常输入如何处理？
- 极端情况如何处理？

**4. 真实场景测试**

在实际工作中使用 Skill，观察是否达到预期效果。

### Q17: 可以修改现有的 Skill 吗？

**可以。**

**方式 1：Fork 后修改（推荐）**
```bash
# 复制到项目目录
cp skills/existing-skill/SKILL.md .claude/skills/existing-skill-custom.md

# 修改文件名和内容
# 你的自定义版本会与原版共存
```

**方式 2：直接修改（全局影响）**
```bash
# 修改全局 Skill
vim ~/.claude/skills/existing-skill/SKILL.md

# 或修改项目 Skill
vim .claude/skills/existing-skill/SKILL.md
```

**建议：**
- 如果是团队共用的 Skill，提交 PR 到主仓库
- 如果是个人特定需求，创建自定义版本

---

## 故障排除

### Q18: Agent 说"我不知道如何执行这个 Skill"

**可能原因：**

1. **Skill 描述不够清晰**
   - 检查 SKILL.md 的"工作流程"部分
   - 确保每个步骤都有明确的说明

2. **Skill 依赖的工具或脚本不存在**
   - 检查 scripts/ 目录是否完整
   - 确保脚本文件有执行权限

3. **Skill 引用了外部资源**
   - 检查 references/ 目录是否完整
   - 确保引用的文件路径正确

**解决方法：**
```bash
# 检查 Skill 目录结构
tree .claude/skills/your-skill/

# 应该包含所有必要文件
your-skill/
├── SKILL.md
├── scripts/          # 如果有脚本
└── references/       # 如果有参考文档
```

### Q19: Skill 的输出结果不准确

**可能原因：**

1. **输入数据格式不符合要求**
   - 检查 SKILL.md 的"输入要求"部分
   - 确保你的数据符合格式要求

2. **基准值或规则过时**
   - 检查 Skill 中的基准值是否需要更新
   - 修改 SKILL.md 或 references/ 中的规则文件

3. **Skill 逻辑有 bug**
   - 检查 SKILL.md 的工作流程
   - 测试边界情况
   - 提交 Issue 报告 bug

**示例：更新基准值**
```markdown
<!-- 修改 SKILL.md -->

## 历史基准值

<!-- 旧值 -->
| 微信广告 | 2.5% | 4.0% |

<!-- 新值 -->
| 微信广告 | 2.8% | 4.2% |  # 更新为 2024 Q1 数据
```

### Q20: Agent 一直重复执行同一个 Skill

**可能原因：**

1. **触发条件过于宽泛**
   - Skill 的"何时使用"条件太宽泛
   - 导致不该触发时也触发了

2. **工作流程没有明确的结束条件**
   - Skill 没有说明何时算"完成"
   - Agent 不确定是否已经完成任务

**解决方法：**

**修改触发条件：**
```markdown
<!-- 过于宽泛 -->
## 何时使用
当用户上传文件时使用

<!-- 更具体 -->
## 何时使用
当用户上传营销数据 CSV 文件，并请求分析 CTR、CVR 等指标时使用
```

**添加结束条件：**
```markdown
## 工作流程

### 最后一步：输出结果
生成完整的分析报告后，Skill 执行完成。
不要重复执行分析，除非用户明确要求重新分析。
```

---

## 高级话题

### Q21: 可以在 Skill 中调用外部 API 吗？

**可以，但需要注意安全性。**

**示例：调用天气 API**
```markdown
## 工作流程

### 步骤 1：获取天气数据
使用以下 Python 代码调用天气 API：

```python
import requests

def get_weather(city):
    api_key = os.getenv('WEATHER_API_KEY')  # 从环境变量读取
    url = f"https://api.weather.com/v3/wx/forecast/daily/5day"
    params = {'city': city, 'apiKey': api_key}
    response = requests.get(url, params=params)
    return response.json()
```
```

**安全建议：**
- 不要在 SKILL.md 中硬编码 API 密钥
- 使用环境变量或配置文件
- 注意 API 的调用频率限制

### Q22: Skill 可以访问数据库吗？

**可以，但要谨慎。**

**示例：查询历史基准值**
```markdown
## 工作流程

### 步骤 1：获取基准值
从数据库中查询最新的行业基准值：

```python
import sqlite3

def get_benchmarks():
    conn = sqlite3.connect('benchmarks.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT channel, ctr_benchmark, cvr_benchmark
        FROM industry_benchmarks
        WHERE date = (SELECT MAX(date) FROM industry_benchmarks)
    """)
    return cursor.fetchall()
```
```

**安全建议：**
- 使用只读账号
- 避免在 Skill 中执行 UPDATE/DELETE 操作
- 验证所有输入，防止 SQL 注入

### Q23: 如何实现多语言 Skill？

**方式 1：创建多个版本**
```
skills/
├── analyzing-marketing-campaign/
│   └── SKILL.md                    # 英文版
└── analyzing-marketing-campaign-zh/
    └── SKILL.md                    # 中文版
```

**方式 2：在同一个 Skill 中支持多语言**
```markdown
---
name: analyzing-marketing-campaign
description: Analyze marketing campaign data (支持中英文)
---

# Marketing Campaign Analysis / 营销活动分析

## When to Use / 何时使用

When analyzing multi-channel marketing data...
当分析多渠道营销数据时...

## Input Requirements / 输入要求

Supported column names (支持的列名):
- English: date, channel, impressions, clicks, conversions
- Chinese: 日期, 渠道, 展示次数, 点击次数, 转化次数
```

**方式 3：使用变量（更高级）**
```markdown
## 语言设置

用户可以指定输出语言：
- `language: en` - English output
- `language: zh` - 中文输出
- `language: auto` - 自动检测（默认）
```

### Q24: Skill 可以调用其他 Skill 吗？

**可以，通过工作流程编排。**

**示例：组合多个 Skill**
```markdown
---
name: complete-analysis-workflow
description: 完整的分析工作流（组合多个 Skill）
---

# 完整分析工作流

## 工作流程

### 1. 澄清需求
首先使用 `clarify-demand-uncertainty` Skill 确认：
- 分析目标
- 关注指标
- 约束条件

### 2. 执行分析
根据数据类型选择合适的分析 Skill：
- 营销数据 → `analyzing-marketing-campaign`
- 财务数据 → `financial-analysis`
- 用户行为数据 → `user-behavior-analysis`

### 3. 生成报告
使用 `report-generator` Skill 生成标准化报告。
```

**注意**：
- Skill 编排增加了复杂性
- 确保各个 Skill 的 I/O 兼容
- 适合高级用户

### Q25: 如何分享我的 Skill 给其他人？

**方式 1：提交到 FlySkill 仓库（公开分享）**
```bash
# Fork 仓库
# 添加你的 Skill
# 提交 Pull Request
```

**方式 2：创建自己的 Skill 仓库**
```bash
# 创建新仓库
mkdir my-skills
cd my-skills
git init

# 添加你的 Skill
cp -r /path/to/your/skill skills/

# 提交和推送
git add .
git commit -m "Add my awesome skill"
git push
```

**方式 3：导出为单个文件（快速分享）**
```bash
# 打包 Skill
tar -czf my-skill.tar.gz skills/my-skill/

# 分享 my-skill.tar.gz 文件给其他人
# 他们可以解压到 .claude/skills/ 目录使用
```

---

## 还有问题？

- 📖 查看 [快速入门指南](QUICK_START.md)
- 📚 阅读 [最佳实践](BEST_PRACTICES.md)
- 🎓 学习 [创建 Skill 教程](CREATE_YOUR_SKILL.md)
- 💬 提交 [Issue](https://github.com/FlyAlBox/FlySkill/issues)
- 👥 加入讨论社区

---

**如果本 FAQ 没有回答你的问题，欢迎提交 Issue，我们会持续更新！**

