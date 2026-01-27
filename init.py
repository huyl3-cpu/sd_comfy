"""
SD Comfy - ComfyUI Initialization Script (Optimized for A100 80GB)
Parallel operations, idempotency checks, and improved security.
"""

import os
import sys
import subprocess
import concurrent.futures
from typing import Optional

# ============ Configuration ============
COMFYUI_REPO = "https://github.com/comfyanonymous/ComfyUI.git"
MANAGER_REPO = "https://github.com/Comfy-Org/ComfyUI-Manager.git"
ENV_URL = "https://huggingface.co/banhkeomath2/wan22/resolve/main/env.txt"

# Allowed env keys (whitelist for security)
ALLOWED_ENV_KEYS = {
    "dif", "cp", "LORAS_WAN22", "clip", "clipv", "lorasf", 
    "ipadapter", "loras15xl", "cnt", "birefnet", "upscale", "vae"
}


def run(cmd: str, check: bool = True, quiet: bool = False) -> subprocess.CompletedProcess:
    """Run a shell command with optional quiet mode."""
    if not quiet:
        print(f"\n$ {cmd}")
    return subprocess.run(cmd, shell=True, check=check, 
                         stdout=subprocess.DEVNULL if quiet else None,
                         stderr=subprocess.DEVNULL if quiet else None)


def run_parallel(*commands, check: bool = False) -> list:
    """Run multiple commands in parallel using ThreadPoolExecutor."""
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(commands)) as executor:
        futures = {executor.submit(run, cmd, check, True): cmd for cmd in commands}
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"⚠ Command failed: {e}")
    return results


def has_ipython_kernel() -> bool:
    """Check if running in IPython/Jupyter environment."""
    try:
        from IPython import get_ipython
        return get_ipython() is not None
    except Exception:
        return False


def load_env_file(filepath: str, allowed_keys: set) -> dict:
    """
    Securely load environment variables from file.
    Only loads keys that are in the whitelist.
    """
    env_vars = {}
    if not os.path.isfile(filepath):
        print(f"⚠ {filepath} not found, skip loading env")
        return env_vars
    
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            
            # Security: Only allow whitelisted keys
            if key in allowed_keys:
                env_vars[key] = value
                os.environ[key] = value
            else:
                print(f"⚠ Line {line_num}: Unknown env key '{key}' ignored (security)")
    
    print(f"✅ Loaded {len(env_vars)} env variables")
    return env_vars


def setup_directories(env_keys: set) -> None:
    """Create directories from environment variables."""
    created = 0
    for key in env_keys:
        path = os.environ.get(key)
        if path:
            os.makedirs(path, exist_ok=True)
            created += 1
    print(f"✅ Created {created} directories")


def clone_if_missing(repo_url: str, target_dir: str, depth: int = 1) -> bool:
    """Clone a git repository if it doesn't exist. Returns True if cloned."""
    if os.path.isdir(target_dir):
        print(f"✅ {os.path.basename(target_dir)} already exists, skip clone")
        return False
    
    cmd = f"git clone --depth {depth} {repo_url} {target_dir}"
    run(cmd, check=True)
    return True


def install_requirements(requirements_path: str, quiet: bool = True) -> None:
    """Install Python requirements with optimized flags."""
    if not os.path.isfile(requirements_path):
        return
    
    cmd = f'"{sys.executable}" -m pip install -r "{requirements_path}"'
    if quiet:
        cmd += " --quiet --disable-pip-version-check"
    run(cmd, check=True, quiet=quiet)


# ============ Main Setup ============
def main():
    print("🚀 SD Comfy - Optimized Init Script")
    print("=" * 50)
    
    # 1. Setup base directory
    os.makedirs("/content", exist_ok=True)
    os.chdir("/content")
    print("📁 cd /content")
    
    # 2. Parallel: Download env.txt + Install aria2
    print("\n📦 Installing dependencies (parallel)...")
    run_parallel(
        f"wget -q {ENV_URL} -O /content/env.txt",
        "apt-get update -qq",
        check=False
    )
    run("apt-get install -y -qq aria2", check=False)
    
    # 3. Clone ComfyUI
    clone_if_missing(COMFYUI_REPO, "/content/ComfyUI")
    
    # 4. Mount Google Drive (if available)
    try:
        from google.colab import drive
        if has_ipython_kernel():
            drive.mount("/content/drive")
            print("✅ Google Drive mounted")
    except Exception as e:
        print(f"⚠ Skip drive.mount: {e}")
    
    # 5. Load environment variables (with security whitelist)
    load_env_file("/content/env.txt", ALLOWED_ENV_KEYS)
    
    # 6. Setup directories
    os.chdir("/content/ComfyUI")
    print("📁 cd /content/ComfyUI")
    setup_directories(ALLOWED_ENV_KEYS)
    
    # 7. Install ComfyUI requirements
    print("\n📦 Installing ComfyUI requirements...")
    install_requirements("/content/ComfyUI/requirements.txt", quiet=True)
    
    # 8. Setup custom_nodes
    custom_nodes = "/content/ComfyUI/custom_nodes"
    os.makedirs(custom_nodes, exist_ok=True)
    os.chdir(custom_nodes)
    print("📁 cd /content/ComfyUI/custom_nodes")
    
    # 9. Clone ComfyUI-Manager
    mgr_dir = os.path.join(custom_nodes, "ComfyUI-Manager")
    if clone_if_missing(MANAGER_REPO, mgr_dir):
        install_requirements(os.path.join(mgr_dir, "requirements.txt"), quiet=True)
    else:
        # Still install requirements in case they changed
        install_requirements(os.path.join(mgr_dir, "requirements.txt"), quiet=True)
    
    print("\n" + "=" * 50)
    print("🎉 Init complete!")


if __name__ == "__main__":
    main()
else:
    # When imported as module, run automatically
    main()
