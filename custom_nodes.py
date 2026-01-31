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
    ("https://github.com/rgthree/rgthree-comfy.git", "rgthree-comfy", False),
    ("https://github.com/1038lab/ComfyUI-QwenVL.git", "ComfyUI-QwenVL", True),
    ("https://github.com/huyl3-cpu/GIMM-VFI.git", "GIMM-VFI", True),
    ("https://github.com/jamesWalker55/comfyui-various.git", "comfyui-various", False),
    ("https://github.com/YMC-GitHub/ymc-node-suite-comfyui.git", "ymc-node-suite-comfyui", True),
    ("https://github.com/daxcay/ComfyUI-YouTubeVideoPlayer.git", "ComfyUI-YouTubeVideoPlayer", False),
    ("https://github.com/TinyBeeman/ComfyUI-TinyBee.git", "ComfyUI-TinyBee", True),
    ("https://github.com/huyl3-cpu/VideoWrapper.git", "VideoWrapper", True),
    ("https://github.com/kijai/ComfyUI-KJNodes.git", "ComfyUI-KJNodes", True),
    ("https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git", "ComfyUI-VideoHelperSuite", True),
    ("https://github.com/justUmen/Bjornulf_custom_nodes.git", "Bjornulf_custom_nodes", True),
    ("https://github.com/kijai/ComfyUI-Florence2.git", "ComfyUI-Florence2", True),
    ("https://github.com/chflame163/ComfyUI_LayerStyle.git", "ComfyUI_LayerStyle", True),
    ("https://github.com/huyl3-cpu/SeedVR2_VideoUpscaler.git", "SeedVR2_VideoUpscaler", True),
    ("https://github.com/Fannovel16/comfyui_controlnet_aux.git", "comfyui_controlnet_aux", True),
    ("https://github.com/kijai/ComfyUI-segment-anything-2.git", "ComfyUI-segment-anything-2", False),
    ("https://github.com/a-und-b/ComfyUI_Delay.git", "ComfyUI_Delay", False),
    ("https://github.com/huyl3-cpu/segment_wan21.git", "segment_wan21", True),
    ("https://github.com/kijai/ComfyUI-MelBandRoFormer.git", "ComfyUI-MelBandRoFormer", True),
]

# Additional downloads
EXTRA_DOWNLOADS = [
    ("hf download banhkeomath2/sound --local-dir /content/ComfyUI/custom_nodes/ComfyUI-Custom-Scripts/web/js/assets --quiet", "sound assets"),
]

MAX_PARALLEL_CLONES = 8
MAX_PARALLEL_PIP = 4


def run(cmd: str, check: bool = True, quiet: bool = False) -> Optional[subprocess.CompletedProcess]:
    """Run a shell command."""
    try:
        if not quiet:
            print(f"\n$ {cmd}")
        return subprocess.run(
            cmd, 
            shell=True, 
            check=check,
            stdout=subprocess.DEVNULL if quiet else None,
            stderr=subprocess.DEVNULL if quiet else None
        )
    except subprocess.CalledProcessError as e:
        return None



def clone_repo(repo_url: str, folder_name: str) -> bool:
    """Clone a repository with depth 1 if it doesn't exist."""
    if os.path.isdir(folder_name):
        return True
    
    result = run(f"git clone --depth 1 -q {repo_url}", quiet=False)
    if result and result.returncode == 0:
        return True
    else:
        return False


def get_requirements(folder_name: str) -> List[str]:
    """Return list of requirements.txt paths for a node if it exists."""
    req_files = []
    
    # Standard requirements.txt
    req_file = os.path.join(folder_name, "requirements.txt")
    if os.path.isfile(req_file):
        req_files.append(req_file)
        
    return req_files


def get_recursive_requirements(root_folder: str) -> List[str]:
    """Recursively find requirements.txt files."""
    req_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file == "requirements.txt":
                req_files.append(os.path.join(root, file))
    return req_files


def clone_and_get_reqs(node_info: Tuple[str, str, bool]) -> Tuple[str, bool, List[str]]:
    """Clone a node and collect its requirements paths. Returns (name, clone_success, req_paths)."""
    repo_url, folder_name, has_req = node_info
    clone_success = clone_repo(repo_url, folder_name)
    req_paths = []
    
    if clone_success:
        if has_req:
            req_paths.extend(get_requirements(folder_name))
        
        # Special handling for AlekPet (recursive scanning)
        if folder_name == "ComfyUI_Custom_Nodes_AlekPet":
            req_paths.extend(get_recursive_requirements(folder_name))

    return (folder_name, clone_success, req_paths)


def main():
    print("🚀 SD Comfy - Custom Nodes Installer (Optimized)")
    print("=" * 50)
    
    # 0. Install uv
    print("📦 Checking uv...")
    custom_nodes_dir = "/content/ComfyUI/custom_nodes"
    os.makedirs(custom_nodes_dir, exist_ok=True)
    os.chdir(custom_nodes_dir)
    print(f"📁 cd {custom_nodes_dir}\n")
    
    # Phase 1: Parallel git clones
    print(f"📦 Cloning {len(CUSTOM_NODES)} repositories (parallel, max {MAX_PARALLEL_CLONES})...")
    
    all_requirements = []
    clone_results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PARALLEL_CLONES) as executor:
        futures = {executor.submit(clone_and_get_reqs, node): node[1] for node in CUSTOM_NODES}
        for future in concurrent.futures.as_completed(futures):
            name, clone_ok, reqs = future.result()
            clone_results[name] = clone_ok
            if clone_ok and reqs:
                all_requirements.extend(reqs)
    
    cloned = sum(1 for v in clone_results.values() if v)

    # Summary
    print(f"\n📊 Summary: {cloned}/{len(CUSTOM_NODES)} cloned")
    
    # Phase 3: Global Installation (Batch)
    print(f"\n📦 Installing pip packages from {len(all_requirements)} requirement files (Global Batch)...")
    
    # 3.1 Custom Node Requirements
    if all_requirements:
        cmd_parts = ["uv", "pip", "install", "--system"]
        for rf in all_requirements:
            cmd_parts.append("-r")
            cmd_parts.append(f'"{rf}"')
            
        final_cmd = " ".join(cmd_parts)
        run(final_cmd, check=False, quiet=False)
    
    # 3.2 Global Extra Packages
    print("\n📦 Installing extra packages...")
    extra_pkgs = [
        "packaging", "ninja", "rembg", "onnxruntime-gpu", "insightface",
        "ffmpeg-python", "segment-anything", "pytube", "soundfile", "librosa",
        "numba", "diffusers", "transformers", "matplotlib", "scikit-learn",
        "scipy", "pandas", "opencv-python-headless", "imageio", "imageio-ffmpeg",
        "einops", "torchsde", "kornia", "spandrel", "huggingface_hub",
        "llama-cpp-python", "nvidia-ml-py"
    ]
    
    pkg_str = " ".join(extra_pkgs)
    run(f"uv pip install {pkg_str} --system", check=False, quiet=False)

    # Phase 2: Extra downloads (Run after installing huggingface_hub)
    if EXTRA_DOWNLOADS:
        print("\n📥 Extra downloads...")
        for cmd, desc in EXTRA_DOWNLOADS:
            print(f"  → {desc}")
            # Ensure using huggingface-cli
            if cmd.startswith("hf "):
                cmd = cmd.replace("hf ", "huggingface-cli ", 1)
            run(cmd, check=False, quiet=False)

    # 2. Special installs
    run("uv pip install flash-attn --no-build-isolation --system", check=False, quiet=False)
    run(f'uv pip install https://github.com/explosion/spacy-models/releases/download/xx_sent_ud_sm-3.8.0/xx_sent_ud_sm-3.8.0-py3-none-any.whl --system', check=False, quiet=False)

    # Phase 4: Fix specific dependencies
    print("\n🔧 Fixing specific dependencies...")
    fix_cmds = [
        ("protobuf", "protobuf==3.20.3"),
        ("onnxruntime", "onnxruntime-gpu"),
        ("torchaudio", "torchaudio==2.9.1"),
        ("torchvision", "torchvision==0.24.1"),
    ]

    for uninstall, install in fix_cmds:
        run(f'uv pip uninstall {uninstall} --system', check=False, quiet=False)
        run(f'uv pip install {install} --system', check=False, quiet=False)

    print("\n" + "=" * 50)
    print("🎉 Custom nodes installation complete!")


if __name__ == "__main__":
    main()
