# 需求优先级类澄清模板

## 典型场景

- "先把这个做了"
- "哪个更重要？"
- "这个需求的优先级？"
- "可以调整计划吗？"

## 标准澄清问题

### 1. 业务价值

- **这个需求为什么重要？**
  - 影响的业务指标？
  - 解决的痛点？
  - 带来的收益？

### 2. 紧急程度

- **为什么需要现在做？**
  - 是否有外部 deadline？
  - 是否阻塞其他工作？
  - 是否有时间窗口？

### 3. 依赖关系

- **这个需求依赖什么？**
  - 前置条件？
  - 需要等待什么？
  - 依赖其他需求？

### 4. 资源约束

- **有哪些限制？**
  - 人力限制？
  - 时间限制？
  - 预算限制？

## 优先级评估框架

使用 RICE 或 MoSCoW 方法评估：

### RICE
- **Reach（触达）**：影响多少用户
- **Impact（影响）**：对用户的影响程度
- **Confidence（信心）**：对评估的信心
- **Effort（工作量）**：实现所需时间/资源

### MoSCoW
- **Must have**：必须有
- **Should have**：应该有
- **Could have**：可以有
- **Won't have**：不会有

## 示例 AskUserQuestion 调用

```python
AskUserQuestion(
    questions=[
        {
            "question": "这个需求的主要驱动力是什么？",
            "header": "驱动因素",
            "options": [
                {"label": "客户需求", "description": "客户明确要求的功能"},
                {"label": "业务机会", "description": "新的商业机会"},
                {"label": "技术债务", "description": "需要偿还的技术债"},
                {"label": "合规要求", "description": "法规或政策要求"}
            ],
            "multiSelect": false
        },
        {
            "question": "期望的交付时间是什么时候？",
            "header": "时间要求",
            "options": [
                {"label": "紧急", "description": "1 周内"},
                {"label": "高优先级", "description": "2-4 周"},
                {"label": "中等优先级", "description": "1-2 个月"},
                {"label": "灵活安排", "description": "没有明确时间要求"}
            ],
            "multiSelect": false
        },
        {
            "question": "如果无法按时交付，有什么影响？",
            "header": "延期影响",
            "options": [
                {"label": "严重影响", "description": "影响业务/客户关系"},
                {"label": "中等影响", "description": "影响用户体验"},
                {"label": "轻微影响", "description": "可以接受延期"},
                {"label": "无影响", "description": "没有直接后果"}
            ],
            "multiSelect": false
        }
    ]
)
```

## 常见补充问题

- 是否与其他需求有冲突？
- 是否需要重新排期其他任务？
- 是否有里程碑/发布计划？
- 是否需要向上汇报/审批？
