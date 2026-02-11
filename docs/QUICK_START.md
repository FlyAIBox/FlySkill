# FlySkill 快速入门指南

本指南将帮助你在 5 分钟内开始使用 Agent Skill。

## 📋 前置条件

- 已安装 Claude Code 或其他支持 Skill 的 AI Agent 框架
- 基本了解如何与 AI Agent 交互

## 🚀 第一个 Skill：营销数据分析

### 步骤 1：安装 Skill（30 秒）

打开终端，执行以下命令：

```bash
# 克隆仓库
git clone https://github.com/FlyAlBox/FlySkill.git
cd FlySkill

# 安装到项目目录（推荐）
mkdir -p .claude/skills
cp -r skills/analyzing-marketing-campaign .claude/skills/

# 或安装到全局目录
# mkdir -p ~/.claude/skills
# cp -r skills/analyzing-marketing-campaign ~/.claude/skills/
```

### 步骤 2：准备测试数据（30 秒）

使用示例数据文件：

```bash
examples/analyzing-marketing-campaign/material/campaign_data_week1_china.csv
```

或准备你自己的营销数据 CSV 文件，确保包含以下列：
- 日期
- 营销活动名称
- 渠道
- 展示次数
- 点击次数
- 转化次数
- 支出
- 收入

### 步骤 3：与 Agent 对话（2 分钟）

在 Claude Code 中，上传数据文件并输入：

```
我上传了本周的营销活动数据。请分析数据，帮助我了解各渠道的表现情况，
以及是否需要重新分配预算。我可以在渠道间调配最多 ¥10,000 的预算，
单个渠道的预算增幅不超过 15%。
```

### 步骤 4：查看分析结果（1 分钟）

Agent 会自动执行完整的分析流程，包括：

1. **数据质量检查报告**
   - 数据完整性
   - 异常值检测
   - 缺失值分析

2. **漏斗绩效分析**
   - CTR（点击率）计算和基准对比
   - CVR（转化率）计算和基准对比
   - 各渠道表现解读

3. **效率绩效分析**
   - ROAS（广告支出回报率）
   - CPA（单次获客成本）
   - 净利润计算

4. **预算重新分配建议**
   - 基于绩效的预算调整方案
   - 符合约束条件的优化建议

## 🎯 对比：使用 Skill 前后

### 传统方式（15 分钟）

**第一轮对话（300 字）：**
```
我上传了我的每周营销活动数据，希望分析其表现。

输入数据：CSV文件包含微信广告、百度推广、抖音广告……

数据质量：检查有无数据缺失或异常情况。

漏斗分析：为每个渠道计算以下两个指标，并与以下历史基准进行比较：
渠道|目标CTR|目标CVR
微信广告|2.5%|4.0%
百度推广|5.0%|5.0%
...

CTR（点击率）= 点击次数/展示次数
CVR（转化率）= 转化次数/点击次数
```

**第二轮对话（250 字）：**
```
效率分析：为每个渠道计算以下额外指标：
- ROAS（广告支出回报率）= 收入/支出
- CPA（单次获客成本）= 支出/转化次数
- 净利润 = 收入 - 总成本

假设：平均单笔订单物流成本为 8 元，产品成本占比为 35%。
```

**第三轮对话（100 字）：**
```
我上传了预算调整的最佳实践参考，请据此建议如何重新分配预算。
我的总调配额度为 1 万元，单个渠道的预算增幅不得超过 15%。
```

**总计：**
- 文字输入：650 字
- 交互轮次：3 轮
- 时间消耗：15 分钟
- 错误风险：高（公式可能写错、基准值可能遗漏）

### 使用 Skill 方式（3 分钟）

**一轮对话（80 字）：**
```
我上传了本周的营销活动数据。请分析数据，帮助我了解各渠道的表现情况，
以及是否需要重新分配预算。我可以在渠道间调配最多 ¥10,000 的预算，
单个渠道的预算增幅不超过 15%。
```

**总计：**
- 文字输入：80 字（减少 87%）
- 交互轮次：1 轮（减少 67%）
- 时间消耗：3 分钟（减少 80%）
- 错误风险：零（标准化计算）

## 🎓 进阶：第二个 Skill

安装需求澄清 Skill：

```bash
cp skills/clarify-demand-uncertainty/SKILL.md .claude/skills/
```

然后试试给 Agent 一个模糊的指令：

```
"在设置页面加一个夜间模式的开关。"
```

观察 Agent 如何主动提出澄清问题，而不是基于假设直接开始编码。

## ✅ 验证安装

检查 Skill 是否正确加载：

1. 启动你的 AI Agent（如 Claude Code）
2. 输入一个模糊的指令，如："写一个登录接口"
3. 如果 Agent 在开始编码前提出澄清问题，说明 `clarify-demand-uncertainty` Skill 已生效
4. 上传营销数据并使用简短提示词，如果 Agent 自动执行完整分析，说明 `analyzing-marketing-campaign` Skill 已生效

## 🔧 故障排除

### Skill 没有触发？

1. **检查路径**：确认 Skill 文件在正确的目录：
   ```bash
   ls -la .claude/skills/
   # 或
   ls -la ~/.claude/skills/
   ```

2. **检查文件格式**：确保 SKILL.md 文件格式正确，包含正确的 YAML front matter：
   ```yaml
   ---
   name: skill-name
   description: 描述
   ---
   ```

3. **重启 Agent**：某些 Agent 框架需要重启才能加载新的 Skill

4. **查看日志**：检查 Agent 的日志输出，看是否有加载错误

### 分析结果不符合预期？

1. **检查数据格式**：确保 CSV 文件包含所有必需的列
2. **检查列名**：支持中英文列名，但需要完全匹配
3. **查看示例**：参考 `examples/analyzing-marketing-campaign/material/` 中的示例数据

## 📚 下一步

- 阅读 [最佳实践指南](BEST_PRACTICES.md)
- 学习如何 [创建自己的 Skill](CREATE_YOUR_SKILL.md)
- 查看 [FAQ 常见问题](FAQ.md)
- 探索更多 [示例和用例](../examples/)

## 🆘 需要帮助？

- 查看 [FAQ](FAQ.md)
- 提交 [Issue](https://github.com/FlyAlBox/FlySkill/issues)
- 加入讨论组
- 关注公众号"萤火 AI 百宝箱"

