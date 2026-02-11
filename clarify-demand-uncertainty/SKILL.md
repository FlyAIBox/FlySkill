---
name: clarify-demand-uncertainty
description: Systematic approach for clarifying ambiguous requirements before implementation. Use when user requests contain vague objectives, unclear boundaries, missing priorities, undefined acceptance criteria, or incomplete constraints. Common scenarios include technical implementation ("optimize performance", "fix bug"), feature design ("add login", "build admin panel"), and priority planning ("which is more important", "do this first").
---

# Clarify Demand Uncertainty

## Overview

This skill provides a structured framework for clarifying ambiguous user requirements before starting implementation. It helps identify missing critical information and gather it systematically using the `AskUserQuestion` tool.

## When to Use This Skill

Trigger this skill when user requests exhibit:

- **Ambiguous scope** - Missing specific objectives or boundaries ("optimize performance", "fix the bug")
- **Unclear priorities** - No urgency level or timeline stated ("do this first", "which is more important")
- **Missing constraints** - No technical stack or environment limits mentioned
- **Undefined acceptance criteria** - Cannot determine how to verify completion

## Quick Start

1. **Identify the ambiguity type** - Match to one of three categories:
   - Technical implementation
   - Feature design
   - Priority planning

2. **Load the appropriate reference** - Read the corresponding reference file:
   - `references/technical-implementation.md` - For optimization, bug fixes, refactoring
   - `references/feature-design.md` - For new features, UI/UX, integrations
   - `references/priority-planning.md` - For prioritization, scheduling decisions

3. **Load workflow guide** - Read `references/workflow-guide.md` for the standard clarification process

4. **Ask clarifying questions** - Use `AskUserQuestion` to gather missing information in batches

5. **Confirm understanding** - Summarize what was learned and verify with the user

## Standard Clarification Framework

### 1. Context & Background
- Why is this needed?
- What problem/opportunity does it address?
- Who are the target users?

### 2. Scope & Boundaries
- What are the core objectives?
- What's included vs. explicitly excluded?

### 3. Priorities & Timeline
- What's the urgency level?
- Are there hard deadlines?
- Can it be delivered in phases?

### 4. Technical Constraints
- What's the tech stack?
- Any compatibility requirements?
- Existing systems to integrate with?

### 5. Acceptance Criteria
- What defines "done"?
- How will success be measured?
- Any performance/quality metrics?

### 6. Dependencies
- Any prerequisites?
- Does it affect existing functionality?
- Cross-team collaboration needed?

## Best Practices

### Batch Questions Efficiently
Use `AskUserQuestion` to ask 2-4 questions at once rather than serial questioning. This respects the user's time and provides context for their answers.

### Provide Clear Options
For each question, offer 2-4 specific options with descriptions. Include "Other" as an option for flexibility.

### Reference Templates
Load the appropriate reference file (`technical-implementation.md`, `feature-design.md`, or `priority-planning.md`) to get pre-defined question templates for common scenarios.

### Confirm Understanding
After gathering information, summarize back to the user: "So to confirm, you want [X] with [constraints], and success means [criteria]?"

### Adjust as Needed
- Simple requests: Merge or skip steps
- Complex requests: Iterate and clarify progressively
- Some information may require exploration first

## References

- **[Workflow Guide](references/workflow-guide.md)** - Complete step-by-step clarification process
- **[Technical Implementation](references/technical-implementation.md)** - Templates for optimization, bugs, refactoring
- **[Feature Design](references/feature-design.md)** - Templates for new features, UI/UX, integrations
- **[Priority Planning](references/priority-planning.md)** - Templates for prioritization and scheduling decisions

## Example Workflow

**User request**: "Optimize the performance"

1. **Identify type**: Technical implementation → Load `technical-implementation.md`

2. **Ask questions**:
```python
AskUserQuestion(
    questions=[
        {
            "question": "What aspect of performance needs optimization?",
            "header": "Optimization Target",
            "options": [
                {"label": "Response Time", "description": "Reduce API latency"},
                {"label": "Throughput", "description": "Increase concurrent capacity"},
                {"label": "Resource Usage", "description": "Reduce CPU/memory"}
            ],
            "multiSelect": false
        },
        {
            "question": "What are the target metrics?",
            "header": "Performance Goals",
            "options": [
                {"label": "P50 < 100ms", "description": "Median response time"},
                {"label": "P95 < 500ms", "description": "95th percentile"}
            ],
            "multiSelect": false
        }
    ]
)
```

3. **Confirm**: "Got it. You want to reduce API response time, targeting P95 < 500ms. Is that correct?"
