# Agent Decision-Making Visual Debugger

## 项目概述

一个全面的可视化调试工具，用于实时跟踪、分析和可视化AI代理的决策过程。

## 核心功能

### 1. 决策追踪器 (Decision Tracker)
- 在每个决策点捕获代理状态快照
- 记录决策上下文、输入和输出
- 存储带有分支逻辑的决策树

### 2. 状态可视化器 (State Visualizer)
- 实时状态机可视化
- 交互式节点探索
- 彩色编码的决策路径

### 3. 决策流分析器 (Decision Flow Analyzer)
- 逐步决策回放
- 分支比较工具
- 概率分布图表

### 4. 多代理监控器 (Multi-Agent Monitor)
- 并发代理跟踪
- 跨代理决策关联
- 资源争用可视化

## 技术架构

```
┌─────────────────────────────────────────────────┐
│             Visual Debugger Core                │
├─────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │ Decision  │  │  State    │  │  Flow     │  │
│  │ Tracker   │  │Visualizer │  │ Analyzer  │  │
│  └───────────┘  └───────────┘  └───────────┘  │
├─────────────────────────────────────────────────┤
│           Multi-Agent Coordinator               │
├─────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────┐  │
│  │         Event Notification System         │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## 关键特性

### 线程安全设计
- 使用threading.Lock确保多线程环境下的数据一致性
- 支持高并发决策记录

### 事件驱动架构
- 实时通知机制
- 可插拔的事件监听器

### 决策树分析
- 自动计算树深度
- 决策模式统计分析
- 置信度追踪

### 会话管理
- 支持多会话并行调试
- 完整的会话数据导出

## 使用示例

```python
from agent_decision_visual_debugger import VisualDebugger, Decision, DecisionType

# 初始化调试器
debugger = VisualDebugger()

# 启动调试会话
debugger.start_session("session_001", ["agent_1", "agent_2"])

# 记录决策
decision = Decision(
    agent_id="agent_1",
    decision_type=DecisionType.ACTION,
    context={"situation": "path_obstruction"},
    reasoning_chain=["分析障碍", "评估路径", "选择最优方案"]
)
debugger.record_decision("agent_1", decision)

# 分析决策模式
patterns = debugger.analyze_decision_patterns("agent_1")
```

## 决策类型支持

| 类型 | 说明 |
|------|------|
| ACTION | 执行动作决策 |
| OBSERVATION | 观察结果处理 |
| REASONING | 推理过程 |
| GOAL_UPDATE | 目标更新 |
| PLAN_REVISION | 计划修正 |

## 可视化输出

### 决策树可视化
```
Decision Tree for Agent: agent_alpha
Total Decisions: 5

├─ [action] decision_0
  ├─ [reasoning] decision_1
    ├─ [action] decision_3
  ├─ [observation] decision_2
    ├─ [goal_update] decision_4
```

### 状态对比
```
State Comparison:
==================================================
Beliefs:
  Before: 2 items
  After:  3 items
  
Confidence:
  Before: 0.85
  After:  0.92
==================================================
```

## 性能指标

- 支持同时跟踪多个代理（100+）
- 决策记录延迟 < 1ms
- 内存占用优化（可配置历史记录上限）
- 支持实时分析和事后回放

## 扩展性

### 添加自定义事件监听器
```python
def my_listener(event_type, data):
    print(f"Event: {event_type}")
    # 自定义处理逻辑

debugger.add_listener(my_listener)
```

### 自定义状态属性
```python
state = AgentState(
    agent_id="agent_1",
    # ... 标准属性 ...
    metadata={
        "custom_field_1": "value1",
        "custom_field_2": 42
    }
)
```

## 应用场景

1. **调试复杂代理行为** - 追踪代理为何做出特定决策
2. **优化决策算法** - 分析决策模式和效率
3. **多代理协调分析** - 监控代理间交互
4. **教学演示** - 可视化AI决策过程
5. **性能调优** - 识别决策瓶颈

## 技术栈

- Python 3.8+
- 标准库实现（无外部依赖）
- 线程安全设计
- 事件驱动架构

## 后续扩展方向

1. Web界面可视化（React/Vue前端）
2. 实时WebSocket推送
3. 决策路径搜索和过滤
4. 导出为标准格式（JSON/GraphML）
5. 与主流Agent框架集成（LangChain、AutoGPT等）

---
**版本**: 1.0.0
**作者**: 媛鸢 (Yuanyuan)
**日期**: 2026-03-21
