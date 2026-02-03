"""
SD Comfy - Unified Installation Script (Optimized for A100 80GB)
Handles ComfyUI setup + custom nodes in one optimized flow using UV
"""

import os
import sys
import subprocess
import concurrent.futures
from typing import List, Tuple, Optional

# ============ Configuration ============
COMFYUI_REPO = "https://github.com/comfyanonymous/ComfyUI.git"
MANAGER_REPO = "https://github.com/Comfy-Org/ComfyUI-Manager.git"

# Format: (repo_url, folder_name, has_requirements)
CUSTOM_NODES: List[Tuple[str, str, bool]] = [
    ("https://github.com/yolain/ComfyUI-Easy-Use.git", "ComfyUI-Easy-Use", True),
    ("https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git", "ComfyUI-Custom-Scripts", False),
    ("https://github.com/crystian/ComfyUI-Crystools.git", "ComfyUI-Crystools", True),
    ("https://github.com/cubiq/ComfyUI_essentials.git", "ComfyUI_essentials", True),
    ("https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet.git", "ComfyUI_Custom_Nodes_AlekPet", False),
    ("https://github.com/coolzilj/ComfyUI-Photopea.git", "ComfyUI-Photopea", False),
    ("https://github.com/huyl3-cpu/comfyui-sortlist.git", "comfyui-sortlist", False),
    ("https://github.com/huyl3-cpu/WanAnimatePreprocess.git", "WanAnimatePreprocess", True),
    ("https://github.com/rgthree/rgthree-comfy.git", "rgthree-comfy", False),
    ("https://github.com/1038lab/ComfyUI-QwenVL.git", "ComfyUI-QwenVL", True),
    ("https://github.com/huyl3-cpu/GIMM-VFI.git", "GIMM-VFI", True),
    ("https://github.com/jamesWalker55/comfyui-various.git", "comfyui-various", False),
    ("https://github.com/YMC-GitHub/ymc-node-suite-comfyui.git", "ymc-node-suite-comfyui", True),
    ("https://github.com/daxcay/ComfyUI-YouTubeVideoPlayer.git", "ComfyUI-YouTubeVideoPlayer", False),
    ("https://github.com/TinyBeeman/ComfyUI-TinyBee.git", "ComfyUI-TinyBee", True),
    ("https://github.com/huyl3-cpu/VideoWrapper.git", "VideoWrapper", True),
    ("https://github.com/kijai/ComfyUI-KJNodes.git", "ComfyUI-KJNodes", True),
    ("https://github.com/huyl3-cpu/VideoHelperSuite.git", "VideoHelperSuite", True),
    ("https://github.com/justUmen/Bjornulf_custom_nodes.git", "Bjornulf_custom_nodes", True),
    ("https://github.com/kijai/ComfyUI-Florence2.git", "ComfyUI-Florence2", True),
    ("https://github.com/chflame163/ComfyUI_LayerStyle.git", "ComfyUI_LayerStyle", True),
    ("https://github.com/huyl3-cpu/SeedVR2_VideoUpscaler.git", "SeedVR2_VideoUpscaler", True),
    ("https://github.com/Fannovel16/comfyui_controlnet_aux.git", "comfyui_controlnet_aux", True),
    ("https://github.com/kijai/ComfyUI-segment-anything-2.git", "ComfyUI-segment-anything-2", False),
    ("https://github.com/a-und-b/ComfyUI_Delay.git", "ComfyUI_Delay", False),
    ("https://github.com/huyl3-cpu/segment_wan21.git", "segment_wan21", True),
    ("https://github.com/kijai/ComfyUI-MelBandRoFormer.git", "ComfyUI-MelBandRoFormer", True),
    ("https://github.com/huyl3-cpu/QwenTTS.git", "QwenTTS", True),
    ("https://github.com/ltdrdata/ComfyUI-Impact-Pack.git", "ComfyUI-Impact-Pack", True),
]

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

MAX_PARALLEL_CLONES = 8


# ============ Helper Functions ============
def run(cmd: str, check: bool = True, quiet: bool = False, print_cmd: bool = False) -> Optional[subprocess.CompletedProcess]:
    """Run a shell command."""
    try:
        if not quiet and print_cmd:
            print(f"\\n$ {cmd}")
        return subprocess.run(
            cmd, 
            shell=True, 
            check=check,
            stdout=subprocess.DEVNULL if quiet else None,
            stderr=subprocess.DEVNULL if quiet else None
        )
    except subprocess.CalledProcessError as e:
        return None


def has_ipython_kernel() -> bool:
    """Check if running in IPython/Jupyter environment."""
    try:
        from IPython import get_ipython
        return get_ipython() is not None
    except Exception:
        return False


def setup_directories(dirs: list) -> None:
    """Create model directories."""
    for path in dirs:
        os.makedirs(path, exist_ok=True)


def clone_repo(repo_url: str, folder_name: str) -> bool:
    """Clone a repository with depth 1 if it doesn't exist."""
    if os.path.isdir(folder_name):
        return True
    
    result = run(f"git clone --depth 1 -q {repo_url}", quiet=True)
    if result and result.returncode == 0:
        return True
    else:
        return False


# ============ Main Setup ============
def main():
    print("Đang cài đặt custom_nodes và model, quá trình diễn ra trong khoảng 5 - 7 phút")
    print("🚀 SD Comfy - Unified Installation Script")
    print("=" * 50)
    
    # 1. Setup base directory
    os.makedirs("/content", exist_ok=True)
    os.chdir("/content")
    print("📁 cd /content")
    
    # 2. Install system dependencies
    print("📦 Installing system dependencies...")
    run("apt-get update -qq", check=False, quiet=True)
    run("apt-get install -y -qq aria2", check=False, quiet=True)
    run("pip install uv", check=False, quiet=True)
    
    # 3. Clone ComfyUI
    print("📦 Cloning ComfyUI...")
    if os.path.isdir("/content/ComfyUI"):
        print("✅ ComfyUI already exists")
    else:
        run(f"git clone --depth 1 -q {COMFYUI_REPO} /content/ComfyUI", check=True)
    
    # 4. Setup directories
    os.chdir("/content/ComfyUI")
    setup_directories(MODEL_DIRS)
    
    # 5. Clone ComfyUI-Manager
    print("📦 Cloning ComfyUI-Manager...")
    custom_nodes_dir = "/content/ComfyUI/custom_nodes"
    os.makedirs(custom_nodes_dir, exist_ok=True)
    os.chdir(custom_nodes_dir)
    
    mgr_dir = os.path.join(custom_nodes_dir, "ComfyUI-Manager")
    if os.path.isdir(mgr_dir):
        print("✅ ComfyUI-Manager already exists")
    else:
        run(f"git clone --depth 1 -q {MANAGER_REPO} {mgr_dir}", check=True)
    
    # 6. Clone custom nodes (parallel)
    print(f"📦 Cloning {len(CUSTOM_NODES)} custom nodes (parallel, max {MAX_PARALLEL_CLONES})...")
    
    clone_results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PARALLEL_CLONES) as executor:
        futures = {executor.submit(clone_repo, node[0], node[1]): node[1] for node in CUSTOM_NODES}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            clone_results[name] = future.result()
    
    cloned = sum(1 for v in clone_results.values() if v)
    print(f"📊 Summary: {cloned}/{len(CUSTOM_NODES)} cloned")
    
    # 7. Install Python packages using UV (OPTIMIZED - Single install!)
    print("📦 Installing Python packages...")
    
    # Phase 1: Install PyTorch stack first (heavy binaries)
    print("  → Phase 1: PyTorch stack...")
    pytorch_packages = "torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 torchcodec==0.10.0"
    run(f"uv pip install --system {pytorch_packages}", check=False, quiet=False)
    
    # Phase 2: Install all packages from consolidated requirements.txt (FAST!)
    print("  → Phase 2: Installing from consolidated requirements.txt...")
    run("uv pip install --system -r /content/sd_comfy/requirements.txt", check=False, quiet=False)
    print("  → ✓ All packages installed in single pass!")
    
    # 8. Special installs (git packages & wheels)
    print("📦 Special installs...")
    run('uv pip install https://github.com/explosion/spacy-models/releases/download/xx_sent_ud_sm-3.8.0/xx_sent_ud_sm-3.8.0-py3-none-any.whl --system', check=False, quiet=False)
    run('uv pip install git+https://github.com/argosopentech/argos-translate.git@08f017c324628434d671cf4d191ce681c620ff33 --system', check=False, quiet=False)
    
    # 9. Fix specific dependencies
    print("🔧 Fixing specific dependencies...")
    run("uv pip uninstall onnxruntime onnxruntime-gpu --system", check=False, quiet=True)
    run("uv pip install onnxruntime-gpu --system", check=False, quiet=True)

    # Specific fixes for QwenVL
    #print("🔧 Aggressively upgrading transformers for QwenVL...")
    #run("pip uninstall -y transformers", check=False, quiet=False)
    #run("pip install transformers>=4.48.0", check=False, quiet=False)
    run("uv pip install llama-cpp-python --system", check=False, quiet=False)
    
    print("=" * 50)
    print("🎉 Installation complete!")



if __name__ == "__main__":
    main()
