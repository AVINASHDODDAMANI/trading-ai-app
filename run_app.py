import subprocess
import webbrowser
import time
import os
import sys

def resource_path(relative_path):
    """Get absolute path for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Start FastAPI backend
backend_dir = resource_path("backend")
uvicorn_cmd = [
    sys.executable,
    "-m",
    "uvicorn",
    "main:app",
    "--host",
    "127.0.0.1",
    "--port",
    "8000",
]

subprocess.Popen(uvicorn_cmd, cwd=backend_dir)

# Wait for server
time.sleep(3)

# Open frontend
frontend_file = resource_path("frontend/index.html")
webbrowser.open(f"file:///{frontend_file}")