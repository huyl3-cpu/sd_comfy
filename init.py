"""
SD Comfy - ComfyUI Initialization Script (Optimized for A100 80GB)
Parallel operations, idempotency checks.
"""

import os
import sys
import subprocess
import concurrent.futures
from typing import Optional

# ============ Configuration ============
COMFYUI_REPO = "https://github.com/comfyanonymous/ComfyUI.git"
MANAGER_REPO = "https://github.com/Comfy-Org/ComfyUI-Manager.git"

# Model directories to create
MODEL_DIRS = [
    "/content/ComfyUI/models/diffusion_models",
    "/content/ComfyUI/models/checkpoints",
    "/content/ComfyUI/models/loras",
    "/content/ComfyUI/models/clip",
    "/content/ComfyUI/models/clip_vision",
    "/content/ComfyUI/models/ipadapter",
    "/content/ComfyUI/models/controlnet",
    "/content/ComfyUI/models/birefnet",
    "/content/ComfyUI/models/upscale_models",
    "/content/ComfyUI/models/vae",
]


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


def setup_directories(dirs: list) -> None:
    """Create model directories."""
    created = 0
    for path in dirs:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            created += 1
    print(f"✅ Created {created} model directories")


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
    
    # 2. Install aria2
    print("\n📦 Installing dependencies...")
    run_parallel(
        "apt-get update -qq",
        check=False
    )
    run("apt-get install -y -qq aria2", check=False)
    
    # 3. Clone ComfyUI
    clone_if_missing(COMFYUI_REPO, "/content/ComfyUI")

    # 3.1 Install specific PyTorch version
    print("\n📦 Installing PyTorch dependencies...")
    run(f'"{sys.executable}" -m pip install torch==2.9.1 torchvision==0.24.1 torchaudio==2.9.1 torchcodec==0.9.1', check=True)
    
    # 4. Mount Google Drive (if available)
    try:
        from google.colab import drive
        if has_ipython_kernel():
            drive.mount("/content/drive")
            print("✅ Google Drive mounted")
    except Exception as e:
        print(f"⚠ Skip drive.mount: {e}")
    
    # 5. Setup directories
    os.chdir("/content/ComfyUI")
    print("📁 cd /content/ComfyUI")
    setup_directories(MODEL_DIRS)
    
    # 6. Install ComfyUI requirements
    print("\n📦 Installing ComfyUI requirements...")
    install_requirements("/content/ComfyUI/requirements.txt", quiet=True)
    
    # 7. Setup custom_nodes
    custom_nodes = "/content/ComfyUI/custom_nodes"
    os.makedirs(custom_nodes, exist_ok=True)
    os.chdir(custom_nodes)
    print("📁 cd /content/ComfyUI/custom_nodes")
    
    # 8. Clone ComfyUI-Manager
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
