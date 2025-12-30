import os, subprocess

def run(cmd: str, check: bool = True):
    print(f"\n$ {cmd}")
    return subprocess.run(cmd, shell=True, check=check)

try:
    from google.colab import drive 
except Exception:
    drive = None

os.chdir("/content")
run("wget -q https://huggingface.co/banhkeomath2/wan22/resolve/main/wan22.sh -O /content/wan22.sh", check=False)
run("wget -q https://huggingface.co/banhkeomath2/wan22/resolve/main/env.txt -O /content/env.txt", check=False)
run("apt-get update -y", check=False)
run("apt-get install -y aria2", check=False)
if not os.path.isdir("/content/ComfyUI"):
    run("git clone https://github.com/comfyanonymous/ComfyUI.git /content/ComfyUI", check=False)
else:
    print("✅ ComfyUI already exists, skip clone")
if drive is not None:
    try:
        drive.mount("/content/drive")
    except Exception as e:
        print("⚠ drive.mount failed:", e)
else:
    print("⚠ Not running in Colab, skip drive.mount")

env_file = "/content/env.txt"
if not os.path.isfile(env_file):
    raise FileNotFoundError(f"Missing {env_file}")

with open(env_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        os.environ[k] = v

print("✅ Loaded env.txt")
run_show("pip install xformers==0.0.32.post2 torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128")
os.chdir("/content/ComfyUI")
env_keys = [
    "dif",
    "cp",
    "LORAS_WAN22",
    "clip",
    "clipv",
    "lorasf",
    "ipadapter",
    "loras15xl",
    "cnt",
    "birefnet",
    "upscale",
    "vae",
]

created = 0
for key in env_keys:
    path = os.environ.get(key)
    if path:
        os.makedirs(path, exist_ok=True)
        print(f"✅ Created: {path} (from {key})")
        created += 1

if created == 0:
    print("⚠ No folders created. Check env.txt keys. "
          "Env variable names cannot contain '/'. Example: LORAS_WAN22=/content/ComfyUI/models/loras/wan22")

print("\n🎉 Done init step.")
