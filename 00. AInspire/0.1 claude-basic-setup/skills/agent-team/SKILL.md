# Agent Team Pattern

Route complex tasks to specialized sub-agents instead of doing everything in one context.

## Teams

| Team | Trigger | Responsibility |
|------|---------|---------------|
| **researcher** | "research / analyze / report / investigate" | Web search, file analysis, synthesis, final report |
| **executor** | "build / create / develop / write / design" | Planning, implementation, content production |
| **reviewer** | "review / check / audit / feedback" | Code review, quality check, checklist evaluation |

## Rules

- Delegate to the matching team when the request fits
- Do not mix roles — a researcher does not implement; an executor does not review their own output
- For tasks that span multiple roles, chain them sequentially: researcher → executor → reviewer
- Single, simple tasks do not need delegation — handle inline

## When to Use

Use this skill (or apply this pattern) when:
- A task requires deep research before implementation
- Output quality needs independent review
- Parallel sub-tasks can be split across agents to save context

## Example

```
User: "Research the best approach for X, then implement it, then review the result"

→ researcher: gather options, produce recommendation
→ executor: implement based on recommendation
→ reviewer: audit the implementation against requirements
```
