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
        return True
    
    result = run(f"git clone --depth 1 -q {repo_url}", quiet=True)
    if result and result.returncode == 0:
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
    
    extra_pkgs = [
        "watchdog", "vtracer", "torchsde", "replicate", "llama-cpp-python", "transformers",
        "googletrans-py", "deep-translator", "argostranslate", "ctranslate2", "stanza", "sacremoses", "emoji"
    ]
    
    # 1. Main batch install (reqs + extras)
    reqs_str = ' '.join(['-r ' + r for r in requirements_files])
    pkgs_str = ' '.join(extra_pkgs)
    run(f"uv pip install --system {reqs_str} {pkgs_str}", check=False)
    
    # 2. Special installs
    run("uv pip install flash-attn --no-build-isolation --system", check=False) # Needs no-build-isolation
    run(f'uv pip install https://github.com/explosion/spacy-models/releases/download/xx_sent_ud_sm-3.8.0/xx_sent_ud_sm-3.8.0-py3-none-any.whl --system', check=False)

    # Phase 4: Fix specific dependencies
    print("\n🔧 Fixing specific dependencies...")
    fix_cmds = [
        ("onnx onnxruntime onnxruntime-gpu", "onnxruntime-gpu"),
        ("opencv-python opencv-python-headless opencv-contrib-python-headless opencv-contrib-python", "opencv-python opencv-python-headless opencv-contrib-python-headless opencv-contrib-python"),
        ("pynvml nvidia-ml-py", "nvidia-ml-py")
    ]
    
    for uninstall, install in fix_cmds:
        run(f'uv pip uninstall {uninstall} --system', check=False)
        run(f'uv pip install {install} --system', check=False)

    print("\n" + "=" * 50)
    print("🎉 Custom nodes installation complete!")

    # Phase 5: Patch specific nodes
    patch_ymc_node()


def patch_ymc_node():
    """Suppress ymc-node-suite startup message."""
    target_file = os.path.join(os.getcwd(), "ymc-node-suite-comfyui", "__init__.py")
    if not os.path.exists(target_file):
        return
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        new_lines = []
        suppress = False
        for line in lines:
            # Detect start of the noisy block
            if 'log_msg(msg_padd("=",60,"="))' in line and not suppress:
                # Check next few lines to confirm it's the welcome block
                suppress = True
                new_lines.append(f"# {line}")
                continue
            
            if suppress:
                new_lines.append(f"# {line}")
                # Detect end of block (it ends with same separator)
                if 'log_msg(msg_padd("=",60,"="))' in line:
                    suppress = False
            else:
                new_lines.append(line)
        
        with open(target_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("🔧 Patched ymc-node-suite-comfyui to suppress output")
            
    except Exception as e:
        print(f"⚠ Failed to patch ymc-node-suite: {e}")



if __name__ == "__main__":
    main()
