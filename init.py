import os
import sys
import subprocess

def run(cmd: str, check: bool = True):
    print(f"\n$ {cmd}")
    return subprocess.run(cmd, shell=True, check=check)

def run_show(cmd: str, check: bool = True):
    return run(cmd, check=check)

def has_ipython_kernel() -> bool:
    try:
        from IPython import get_ipython
        return get_ipython() is not None
    except Exception:
        return False

try:
    from google.colab import drive
except Exception:
    drive = None

os.makedirs("/content", exist_ok=True)
os.chdir("/content")
print("📁 cd /content")

run("wget -q https://huggingface.co/banhkeomath2/wan22/resolve/main/wan22.sh -O /content/wan22.sh", check=False)
run("wget -q https://huggingface.co/banhkeomath2/wan22/resolve/main/env.txt -O /content/env.txt", check=False)

run("apt-get update -y", check=False)
run("apt-get install -y aria2", check=False)

if not os.path.isdir("/content/ComfyUI"):
    run("git clone https://github.com/comfyanonymous/ComfyUI.git /content/ComfyUI", check=True)
else:
    print("✅ ComfyUI already exists, skip clone")

if drive is not None and has_ipython_kernel():
    try:
        drive.mount("/content/drive")
    except Exception as e:
        print("⚠ drive.mount failed:", e)
else:
    print("⚠ Skip drive.mount")

env_file = "/content/env.txt"
if os.path.isfile(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")
    print("✅ Loaded env.txt")
else:
    print("⚠ env.txt not found, skip loading env")

os.chdir("/content/ComfyUI")
print("📁 cd /content/ComfyUI")

env_keys = ["dif","cp","LORAS_WAN22","clip","clipv","lorasf","ipadapter","loras15xl","cnt","birefnet","upscale","vae"]
for k in env_keys:
    p = os.environ.get(k)
    if p:
        os.makedirs(p, exist_ok=True)
        print(f"✅ Created: {p}")

run(f'"{sys.executable}" -m pip install -r /content/ComfyUI/requirements.txt', check=True)

custom_nodes = "/content/ComfyUI/custom_nodes"
os.makedirs(custom_nodes, exist_ok=True)
os.chdir(custom_nodes)
print("📁 cd /content/ComfyUI/custom_nodes")

mgr_dir = os.path.join(custom_nodes, "ComfyUI-Manager")
if not os.path.isdir(mgr_dir):
    run("git clone https://github.com/Comfy-Org/ComfyUI-Manager.git", check=True)
else:
    print("✅ ComfyUI-Manager already exists, skip clone")

run(f'"{sys.executable}" -m pip install -r "{mgr_dir}/requirements.txt"', check=True)

print("\n🎉 Done.")
