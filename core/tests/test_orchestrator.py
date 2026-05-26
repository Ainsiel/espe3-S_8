import os
import json
import pytest
import shutil
from core.orchestrator import Orchestrator
from core.sandbox import SandboxManager
from core.index_manager import IndexManager
from core.cache_manager import CacheManager

@pytest.fixture
def workspace_setup():
    test_workspace = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    yield test_workspace

def test_orchestrator_initialization(workspace_setup):
    orch = Orchestrator(workspace_setup)
    orch.initialize_cycle("test_project", "Test Project", "Requerimiento de pruebas")
    
    assert orch.cycle_id is not None
    assert orch.state["project_id"] == "test_project"
    assert orch.state["status"] == "running"
    assert orch.state["gates"]["sdd_spec_first"] == "pending"

def test_sandbox_security(workspace_setup):
    sandbox = SandboxManager("test_project", workspace_setup)
    
    # Executing safe allowed command
    res_safe = sandbox.run_command("echo Hello")
    assert res_safe["status"] == "success"
    assert "Hello" in res_safe["stdout"]
    
    # Executing blocked command containing SUDO
    res_unsafe = sandbox.run_command("sudo rm -rf /")
    assert res_unsafe["status"] == "blocked"

def test_indexer_and_cache(workspace_setup):
    index_m = IndexManager(workspace_setup)
    cache_m = CacheManager(workspace_setup)
    
    index_data = index_m.scan_workspace()
    assert index_data is not None
    
    test_hash = cache_m.generate_hash("some_data")
    cache_m.set_cache("test_cache", test_hash, "cached_value")
    
    cached = cache_m.get_cache("test_cache", test_hash)
    assert cached == "cached_value"

def test_full_cycle_execution(workspace_setup):
    orch = Orchestrator(workspace_setup)
    # Clean old projects/test_project to avoid state conflict
    proj_dir = os.path.join(workspace_setup, "projects", "test_project")
    if os.path.exists(proj_dir):
        shutil.rmtree(proj_dir)
        
    success = orch.execute_cycle("test_project", "Test Project", "Quiero una base de datos simple de items")
    assert success is True
    
    # Check that spec files were created
    assert os.path.exists(os.path.join(proj_dir, "specs", "spec.md"))
    assert os.path.exists(os.path.join(proj_dir, "specs", "plan.md"))
    assert os.path.exists(os.path.join(proj_dir, "specs", "validation-report.md"))
    assert os.path.exists(os.path.join(proj_dir, "backend", "app", "main.py"))
