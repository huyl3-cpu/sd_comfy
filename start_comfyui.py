# @title 🚀 2. Start ComfyUI { display-mode: "form" }
# @markdown ### Tunnel Settings
Tunnel_Type = "Pinggy"  # @param ["Pinggy", "Cloudflare"]
Pinggy_token = "NyiGDbViHdm@free.pinggy.io"  # @param {type:"string"}

# ── Imports ──────────────────────────────────────────────────────────────────
import os, subprocess, threading, re, time, socket

COMFYUI_PORT = 8188
COMFY_CMD = f"/content/ComfyUI/main.py --listen 0.0.0.0 --port {COMFYUI_PORT} --disable-smart-memory --reserve-vram 1 --gpu-only"

public_url = None


# ── Helper: wait for port ─────────────────────────────────────────────────────
def wait_for_port(port: int, timeout: int = 120) -> bool:
    """Block until localhost:port is open (or timeout seconds pass)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except OSError:
            time.sleep(1)
    return False


# ── Tunnel: Pinggy ────────────────────────────────────────────────────────────
if Tunnel_Type == "Pinggy":
    # Write config with ONLY the token (pinggy.py no longer needs a port line)
    os.makedirs("/content/sd_comfy", exist_ok=True)
    with open("/content/sd_comfy/user.conf", "w") as f:
        f.write(f"{Pinggy_token.strip()}\n")

    # %run executes pinggy.py in this namespace → tunnel_url / public_url
    # will be written back into this cell's globals by pinggy.py
    %run /content/sd_comfy/pinggy.py

# ── Tunnel: Cloudflare ────────────────────────────────────────────────────────
else:
    # Install cloudflared (idempotent)
    if not os.path.exists("/usr/local/bin/cloudflared"):
        print("⬇ Installing cloudflared...")
        os.system(
            "wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/"
            "cloudflared-linux-amd64.deb && dpkg -i cloudflared-linux-amd64.deb > /dev/null "
            "&& rm -f cloudflared-linux-amd64.deb"
        )
        print("✅ cloudflared installed")

    def _run_cloudflare():
        global public_url
        p = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", f"http://localhost:{COMFYUI_PORT}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        for line in iter(p.stdout.readline, ""):
            if not public_url:
                m = re.search(r"https://[^\s]+\.trycloudflare\.com", line)
                if m:
                    public_url = m.group()
                    print(f"\n\033[1;96m🌐 Cloudflare URL found: {public_url}\033[0m\n")

    threading.Thread(target=_run_cloudflare, daemon=True).start()


# ── Start ComfyUI ─────────────────────────────────────────────────────────────
%cd /content/
print(f"\n🚀 Launching ComfyUI on port {COMFYUI_PORT}...\n")

process = subprocess.Popen(
    f"python {COMFY_CMD}",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    universal_newlines=True,
)

printed_link = False
comfyui_ready = False

for line in iter(process.stdout.readline, ""):
    print(line, end="")

    # Detect when ComfyUI finished startup
    if not comfyui_ready and ("To see the GUI go to" in line or "FETCH ComfyRegistry Data" in line):
        comfyui_ready = True

    # Print public link once ComfyUI is up AND tunnel URL is available
    if comfyui_ready and not printed_link:
        # For Pinggy: public_url is set by pinggy.py in its tunnel_worker thread
        # We import the module-level variable here
        try:
            import importlib, sys
            _pinggy_mod = sys.modules.get("pinggy") or sys.modules.get("sd_comfy.pinggy")
            if _pinggy_mod and getattr(_pinggy_mod, "public_url", None):
                public_url = _pinggy_mod.public_url
        except Exception:
            pass

        if public_url:
            time.sleep(2)
            print(f"\n\n\033[1;96m🌐 COMFYUI PUBLIC LINK: {public_url}\033[0m\n")
            printed_link = True
        # else: keep waiting — Pinggy tunnel will print its own banner when ready
