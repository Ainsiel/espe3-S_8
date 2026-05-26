import os
import json
import hashlib
from datetime import datetime, timezone

class IndexManager:
    def __init__(self, workspace_path=None):
        self.workspace_path = workspace_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.factory_dir = os.path.join(self.workspace_path, ".factory")
        os.makedirs(self.factory_dir, exist_ok=True)
        self.index_path = os.path.join(self.factory_dir, "index.json")
        self.index_data = self.load_index()

    def load_index(self):
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "last_updated": None,
            "spec_index": {},
            "code_index": {},
            "test_index": {},
            "policy_index": {},
            "learning_index": {},
            "evidence_index": {}
        }

    def save_index(self):
        self.index_data["last_updated"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.index_data, f, ensure_ascii=False, indent=2)

    def calculate_file_hash(self, file_path):
        hasher = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                buf = f.read(65536)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(65536)
            return hasher.hexdigest()
        except IOError:
            return None

    def scan_workspace(self, project_dir=None):
        """Scans workspace files, hashes them, and indexes them by type."""
        scan_root = project_dir if project_dir else self.workspace_path
        
        # Reset current indices but preserve structure
        self.index_data["spec_index"] = {}
        self.index_data["code_index"] = {}
        self.index_data["test_index"] = {}
        self.index_data["policy_index"] = {}
        self.index_data["learning_index"] = {}
        self.index_data["evidence_index"] = {}

        for root, dirs, files in os.walk(scan_root):
            # Ignore hidden files, runs directory, virtual environments, node_modules
            if any(part in root.split(os.sep) for part in [".git", "runs", "venv", "node_modules", "__pycache__", ".pytest_cache"]):
                continue
            
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.workspace_path)
                file_hash = self.calculate_file_hash(file_path)
                if not file_hash:
                    continue

                file_size = os.path.getsize(file_path)
                last_modified = datetime.fromtimestamp(os.path.getmtime(file_path), timezone.utc).isoformat().replace("+00:00", "Z")
                
                metadata = {
                    "path": rel_path,
                    "hash": file_hash,
                    "size": file_size,
                    "last_modified": last_modified
                }

                # Categorize file
                if file.startswith("0") and file.endswith(".md") and "Fabrica" in root:
                    # Configuration/constitution policy
                    self.index_data["policy_index"][rel_path] = metadata
                elif rel_path.startswith("specs/") or "specs" in root.split(os.sep):
                    self.index_data["spec_index"][rel_path] = metadata
                elif "Aprendizaje" in file and file.endswith(".md"):
                    self.index_data["learning_index"][rel_path] = metadata
                elif "test" in file.lower() or file.endswith("_test.py") or "tests" in root.split(os.sep):
                    self.index_data["test_index"][rel_path] = metadata
                elif file.endswith((".py", ".js", ".jsx", ".html", ".css", ".json")):
                    self.index_data["code_index"][rel_path] = metadata
                else:
                    self.index_data["evidence_index"][rel_path] = metadata

        self.save_index()
        return self.index_data
