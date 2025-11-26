# ==========================
# FILE 4.py — KHỞI TẠO PINGGY + COMFYUI
# ==========================

import os, subprocess, threading, time, socket, re
from IPython.display import Audio, Javascript, display

CONFIG_PATH = "/content/sd_comfy/user.conf"

# ==========================
# 1. ĐỌC CONFIG USER
# ==========================

if not os.path.exists(CONFIG_PATH):
    print("❌ Không tìm thấy file user.conf!")
    print("➡ Vui lòng chạy 0.py trước:")
    print("%run /content/sd_comfy/0.py")
    raise SystemExit

with open(CONFIG_PATH, "r") as f:
    lines = [x.strip() for x in f.readlines() if x.strip()]

if len(lines) < 2:
    print("❌ File user.conf không hợp lệ!")
    print("➡ Cần 2 dòng:\nTOKEN\nLOCALPORT")
    raise SystemExit

PINGGY_TOKEN = lines[0]
PINGGY_LOCAL_PORT = lines[1]

print("🔑 Token:", PINGGY_TOKEN)
print("🔌 LocalPort:", PINGGY_LOCAL_PORT)

# ==========================
# 2. KHỞI TẠO COMFYUI + TUNNEL
# ==========================

COMFYUI_PORT = 8188

os.system("pkill -f 'python.*main.py' >/dev/null 2>&1")
os.system("pkill -f 'ssh.*pinggy' >/dev/null 2>&1")

tunnel_proc = None
tunnel_url = None
tunnel_ready = False


# ==========================
# 3. BẮT URL TỪ PINGGY
# ==========================

def extract_tunnel_url(text):
    patterns = [
        r'https://[a-zA-Z0-9\-]+\.pinggy\.link',
        r'https://[a-zA-Z0-9\-]+\.free\.pinggy\.link',
        r'https://[a-zA-Z0-9\-\.]+\.pinggy\.[a-zA-Z]+',
        r'Forwarding.*?(https://[^\s]+)',
        r'Your.*URL.*?(https://[^\s]+)',
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            url = m.group(1) if m.lastindex else m.group(0)
            return url.rstrip("/")
    return None


def start_pinggy_tunnel():
    global tunnel_proc

    tunnel_proc = subprocess.Popen([
        'ssh',
        '-p', '443',
        f'-R0:localhost:{COMFYUI_PORT}',
        f'-L{PINGGY_LOCAL_PORT}',
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'ServerAliveInterval=30',
        PINGGY_TOKEN
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
       text=True, bufsize=1)

    return tunnel_proc


def monitor_pinggy():
    global tunnel_url, tunnel_ready

    try:
        buffer_output = ""
        for _ in range(60):
            line = tunnel_proc.stdout.readline()
            if not line:
                continue

            clean = line.strip()
            buffer_output += clean + "\n"

            url = extract_tunnel_url(clean)
            if url:
                tunnel_url = url
                tunnel_ready = True
                print(f"\n🌍 Public URL: {url}")
                return
    except Exception as e:
        print("❌ Tunnel error:", e)


def wait_for_comfy(port):
    print("⏳ Waiting for ComfyUI to start...")

    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex(("127.0.0.1", port))
        s.close()

        if result == 0:
            print("✔ ComfyUI started!")
            break
        time.sleep(0.4)


# ==========================
# 4. BẮT ĐẦU TẠO TUNNEL
# ==========================

def start_tunnel():
    start_pinggy_tunnel()
    threading.Thread(target=monitor_pinggy, daemon=True).start()

threading.Thread(target=lambda: (wait_for_comfy(COMFYUI_PORT), start_tunnel()), daemon=True).start()


# ==========================
# 5. CÀI COMFYUI
# ==========================

print("🔧 Installing dependencies...")
os.system("pip install -r /content/ComfyUI/requirements.txt -q")
os.system("pip install watchdog vtracer torchsde replicate -q")
os.system("pip install sageattention==2.2.0 --no-build-isolation -q")

# ==========================
# 6. PHÁT ÂM THANH KHI XONG
# ==========================

audio = "/content/sound/start.mp3"
try:
    display(Audio(audio, autoplay=True))
    display(Javascript('document.querySelector("audio").style.display="none"'))
except:
    pass

print("\n🚀 READY! ComfyUI đang chạy nền…")
print("⏳ Đợi Pinggy tạo URL…")
