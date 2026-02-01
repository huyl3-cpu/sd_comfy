import os
import subprocess
import sys
from pathlib import Path

# Target directory containing custom nodes
CUSTOM_NODES_DIR = "/content/ComfyUI/custom_nodes"

def install_requirements_with_uv():
    print("Installing Custom Nodes Requirements using uv")
    print(f"Target: {CUSTOM_NODES_DIR}")
    print("=" * 50)

    if not os.path.exists(CUSTOM_NODES_DIR):
        print(f"Directory not found: {CUSTOM_NODES_DIR}")
        return

    # Find all requirements.txt files
    req_files = list(Path(CUSTOM_NODES_DIR).rglob("requirements.txt"))
    
    print(f"Found {len(req_files)} requirements.txt files.")
    
    success_count = 0
    fail_count = 0

    # Get current python executable to target the right environment
    python_exe = sys.executable

    for req_file in req_files:
        node_name = req_file.parent.name
        print(f"\nInstalling for: {node_name}")
        
        # Construct uv command
        # uv pip install -r <req_file> --python <python_exe>
        cmd = [
            "uv", "pip", "install", 
            "-r", str(req_file), 
            "--python", python_exe
        ]
        
        try:
            # Run uv
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8', 
                errors='replace' # Handle potential encoding issues
            )
            print(f"  [OK] Success")
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"  [FAILED] Failed")
            # Safely print stderr handling encoding
            error_msg = e.stderr.strip()
            try:
                print(f"  Error output: {error_msg}")
            except UnicodeEncodeError:
                print(f"  Error output: {error_msg.encode('ascii', 'replace').decode('ascii')}")
            fail_count += 1
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            fail_count += 1

    print("\n" + "=" * 50)
    print(f"Summary: {success_count} succeeded, {fail_count} failed")
    print("Done!")

if __name__ == "__main__":
    install_requirements_with_uv()
