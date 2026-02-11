# 技术实现类需求澄清模板

## 典型场景

- "优化性能"
- "修复 bug"
- "重构代码"
- "升级依赖"
- "改进架构"

## 标准澄清问题

### 1. 问题定位

- **具体问题是什么？**
  - 复现步骤是什么？
  - 预期行为 vs 实际行为？
  - 错误信息/日志是什么？

### 2. 影响范围

- **哪些模块/功能受影响？**
  - 具体文件/代码位置？
  - 影响的用户场景？
  - 是否有现有关联 issue？

### 3. 技术约束

- **技术栈是什么？**
  - 编程语言/框架版本？
  - 依赖库版本？
  - 部署环境？

### 4. 验收标准

- **如何判断问题已解决？**
  - 具体的性能指标（如：响应时间 < 200ms）？
  - 需要运行的测试？
  - 需要验证的场景？

### 5. 优先级

- **紧急程度？**
  - 是否阻断用户使用？
  - 是否有 SLA 要求？
  - 期望完成时间？

## 示例 AskUserQuestion 调用

```python
AskUserQuestion(
    questions=[
        {
            "question": "这个性能优化主要关注哪个方面？",
            "header": "优化目标",
            "options": [
                {"label": "响应时间", "description": "降低 API 响应延迟"},
                {"label": "吞吐量", "description": "提升系统并发处理能力"},
                {"label": "资源占用", "description": "减少 CPU/内存使用"},
                {"label": "数据库查询", "description": "优化 SQL 查询性能"}
            ],
            "multiSelect": false
        },
        {
            "question": "优化目标的具体指标是什么？",
            "header": "性能指标",
            "options": [
                {"label": "P50 < 100ms", "description": "中位数响应时间"},
                {"label": "P95 < 500ms", "description": "95 分位响应时间"},
                {"label": "P99 < 1s", "description": "99 分位响应时间"},
                {"label": "自定义", "description": "在 Other 中说明具体指标"}
            ],
            "multiSelect": false
        }
    ]
)
```

## 常见补充问题

- 是否有性能分析数据（profiling 结果）？
- 是否已经尝试过哪些方案？
- 是否有回滚计划？
- 是否需要监控/告警？
