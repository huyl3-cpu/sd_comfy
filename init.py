# init.py — chạy bằng: !python init.py (Google Colab)
# Auto-generated from init.ipynb

import os, subprocess, sys, time, socket, re, threading, base64

def run(cmd, check=True):
    """Run a shell command (Colab-friendly)."""
    print(f"\n$ {cmd}")
    return subprocess.run(cmd, shell=True, check=check)

# Optional: Colab-only / Notebook-only helpers
try:
    from google.colab import drive  # type: ignore
except Exception:
    drive = None

try:
    from IPython.display import Audio, Javascript, display  # type: ignore
except Exception:
    Audio = Javascript = display = None

os.chdir('/content/')
print('📁 cd /content/')
# ==============================================================
# 1) WAN22 + ENV + TUTORIAL IMAGE + SOUND + COMFYUI
# ==============================================================
run('wget https://huggingface.co/banhkeomath1/and/resolve/main/tutorial.png -P /content/ -q', check=True)
import base64, os, subprocess, threading, time, socket, re
import base64, os, subprocess, threading, time, socket, re

with open('/content/tutorial.png','rb') as f:
    html_img = 'data:image/png;base64,' + base64.b64encode(f.read()).decode()
print('✔ Tutorial encoded')

run('wget https://huggingface.co/banhkeomath2/wan22/resolve/main/wan22.sh -q', check=True)
run('wget https://huggingface.co/banhkeomath2/wan22/resolve/main/env.txt -q', check=True)
run('apt -y install aria2', check=True)
run('git clone https://github.com/comfyanonymous/ComfyUI.git', check=True)
if drive is not None:
    drive.mount('/content/drive')
else:
    print('⚠ Not in Colab: skip drive.mount')

os.chdir('/content/ComfyUI')
print('📁 cd /content/ComfyUI')
env_file = '/content/env.txt'
with open(env_file,'r') as f:
    for line in f:
        if '=' in line:
            k,v = line.strip().split('=',1)
            os.environ[k] = v

dirs = [
 os.environ.get('dif'),
 os.environ.get('cp'),
 os.environ.get('loras/wan22'),
 os.environ.get('clip'),
 os.environ.get('clipv'),
 os.environ.get('lorasf'),
 os.environ.get('ipadapter'),
 os.environ.get('loras15xl'),
 os.environ.get('cnt'),
 os.environ.get('birefnet'),
 os.environ.get('upscale'),
 os.environ.get('vae')
]
for d in dirs:
    if d:
        os.makedirs(d, exist_ok=True)
        print('Created:', d)

run('hf download banhkeomath2/sound --local-dir /content/sound/', check=True)
audio_path = '/content/sound/1.mp3'

def play_audio(p):
    if display is not None:
        display(Audio(p, autoplay=True))
    if display is not None:
        display(Javascript('document.querySelector("audio").style.display="none"'))

if display is not None:
    play_audio(audio_path)
else:
    print('🔊 Audio ready at:', audio_path)

# ==============================================================
# 2) PINGGY TUNNEL + COMFYUI AUTO START
# ==============================================================
os.chdir('/content/ComfyUI')
print('📁 cd /content/ComfyUI')
run('pkill -f "python.*main.py"', check=False)
run('pkill -f "ssh.*pinggy"', check=False)

COMFYUI_PORT = 8188
PINGGY_LOCAL_PORT = '4300:localhost:4300'
PINGGY_TOKEN = 'free.pinggy.io'

tunnel_proc = None
tunnel_url = None
tunnel_ready = False

def extract_tunnel_url(text):
    m = re.search(r"https?://[a-zA-Z0-9.-]+\\.pinggy\\.link", text)
    return m.group(0) if m else None

def start_pinggy_tunnel():
    global tunnel_proc
    cmd = f"ssh -o StrictHostKeyChecking=no -p 443 -R 0:localhost:{COMFYUI_PORT} {PINGGY_TOKEN}"
    print("▶ Starting Pinggy tunnel...")
    tunnel_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

def monitor_pinggy():
    global tunnel_url, tunnel_ready
    buf = ""
    try:
        while True:
            line = tunnel_proc.stdout.readline()
            if not line:
                break
            if "pinggy.link" in line:
                print('PINGGY:', line.strip())
                url = extract_tunnel_url(line)
                if url:
                    tunnel_url = url
                    tunnel_ready = True
                    print('\n🌍 Public URL:', tunnel_url)
                    break
            buf += line
        if not tunnel_ready:
            url = extract_tunnel_url(buf)
            if url:
                tunnel_url = url
                tunnel_ready = True
                print('\n🌍 Public URL:', tunnel_url)
    except Exception as e:
        print('Pinggy error:', e)

def iframe_thread(port):
    print('⏳ Waiting ComfyUI...')
    while True:
        time.sleep(0.5)
        s = socket.socket()
        if s.connect_ex(('127.0.0.1',port)) == 0:
            break
        s.close()
    print('✔ ComfyUI ready → creating tunnel...')
    start_pinggy_tunnel()
    threading.Thread(target=monitor_pinggy, daemon=True).start()

threading.Thread(target=iframe_thread, daemon=True, args=(COMFYUI_PORT,)).start()

run('pip install -r /content/ComfyUI/requirements.txt', check=True)
run('wget https://huggingface.co/banhkeomath1/and/resolve/main/ComfyUI_00005_.png -P /content/ComfyUI/input', check=True)
run('pip install watchdog vtracer torchsde replicate', check=True)
run('pip install sageattention==2.2.0 --no-build-isolation', check=True)

if display is not None:
    play_audio(audio_path)
else:
    print('🔊 Audio ready at:', audio_path)

print('\n🎉 INSTALL COMPLETED – READY TO RUN COMFYUI!')
