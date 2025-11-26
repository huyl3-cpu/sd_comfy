import os
import subprocess
import threading
import time
import socket
import re
from IPython.display import Audio, Javascript, display
CONF = "/content/sd_comfy/user.conf"
if not os.path.exists(CONF):
    raise SystemExit("❌ Không tìm thấy user.conf — hãy chạy Bước 1 trước!")
with open(CONF, "r") as f:
    lines = [x.strip() for x in f.readlines() if x.strip()]
if len(lines) < 2:
    raise SystemExit("❌ user.conf không hợp lệ — cần 2 dòng TOKEN + LOCALPORT")
PINGGY_TOKEN      = lines[0]
PINGGY_LOCAL_PORT = lines[1]
COMFYUI_PORT      = 8188
tunnel_proc = None
tunnel_url = None
tunnel_ready = False
def extract_tunnel_url(text):
    """Extract tunnel URL from Pinggy SSH output - supports any custom domain"""
    patterns = [
        r'https://[a-zA-Z0-9\-]+\.a\.free\.pinggy\.link',
        r'https://[a-zA-Z0-9\-]+\.free\.pinggy\.link',
        r'https://[a-zA-Z0-9\-]+\.pinggy\.link',
        r'tcp://[a-zA-Z0-9\-]+\.a\.free\.pinggy\.link',
        r'tcp://[a-zA-Z0-9\-]+\.free\.pinggy\.link',
        r'tcp://[a-zA-Z0-9\-]+\.pinggy\.link',
        r'https://[a-zA-Z0-9\-\.]+\.pinggy\.[a-zA-Z]+(?:\.[a-zA-Z]+)?',
        r'tcp://[a-zA-Z0-9\-\.]+\.pinggy\.[a-zA-Z]+(?:\.[a-zA-Z]+)?',
        r'https://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?::[0-9]+)?/?',
        r'tcp://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?::[0-9]+)?/?',
        r'https://[a-zA-Z0-9\-\.]+\.ngrok\.[a-zA-Z]+',
        r'https://[a-zA-Z0-9\-\.]+\.localtunnel\.[a-zA-Z]+',
        r'https://[a-zA-Z0-9\-\.]+\.tunnel\.[a-zA-Z]+',
        r'Forwarding.*?(https://[^\s]+)',
        r'Your.*URL.*?(https://[^\s]+)',
        r'Tunnel.*URL.*?(https://[^\s]+)',
        r'Access.*?(https://[^\s]+)',
        r'Visit.*?(https://[^\s]+)',
        r'Open.*?(https://[^\s]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            url = match.group(1) if match.lastindex else match.group(0)
            if url.startswith('tcp://'):
                url = url.replace('tcp://', 'https://')
            url = url.rstrip('/')
            exclude_keywords = [
                'dashboard', 'docs', 'support', 'github', 'gitlab',
                'localhost', '127.0.0.1', 'example.com', 'test.com'
            ]
            if not any(exclude in url.lower() for exclude in exclude_keywords):
                if re.match(r'https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}', url):
                    return url
    return None
def start_pinggy_tunnel():
    """Start Pinggy SSH tunnel with configurable variables"""
    global tunnel_proc
    tunnel_proc = subprocess.Popen([
        'ssh',
        '-p', '443',
        f'-R0:localhost:{COMFYUI_PORT}',
        f'-L{PINGGY_LOCAL_PORT}',
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'ServerAliveInterval=30',
        PINGGY_TOKEN
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    return tunnel_proc
def monitor_pinggy():
    """Monitor Pinggy tunnel and extract any tunnel URL format"""
    global tunnel_url, tunnel_ready
    try:
        output_buffer = ""
        line_count = 0
        max_lines = 50
        while tunnel_proc.poll() is None and line_count < max_lines:
            line = tunnel_proc.stdout.readline()
            if line:
                line_str = line.strip()
                output_buffer += line_str + "\n"
                line_count += 1

                if line_str:
                    print(f"🌐 Pinggy: {line_str}")
                url = extract_tunnel_url(line_str)
                if url and not tunnel_url:
                    tunnel_url = url
                    tunnel_ready = True
                    break
                if any(indicator in line_str.lower() for indicator in [
                    "tunnel established", "forwarding", "connected",
                    "your url", "access your", "visit", "open", "ready"
                ]):
                    print("✅ Tunnel connection established")
                if any(error in line_str.lower() for error in [
                    "cannot listen", "connection refused", "failed",
                    "error", "authentication failed", "timeout"
                ]):
                    print(f"❌ Pinggy error: {line_str}")
                    break
        if not tunnel_url and output_buffer:
            print("🔍 Searching buffer for any tunnel URL...")
            url = extract_tunnel_url(output_buffer)
            if url:
                tunnel_url = url
                tunnel_ready = True
                print(f"\n🎉 TUNNEL URL FOUND IN BUFFER!")
                print(f"📡 Public URL: {tunnel_url}")
                print(f"🔗 Format: {url.split('://')[1].split('/')[0]}")
            else:
                print("⚠️ No tunnel URL detected in output. Raw buffer:")
                print("=" * 40)
                print(output_buffer)
                print("=" * 40)
    except Exception as e:
        print(f"❌ Pinggy monitoring error: {e}")
def iframe_thread(port):
    """Wait for ComfyUI to start and then setup Pinggy tunnel"""
    global tunnel_url
    print("⏳ Waiting for ComfyUI to start on port", port, "...")
    while True:
        time.sleep(0.5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            sock.close()
            break
        sock.close()
    print("✅ ComfyUI đã load xong, đang setup Pinggy tunnel...")
    start_pinggy_tunnel()
    tunnel_thread = threading.Thread(target=monitor_pinggy, daemon=True)
    tunnel_thread.start()
    wait_time = 0
    max_wait = 30
    while not tunnel_ready and wait_time < max_wait:
        time.sleep(1)
        wait_time += 1
    if tunnel_url:
        print(f"\n🌍 Link Pinggy truy cập ComfyUI (Random URL): {tunnel_url}")
    else:
        print("⚠️ Pinggy tunnel started but random URL not detected yet. Check output above.")
threading.Thread(target=iframe_thread, daemon=True, args=(COMFYUI_PORT,)).start()
print("🚦 Starting ComfyUI server...")