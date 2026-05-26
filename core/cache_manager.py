import os
import json
import hashlib

class CacheManager:
    def __init__(self, workspace_path=None):
        self.workspace_path = workspace_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.factory_dir = os.path.join(self.workspace_path, ".factory")
        os.makedirs(self.factory_dir, exist_ok=True)
        self.cache_path = os.path.join(self.factory_dir, "cache.json")
        self.cache_data = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "prompt_cache": {},
            "spec_cache": {},
            "context_cache": {},
            "tool_result_cache": {},
            "test_cache": {},
            "plan_cache": {}
        }

    def save_cache(self):
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(self.cache_data, f, ensure_ascii=False, indent=2)

    def generate_hash(self, data):
        if isinstance(data, str):
            payload = data.encode("utf-8")
        else:
            payload = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def get_cache(self, category, key):
        if category in self.cache_data:
            return self.cache_data[category].get(key)
        return None

    def set_cache(self, category, key, value):
        if category not in self.cache_data:
            self.cache_data[category] = {}
        self.cache_data[category][key] = value
        self.save_cache()

    def check_and_retrieve_context(self, spec_hash, index_version):
        cache_key = f"{spec_hash}_{index_version}"
        return self.get_cache("context_cache", cache_key)

    def cache_context(self, spec_hash, index_version, context_pack):
        cache_key = f"{spec_hash}_{index_version}"
        self.set_cache("context_cache", cache_key, context_pack)
