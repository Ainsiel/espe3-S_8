import os
import json
from datetime import datetime, timezone

class UsageLedger:
    def __init__(self, cycle_id=None):
        self.cycle_id = cycle_id
        self.runs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".factory", "runs")
        self.cycle_dir = None
        self.started_at = None
        self.cumulative_usage = {
            "input_tokens": 0,
            "cached_input_tokens": 0,
            "output_tokens": 0,
            "tool_calls": 0,
            "estimated_cost": 0.0
        }
        if self.cycle_id:
            self.cycle_dir = os.path.join(self.runs_dir, self.cycle_id)
            os.makedirs(self.cycle_dir, exist_ok=True)
            self.started_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def set_cycle_id(self, cycle_id):
        self.cycle_id = cycle_id
        self.cycle_dir = os.path.join(self.runs_dir, self.cycle_id)
        os.makedirs(self.cycle_dir, exist_ok=True)
        self.started_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def record_usage(self, agent_id, phase, skill_id, input_tokens, output_tokens, cached_input_tokens=0, tool_calls=0, model="Gemini 3.5 Flash (High)"):
        # Pricing: Input $0.075 / 1M, Cached Input $0.01875 / 1M, Output $0.30 / 1M
        cost = (input_tokens * 0.075 / 1_000_000) + (cached_input_tokens * 0.01875 / 1_000_000) + (output_tokens * 0.30 / 1_000_000)
        
        self.cumulative_usage["input_tokens"] += input_tokens
        self.cumulative_usage["cached_input_tokens"] += cached_input_tokens
        self.cumulative_usage["output_tokens"] += output_tokens
        self.cumulative_usage["tool_calls"] += tool_calls
        self.cumulative_usage["estimated_cost"] += cost

        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        entry = {
            "timestamp": timestamp,
            "cycle_id": self.cycle_id,
            "phase": phase,
            "agent_id": agent_id,
            "skill_id": skill_id,
            "model": model,
            "input_tokens": input_tokens,
            "cached_input_tokens": cached_input_tokens,
            "output_tokens": output_tokens,
            "tool_calls": tool_calls,
            "estimated_cost": cost,
            "cumulative": self.cumulative_usage.copy()
        }

        if self.cycle_dir:
            ledger_path = os.path.join(self.cycle_dir, "usage_ledger.jsonl")
            with open(ledger_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
        return entry

    def get_totals(self):
        return self.cumulative_usage
