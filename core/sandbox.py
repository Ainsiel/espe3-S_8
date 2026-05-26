import os
import shutil
import subprocess
import sys

class SandboxManager:
    def __init__(self, project_id, workspace_path=None):
        self.project_id = project_id
        self.workspace_path = workspace_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sandbox_root = os.path.join(self.workspace_path, "sandbox", self.project_id)
        os.makedirs(self.sandbox_root, exist_ok=True)

    def clean_sandbox(self):
        """Cleans the sandbox environment."""
        if os.path.exists(self.sandbox_root):
            shutil.rmtree(self.sandbox_root)
        os.makedirs(self.sandbox_root, exist_ok=True)

    def prepare_sandbox(self, project_path):
        """Copies project files into sandbox for isolated testing."""
        self.clean_sandbox()
        if os.path.exists(project_path):
            for item in os.listdir(project_path):
                s = os.path.join(project_path, item)
                d = os.path.join(self.sandbox_root, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, symlinks=False, ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache', '*.pyc'))
                else:
                    shutil.copy2(s, d)

    def run_command(self, cmd, cwd_subdir=None):
        """Executes allowlisted shell commands securely in the sandbox."""
        cwd = self.sandbox_root
        if cwd_subdir:
            cwd = os.path.join(self.sandbox_root, cwd_subdir)
            os.makedirs(cwd, exist_ok=True)

        # Allow all commands and tools, except that any command containing 'sudo' requires explicit confirmation.
        cmd_parts = cmd.split()
        if not cmd_parts:
            return {"status": "error", "message": "Comando vacío."}

        # Case-insensitive check for sudo in any part of the command
        has_sudo = any(part.lower() == "sudo" for part in cmd_parts)
        if has_sudo:
            print(f"\n\033[93m[ATENCIÓN - SEGURIDAD] El comando requiere privilegios elevados (SUDO): '{cmd}'\033[0m")
            try:
                confirm = input("¿Desea permitir la ejecución de este comando con SUDO? (sí/no): ").strip().lower()
                if confirm not in ["sí", "si", "yes", "y"]:
                    return {
                        "status": "blocked",
                        "message": "Ejecución de comando SUDO rechazada por el usuario (no se concedió confirmación)."
                    }
            except Exception as e:
                return {
                    "status": "blocked",
                    "message": f"Comando SUDO bloqueado. No se pudo obtener confirmación interactiva: {str(e)}"
                }

        try:
            # Run the command in a subprocess with isolated environment
            env = os.environ.copy()
            # Ensure python path includes sandbox root and cwd
            env["PYTHONPATH"] = os.path.pathsep.join([cwd, self.sandbox_root, env.get("PYTHONPATH", "")])
            
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                env=env,
                timeout=30 # 30-second circuit breaker for long runs
            )
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "message": "La ejecución del comando excedió el tiempo límite (Timeout - 30s)."
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Fallo al ejecutar el comando: {str(e)}"
            }
            
    def run_tests(self, cwd_subdir="backend"):
        """Runs pytest on sandbox code."""
        # Check if tests directory exists inside sandbox
        test_dir = os.path.join(self.sandbox_root, cwd_subdir, "tests")
        if not os.path.exists(test_dir):
            # Try root level tests
            test_dir = os.path.join(self.sandbox_root, "tests")
            if not os.path.exists(test_dir):
                return {
                    "status": "success",
                    "stdout": "No se encontraron suites de prueba para ejecutar.",
                    "exit_code": 0
                }

        # Run pytest via sys.executable to avoid local executable path issues
        return self.run_command(f"{sys.executable} -m pytest", cwd_subdir=cwd_subdir)
