# Agent Decision-Making Visual Debugger

## Overview
A comprehensive visual debugging tool for tracking, analyzing, and visualizing agent decision-making processes in real-time.

## Architecture

### Core Components

1. **Decision Tracker**
   - Captures agent state snapshots at each decision point
   - Records decision context, inputs, and outputs
   - Stores decision trees with branching logic

2. **State Visualizer**
   - Real-time state machine visualization
   - Interactive node exploration
   - Color-coded decision paths

3. **Decision Flow Analyzer**
   - Step-by-step decision replay
   - Branch comparison tool
   - Probability distribution charts

4. **Multi-Agent Monitor**
   - Concurrent agent tracking
   - Cross-agent decision correlation
   - Resource contention visualization

## Implementation

```python
"""
Agent Decision Visual Debugger
A comprehensive debugging tool for AI agent decision-making processes
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import threading
from collections import defaultdict

class DecisionType(Enum):
    ACTION = "action"
    OBSERVATION = "observation"
    REASONING = "reasoning"
    GOAL_UPDATE = "goal_update"
    PLAN_REVISION = "plan_revision"

@dataclass
class AgentState:
    """Snapshot of agent state at decision point"""
    agent_id: str
    timestamp: datetime
    state_type: str
    beliefs: Dict[str, Any]
    desires: List[str]
    intentions: List[str]
    current_goal: Optional[str]
    available_actions: List[str]
    selected_action: Optional[str]
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Decision:
    """Single decision record"""
    decision_id: str
    agent_id: str
    timestamp: datetime
    decision_type: DecisionType
    context: Dict[str, Any]
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    reasoning_chain: List[str]
    parent_decision_id: Optional[str]
    child_decisions: List[str] = field(default_factory=list)
    state_before: AgentState = None
    state_after: AgentState = None
    
class DecisionTree:
    """Decision tree structure for tracking decision flow"""
    
    def __init__(self):
        self.decisions: Dict[str, Decision] = {}
        self.root_decisions: List[str] = []
        self.decision_counter = 0
        
    def add_decision(self, decision: Decision) -> str:
        decision_id = f"decision_{self.decision_counter}"
        decision.decision_id = decision_id
        self.decisions[decision_id] = decision
        self.decision_counter += 1
        
        if decision.parent_decision_id:
            parent = self.decisions.get(decision.parent_decision_id)
            if parent:
                parent.child_decisions.append(decision_id)
        else:
            self.root_decisions.append(decision_id)
            
        return decision_id
    
    def get_decision_path(self, decision_id: str) -> List[str]:
        """Get full path from root to decision"""
        path = []
        current = self.decisions.get(decision_id)
        while current:
            path.insert(0, current.decision_id)
            current = self.decisions.get(current.parent_decision_id)
        return path

class VisualDebugger:
    """Main visual debugger implementation"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.decision_trees: Dict[str, DecisionTree] = defaultdict(DecisionTree)
        self.agent_states: Dict[str, AgentState] = {}
        self.active_sessions: Dict[str, Dict] = {}
        self.event_listeners: List[callable] = []
        self.lock = threading.Lock()
        
    def start_session(self, session_id: str, agent_ids: List[str]) -> None:
        """Start a new debugging session"""
        with self.lock:
            self.active_sessions[session_id] = {
                "session_id": session_id,
                "agent_ids": agent_ids,
                "start_time": datetime.now(),
                "decision_count": 0,
                "status": "active"
            }
            
    def record_state(self, agent_id: str, state: AgentState) -> None:
        """Record agent state snapshot"""
        with self.lock:
            self.agent_states[agent_id] = state
            self._notify_listeners("state_update", {
                "agent_id": agent_id,
                "state": state
            })
            
    def record_decision(self, agent_id: str, decision: Decision) -> str:
        """Record a decision and return decision ID"""
        with self.lock:
            tree = self.decision_trees[agent_id]
            decision_id = tree.add_decision(decision)
            
            # Update session stats
            for session in self.active_sessions.values():
                if agent_id in session["agent_ids"]:
                    session["decision_count"] += 1
                    
            self._notify_listeners("decision_recorded", {
                "agent_id": agent_id,
                "decision_id": decision_id,
                "decision": decision
            })
            
            return decision_id
            
    def get_decision_tree(self, agent_id: str) -> Dict:
        """Get decision tree visualization data"""
        tree = self.decision_trees[agent_id]
        return {
            "agent_id": agent_id,
            "root_decisions": tree.root_decisions,
            "total_decisions": len(tree.decisions),
            "tree_structure": self._build_tree_structure(tree)
        }
        
    def _build_tree_structure(self, tree: DecisionTree) -> List[Dict]:
        """Build hierarchical tree structure for visualization"""
        def build_node(decision_id: str) -> Dict:
            decision = tree.decisions[decision_id]
            return {
                "id": decision_id,
                "type": decision.decision_type.value,
                "timestamp": decision.timestamp.isoformat(),
                "context": decision.context,
                "children": [build_node(cid) for cid in decision.child_decisions]
            }
        return [build_node(rid) for rid in tree.root_decisions]
        
    def analyze_decision_patterns(self, agent_id: str) -> Dict:
        """Analyze decision patterns for insights"""
        tree = self.decision_trees[agent_id]
        
        type_counts = defaultdict(int)
        avg_confidence = 0
        total_decisions = len(tree.decisions)
        
        for decision in tree.decisions.values():
            type_counts[decision.decision_type.value] += 1
            if decision.state_after:
                avg_confidence += decision.state_after.confidence
                
        if total_decisions > 0:
            avg_confidence /= total_decisions
            
        return {
            "total_decisions": total_decisions,
            "decision_types": dict(type_counts),
            "average_confidence": avg_confidence,
            "tree_depth": self._calculate_tree_depth(tree)
        }
        
    def _calculate_tree_depth(self, tree: DecisionTree) -> int:
        """Calculate maximum depth of decision tree"""
        def depth(decision_id: str) -> int:
            decision = tree.decisions[decision_id]
            if not decision.child_decisions:
                return 1
            return 1 + max(depth(cid) for cid in decision.child_decisions)
        return max((depth(rid) for rid in tree.root_decisions), default=0)
        
    def add_listener(self, callback: callable) -> None:
        """Add event listener for real-time updates"""
        self.event_listeners.append(callback)
        
    def _notify_listeners(self, event_type: str, data: Dict) -> None:
        """Notify all listeners of event"""
        for listener in self.event_listeners:
            try:
                listener(event_type, data)
            except Exception as e:
                print(f"Listener error: {e}")
                
    def export_session(self, session_id: str) -> Dict:
        """Export session data for analysis"""
        session = self.active_sessions.get(session_id, {})
        agent_ids = session.get("agent_ids", [])
        
        return {
            "session": session,
            "agent_trees": {
                aid: self.get_decision_tree(aid)
                for aid in agent_ids
            },
            "final_states": {
                aid: self.agent_states.get(aid)
                for aid in agent_ids
            }
        }

class DebugVisualizer:
    """Visualization renderer for debugging data"""
    
    @staticmethod
    def render_decision_tree(tree_data: Dict) -> str:
        """Render decision tree as ASCII art"""
        def render_node(node: Dict, indent: int = 0) -> List[str]:
            lines = []
            prefix = "  " * indent
            lines.append(f"{prefix}├─ [{node['type']}] {node['id']}")
            for child in node.get("children", []):
                lines.extend(render_node(child, indent + 1))
            return lines
            
        output = [f"Decision Tree for Agent: {tree_data['agent_id']}"]
        output.append(f"Total Decisions: {tree_data['total_decisions']}")
        output.append("")
        
        for root in tree_data.get("tree_structure", []):
            output.extend(render_node(root))
            
        return "\n".join(output)
        
    @staticmethod
    def render_state_comparison(state1: AgentState, state2: AgentState) -> str:
        """Compare two agent states side by side"""
        return f"""
State Comparison:
{'='*50}
Beliefs:
  Before: {len(state1.beliefs)} items
  After:  {len(state2.beliefs)} items
  
Goals:
  Before: {state1.current_goal}
  After:  {state2.current_goal}
  
Confidence:
  Before: {state1.confidence:.2f}
  After:  {state2.confidence:.2f}
{'='*50}
"""

# Example usage and demonstration
def main():
    """Demonstrate the visual debugger capabilities"""
    
    # Initialize debugger
    debugger = VisualDebugger({
        "max_history": 1000,
        "auto_save": True
    })
    
    # Start debugging session
    session_id = "demo_session_001"
    agent_ids = ["agent_alpha", "agent_beta"]
    debugger.start_session(session_id, agent_ids)
    
    # Record initial states
    initial_state = AgentState(
        agent_id="agent_alpha",
        timestamp=datetime.now(),
        state_type="initial",
        beliefs={"location": "start", "energy": 100},
        desires=["explore", "collect_resources"],
        intentions=["move_north"],
        current_goal="reach_destination",
        available_actions=["move_north", "move_south", "wait"],
        selected_action=None,
        confidence=0.85
    )
    debugger.record_state("agent_alpha", initial_state)
    
    # Record decision
    decision = Decision(
        decision_id="",
        agent_id="agent_alpha",
        timestamp=datetime.now(),
        decision_type=DecisionType.ACTION,
        context={"situation": "path_obstruction"},
        inputs={"available_paths": ["north", "east", "west"]},
        outputs={"selected_path": "east"},
        reasoning_chain=[
            "Obstacle detected on north path",
            "Evaluating alternative routes",
            "East path selected - shortest distance"
        ],
        parent_decision_id=None
    )
    debugger.record_decision("agent_alpha", decision)
    
    # Analyze patterns
    patterns = debugger.analyze_decision_patterns("agent_alpha")
    print("\n=== Decision Pattern Analysis ===")
    print(f"Total Decisions: {patterns['total_decisions']}")
    print(f"Average Confidence: {patterns['average_confidence']:.2f}")
    
    # Export session
    session_data = debugger.export_session(session_id)
    print("\n=== Session Export ===")
    print(f"Session ID: {session_id}")
    print(f"Decision Count: {session_data['session']['decision_count']}")
    
if __name__ == "__main__":
    main()
