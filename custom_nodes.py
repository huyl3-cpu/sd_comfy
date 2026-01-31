"""
SD Comfy - Custom Nodes Installer (Optimized for A100 80GB)
Parallel git clones and pip installs for faster setup.
"""

import os
import sys
import subprocess
import concurrent.futures
from typing import List, Tuple, Optional

# ============ Configuration ============
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
    ("https://github.com/rgthree/rgthree-comfy.git", "rgthree-comfy", True),
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
    ("https://github.com/SeanScripts/ComfyUI-Unload-Model.git", "ComfyUI-Unload-Model", False),
    ("https://github.com/huyl3-cpu/QwenTTS.git", "QwenTTS", True),
]

# Additional downloads
EXTRA_DOWNLOADS = [
    ("hf download banhkeomath2/sound --local-dir /content/ComfyUI/custom_nodes/ComfyUI-Custom-Scripts/web/js/assets --quiet", "sound assets"),
]

MAX_PARALLEL_CLONES = 8

def run(cmd: str, check: bool = True, quiet: bool = False) -> Optional[subprocess.CompletedProcess]:
    """Run a shell command."""
    try:
        return subprocess.run(
            cmd, 
            shell=True, 
            check=check,
            stdout=subprocess.DEVNULL if quiet else None,
            stderr=subprocess.DEVNULL if quiet else None
        )
    except subprocess.CalledProcessError as e:
        if not quiet:
            print(f"⚠ Command failed: {cmd}")
        return None


def clone_repo(repo_url: str, folder_name: str) -> bool:
    """Clone a repository with depth 1 if it doesn't exist."""
    if os.path.isdir(folder_name):
        print(f"  ✓ {folder_name} (exists)")
        return True
    
    result = run(f"git clone --depth 1 -q {repo_url}", quiet=True)
    if result and result.returncode == 0:
        print(f"  ✓ {folder_name} (cloned)")
        return True
    else:
        print(f"  ✗ {folder_name} (failed)")
        return False


def setup_node(node_info: Tuple[str, str, bool]) -> Tuple[str, bool, Optional[str]]:
    """Clone a node and check for requirements. Returns (name, clone_success, req_path)."""
    repo_url, folder_name, has_req = node_info
    clone_success = clone_repo(repo_url, folder_name)
    
    req_path = None
    if clone_success and has_req:
        possible_req = os.path.join(folder_name, "requirements.txt")
        if os.path.isfile(possible_req):
            req_path = possible_req
    
    return (folder_name, clone_success, req_path)


def main():
    print("🚀 SD Comfy - Custom Nodes Installer (Optimized)")
    print("=" * 50)
    
    # 0. Install uv
    print("📦 Checking uv...")
    run(f'"{sys.executable}" -m pip install uv', check=False, quiet=True)
    
    # Ensure we're in custom_nodes directory
    custom_nodes_dir = "/content/ComfyUI/custom_nodes"
    os.makedirs(custom_nodes_dir, exist_ok=True)
    os.chdir(custom_nodes_dir)
    print(f"📁 cd {custom_nodes_dir}\n")
    
    # Phase 1: Parallel git clones
    print(f"📦 Cloning {len(CUSTOM_NODES)} repositories (parallel, max {MAX_PARALLEL_CLONES})...")
    
    requirements_files = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PARALLEL_CLONES) as executor:
        futures = {executor.submit(setup_node, node): node[1] for node in CUSTOM_NODES}
        for future in concurrent.futures.as_completed(futures):
            name, clone_ok, req_path = future.result()
            if start_req := req_path:
                 requirements_files.append(req_path)

    print(f"\n✅ Cloning complete.")
    
    # Phase 2: Extra downloads
    if EXTRA_DOWNLOADS:
        print("\n📥 Extra downloads...")
        for cmd, desc in EXTRA_DOWNLOADS:
            print(f"  → {desc}")
            run(cmd, check=False, quiet=True)
    
    # Phase 3: Global Installation (Batch)
    print("\n📦 Installing pip packages (Global Batch)...")
    
    # Build huge command
    install_cmd = ["uv", "pip", "install", "--system"]
    
    # Add all requirements files
    for r in requirements_files:
        install_cmd.extend(["-r", r])
        
    # Add additional packages
    additional_packages = [
        "watchdog", "vtracer", "torchsde", "replicate", 
        "llama-cpp-python", "transformers",
        "flash-attn", 
        "googletrans-py", "deep-translator", "argostranslate", 
        "ctranslate2", "stanza", "sacremoses", "emoji"
    ]
    install_cmd.extend(additional_packages)
    
    # Run the big install
    print(f"  → Installing {len(requirements_files)} requirements files and {len(additional_packages)} extra packages...")
    
    # We join manually for visual printing, but subprocess takes list ideally. 
    # But run() takes string. Let's form the string carefully.
    # Note: flash-attn might need --no-build-isolation, so we handle it separately or mix it?
    # Mixing --no-build-isolation usually applies to all. Safe to run flash-attn separately?
    # User had !pip install flash-attn --no-build-isolation.
    # Let's separate flash-attn to be safe.
    
    # remove flash-attn from batch
    main_packages = [p for p in additional_packages if p != "flash-attn"]
    
    cmd_str = f"uv pip install --system {' '.join(['-r ' + r for r in requirements_files])} {' '.join(main_packages)}"
    run(cmd_str, check=False)
    
    # Install flash-attn separately
    print("  → Installing flash-attn...")
    run("uv pip install flash-attn --no-build-isolation --system", check=False)

    # Install spacy model
    print("\n📦 Installing Spacy model...")
    run(f'uv pip install https://github.com/explosion/spacy-models/releases/download/xx_sent_ud_sm-3.8.0/xx_sent_ud_sm-3.8.0-py3-none-any.whl --system', check=False)

    # Phase 4: Fix specific dependencies (Uninstall & Reinstall)
    print("\n🔧 Fixing specific dependencies...")
    run(f'uv pip uninstall onnx onnxruntime onnxruntime-gpu --system', check=False)
    run(f'uv pip install onnxruntime-gpu --system', check=False)

    run(f'uv pip uninstall opencv-python opencv-python-headless opencv-contrib-python-headless opencv-contrib-python --system', check=False)
    run(f'uv pip install opencv-python opencv-python-headless opencv-contrib-python-headless opencv-contrib-python --system', check=False)

    run(f'uv pip uninstall pynvml nvidia-ml-py --system', check=False)
    run(f'uv pip install nvidia-ml-py --system', check=False)

    print("\n" + "=" * 50)
    print("🎉 Custom nodes installation complete!")


if __name__ == "__main__":
    main()
