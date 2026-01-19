#@title 🚀 2. Start ComfyUI { display-mode: "form" }
#@markdown ## 🌐 CẤU HÌNH TUNNEL
tunnel_type = "Cloudflare" #@param ["Pinggy", "Cloudflare"]

#@markdown ---
#@markdown ##### 🔧 Cấu hình Pinggy *(chỉ cần điền nếu chọn Pinggy)*
Pinggy_token = "rrkChZfV3L1@pro.pinggy.io" #@param {type:"string"}
Pinggy_port = "9999" #@param {type:"string"}
!pip install -r /content/ComfyUI/requirements.txt
!pip install watchdog vtracer torchsde replicate llama-cpp-python
!pip install flash-attn --no-build-isolation
!pip install transformers==4.57.3
if tunnel_type == "Pinggy":
    PINGGY_LOCAL_PORT = f"{Pinggy_port}:localhost:4300"
    CONF = "/content/sd_comfy/user.conf"
    import os
    with open(CONF, "w") as f:
        f.write(Pinggy_token.strip() + "\n")
        f.write(PINGGY_LOCAL_PORT.strip() + "\n")
    %run /content/sd_comfy/pinggy.py
    %cd /content/
    !python /content/ComfyUI/main.py --listen 0.0.0.0 --port 8188 --dont-print-server --disable-metadata
elif tunnel_type == "Cloudflare":
    %cd /content/
    !wget -P ~ https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    !dpkg -i ~/cloudflared-linux-amd64.deb
    
    import subprocess, re, time, threading
    
    def start_cloudflared(port=8188, delay_sec=25):
        print("✅ ComfyUI started. Creating Cloudflare tunnel...\n")
        tunnel = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", f"http://localhost:{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        def read_output():
            url = None
            while True:
                line = tunnel.stdout.readline()
                if not line:
                    break
                if "trycloudflare.com" in line:
                    m = re.search(r"https://[^\s]+", line)
                    if m:
                        url = m.group()
                        break
            if url:
                time.sleep(delay_sec)
                print(f"\n\033[1m\033[96m🌐 COMFYUI PUBLIC LINK:\033[0m \033[1m{url}\033[0m\n")
        threading.Thread(target=read_output, daemon=True).start()
        return tunnel
    start_cloudflared(port=8188, delay_sec=45)
    !python /content/ComfyUI/main.py --listen 0.0.0.0 --port 8188 --dont-print-server --disable-metadata
