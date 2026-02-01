import os
import subprocess
import concurrent.futures
from typing import List, Tuple

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

MAX_PARALLEL_CLONES = 8

def run(cmd: str, check: bool = True, quiet: bool = False):
    """Run a shell command."""
    try:
        return subprocess.run(
            cmd, 
            shell=True, 
            check=check,
            stdout=subprocess.DEVNULL if quiet else None,
            stderr=subprocess.DEVNULL if quiet else None
        )
    except subprocess.CalledProcessError:
        if not quiet:
            print(f"⚠ Command failed: {cmd}")
        return None

def clone_repo(repo_url: str, folder_name: str) -> bool:
    """Clone a repository with depth 1 if it doesn't exist."""
    target_path = os.path.join(os.getcwd(), folder_name)
    if os.path.exists(target_path) and os.path.isdir(target_path):
        print(f"  [EXISTS] {folder_name}")
        return True
    
    # Using git clone
    print(f"  [CLONING] {folder_name}...")
    result = run(f"git clone --depth 1 -q {repo_url} \"{folder_name}\"", quiet=False)
    if result and result.returncode == 0:
        print(f"  [OK] {folder_name}")
        return True
    else:
        print(f"  [FAILED] {folder_name}")
        return False

def main():
    print("ComfyUI Windows Custom Nodes Cloner")
    print("=" * 50)
    
    # Target directory
    custom_nodes_dir = "/content/ComfyUI/custom_nodes"
    if not os.path.exists(custom_nodes_dir):
        try:
            os.makedirs(custom_nodes_dir)
            print(f"Created directory: {custom_nodes_dir}")
        except OSError as e:
            print(f"Error creating directory {custom_nodes_dir}: {e}")
            return
    
    os.chdir(custom_nodes_dir)
    print(f"Working directory: {os.getcwd()}\n")
    
    print(f"Cloning {len(CUSTOM_NODES)} repositories (parallel, max {MAX_PARALLEL_CLONES})...")
    
    clone_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PARALLEL_CLONES) as executor:
        futures = {executor.submit(clone_repo, node[0], node[1]): node[1] for node in CUSTOM_NODES}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                success = future.result()
                clone_results[name] = success
            except Exception as e:
                print(f"  FAILED {name} (exception: {e})")
                clone_results[name] = False
    
    # Summary
    cloned = sum(1 for v in clone_results.values() if v)
    
    print(f"\nSummary: {cloned}/{len(CUSTOM_NODES)} cloned successfully")
    print("\n" + "=" * 50)
    print("Done!")

if __name__ == "__main__":
    main()
