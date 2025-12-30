import os
import subprocess
import sys
DEBUG = False  
def run_silent(command):
    if DEBUG:
        subprocess.run(command, shell=True)
    else:
        subprocess.run(
            command, 
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
os.chdir("/content")
run_silent("wget https://huggingface.co/banhkeomath2/wan22/resolve/main/wan22.sh -q")
run_silent("wget https://huggingface.co/banhkeomath2/wan22/resolve/main/env.txt -q")
run_silent("apt -y install aria2")
run_silent("hf download banhkeomath2/sound --local-dir /content/sound/")
run_silent("git clone https://github.com/comfyanonymous/ComfyUI.git")
run_silent("git describe --tags")
os.chdir("/content/ComfyUI")
env_file = "/content/env.txt"
if os.path.exists(env_file):
    with open(env_file, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
dirs = [
    os.environ.get("dif"),
    os.environ.get("cp"),
    os.environ.get("loras/wan22"),
    os.environ.get("clip"),
    os.environ.get("clipv"),
    os.environ.get("lorasf"),
    os.environ.get("ipadapter"),
    os.environ.get("loras15xl"),
    os.environ.get("cnt"),
    os.environ.get("birefnet"),
    os.environ.get("upscale"),
    os.environ.get("vae"),
]
for d in dirs:
    if d:
        try:
            os.makedirs(d, exist_ok=True)
        except:
            pass
if DEBUG:
    print("✔ 1.py completed")
