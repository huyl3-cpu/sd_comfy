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
    ("hf download banhkeomath2/sound --local-dir /content/ComfyUI/custom_nodes/ComfyUI-Custom-Scripts/web/js/assets", "sound assets"),
]

MAX_PARALLEL_CLONES = 8
MAX_PARALLEL_PIP = 4


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
        return None



def clone_repo(repo_url: str, folder_name: str) -> bool:
    """Clone a repository with depth 1 if it doesn't exist."""
    if os.path.isdir(folder_name):
        return True
    
    result = run(f"git clone --depth 1 -q {repo_url}", quiet=True)
    if result and result.returncode == 0:
        return True
    else:
        return False


def install_requirements(folder_name: str) -> bool:
    """Install requirements.txt for a node if it exists."""
    req_file = os.path.join(folder_name, "requirements.txt")
    if not os.path.isfile(req_file):
        return True
    
    result = run(
        f'"{sys.executable}" -m pip install -r "{req_file}" --quiet --disable-pip-version-check',
        quiet=True
    )
    return result is not None and result.returncode == 0


def clone_and_setup(node_info: Tuple[str, str, bool]) -> Tuple[str, bool, bool]:
    """Clone a node and install its requirements. Returns (name, clone_success, pip_success)."""
    repo_url, folder_name, has_req = node_info
    clone_success = clone_repo(repo_url, folder_name)
    pip_success = True
    
    if clone_success and has_req:
        pip_success = install_requirements(folder_name)
    
    
    # Suppress YMC Node Logs
    if folder_name == "ymc-node-suite-comfyui":
        try:
            init_file = os.path.join(folder_name, "__init__.py")
            if os.path.isfile(init_file):
                with open(init_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Comment out print statements
                new_content = ""
                for line in content.splitlines():
                    if "print" in line and ("-----" in line or "welocme" in line.lower() or "node counts" in line or "version:" in line or "node menu names" in line or "✅" in line):
                        new_content += "# " + line + "\n"
                    else:
                        new_content += line + "\n"
                        
                with open(init_file, "w", encoding="utf-8") as f:
                    f.write(new_content)
        except Exception as e:
            pass # Ignore errors during suppression

    return (folder_name, clone_success, pip_success)


def main():
    # print("🚀 SD Comfy - Custom Nodes Installer (Optimized)")
    # print("=" * 50)
    
    # 0. Install uv
    # print("📦 Checking uv...")custom_nodes directory
    custom_nodes_dir = "/content/ComfyUI/custom_nodes"
    os.makedirs(custom_nodes_dir, exist_ok=True)
    os.chdir(custom_nodes_dir)
    # print(f"📁 cd {custom_nodes_dir}\n")
    
    # Phase 1: Parallel git clones
    # print(f"📦 Cloning {len(CUSTOM_NODES)} repositories (parallel, max {MAX_PARALLEL_CLONES})...")
    
    clone_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PARALLEL_CLONES) as executor:
        futures = {executor.submit(clone_and_setup, node): node[1] for node in CUSTOM_NODES}
        for future in concurrent.futures.as_completed(futures):
            name, clone_ok, pip_ok = future.result()
            clone_results[name] = (clone_ok, pip_ok)
    
    
    cloned = sum(1 for v in clone_results.values() if v[0])
    pip_ok = sum(1 for v in clone_results.values() if v[1])

    # Summary
    print(f"\n📊 Summary: {cloned}/{len(CUSTOM_NODES)} cloned, {pip_ok}/{len(CUSTOM_NODES)} pip success")
    
    # Phase 2: Extra downloads
    if EXTRA_DOWNLOADS:
        # print("\n📥 Extra downloads...")
        for cmd, desc in EXTRA_DOWNLOADS:
            # print(f"  → {desc}")
            run(cmd, check=False, quiet=True)

    # Phase 3: Global Installation (Batch)
    # print("\n📦 Installing pip packages (Global Batch)...")
    
    extra_pkgs = [
        "packaging", "ninja", "rembg", "onnxruntime-gpu", "insightface",
        "ffmpeg-python", "segment-anything", "pytube", "soundfile", "librosa",
        "numba", "diffusers", "transformers", "matplotlib", "scikit-learn",
        "scipy", "pandas", "opencv-python-headless", "imageio", "imageio-ffmpeg",
        "einops", "torchsde", "kornia", "spandrel", "huggingface_hub"
    ]
    
    pkg_str = " ".join(extra_pkgs)
    run(f"uv pip install {pkg_str} --system", check=False, quiet=True)

    # 2. Special installs
    run("uv pip install flash-attn --no-build-isolation --system", check=False, quiet=True)
    run(f'uv pip install https://github.com/explosion/spacy-models/releases/download/xx_sent_ud_sm-3.8.0/xx_sent_ud_sm-3.8.0-py3-none-any.whl --system', check=False, quiet=True)

    # Phase 4: Fix specific dependencies
    # print("\n🔧 Fixing specific dependencies...")
    fix_cmds = [
        ("protobuf", "protobuf==3.20.3"),
        ("onnxruntime", "onnxruntime-gpu"),
        ("torchaudio", "torchaudio==2.9.1"),
        ("torchvision", "torchvision==0.24.1"),
    ]

    for uninstall, install in fix_cmds:
        run(f'uv pip uninstall {uninstall} --system', check=False, quiet=True)
        run(f'uv pip install {install} --system', check=False, quiet=True)

    # print("\n" + "=" * 50)
    # print("🎉 Custom nodes installation complete!")


if __name__ == "__main__":
    main()
