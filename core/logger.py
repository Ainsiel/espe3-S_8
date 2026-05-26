import os
import json
from datetime import datetime, timezone

class FactoryLogger:
    def __init__(self, cycle_id=None):
        self.cycle_id = cycle_id
        self.runs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".factory", "runs")
        self.cycle_dir = None
        if self.cycle_id:
            self.cycle_dir = os.path.join(self.runs_dir, self.cycle_id)
            os.makedirs(self.cycle_dir, exist_ok=True)
            os.makedirs(os.path.join(self.cycle_dir, "agent_logs"), exist_ok=True)

    def set_cycle_id(self, cycle_id):
        self.cycle_id = cycle_id
        self.cycle_dir = os.path.join(self.runs_dir, self.cycle_id)
        os.makedirs(self.cycle_dir, exist_ok=True)
        os.makedirs(os.path.join(self.cycle_dir, "agent_logs"), exist_ok=True)

    def log_event(self, agent_id, phase, event, status="success", evidence_path=None, trace_id=None):
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        log_entry = {
            "timestamp": timestamp,
            "cycle_id": self.cycle_id,
            "trace_id": trace_id or f"TRACE-{self.cycle_id}",
            "agent_id": agent_id,
            "phase": phase,
            "event": event,
            "status": status,
            "evidence_path": evidence_path
        }
        
        # Write to general cycle_log.jsonl
        if self.cycle_dir:
            cycle_log_path = os.path.join(self.cycle_dir, "cycle_log.jsonl")
            with open(cycle_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            
            # Write to agent-specific log
            agent_log_path = os.path.join(self.cycle_dir, "agent_logs", f"{agent_id}.jsonl")
            with open(agent_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        # Print to console in readable format
        status_color = "\033[92m" if status == "success" else "\033[91m" if status == "error" else "\033[93m"
        reset_color = "\033[0m"
        print(f"[{timestamp}] [{agent_id.upper()}] ({phase.upper()}) {event} -> {status_color}{status.upper()}{reset_color}")

    def log_user_update(self, message):
        if self.cycle_dir:
            user_updates_path = os.path.join(self.cycle_dir, "user_updates.log")
            timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            with open(user_updates_path, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")
        print(f"\033[94m[USER UPDATE] {message}\033[0m")
