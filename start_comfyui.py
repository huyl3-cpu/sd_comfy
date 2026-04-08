"""
SD Comfy - Start ComfyUI with Tunnel
=====================================
All-in-one script: tunnel setup + ComfyUI launch.
No external config files needed.

Usage in Colab cell:
    Tunnel_Type  = "Pinggy"                    # or "Cloudflare"
    Pinggy_token = "TOKEN@pro.pinggy.io"
    %run /content/sd_comfy/start_comfyui.py
"""

# ─────────────────────────────────────────────────────────────
# CONFIGURATION — override these in the Colab cell BEFORE %run
# ─────────────────────────────────────────────────────────────
import builtins as _builtins

def _cfg(name: str, default):
    """Read variable from IPython/caller namespace, fallback to default."""
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip and name in ip.user_ns:
            return ip.user_ns[name]
    except Exception:
        pass
    return _builtins.__dict__.get(name, default)

TUNNEL_TYPE   = _cfg("Tunnel_Type",   "Pinggy")                   # "Pinggy" | "Cloudflare"
PINGGY_TOKEN  = _cfg("Pinggy_token",  "TOKEN@pro.pinggy.io")      # set in cell
COMFYUI_PORT  = _cfg("Comfy_Port",    8188)
EXTRA_ARGS    = _cfg("Comfy_ExtraArgs", "")                        # optional extra ComfyUI flags

COMFY_CMD = (
    f"/content/ComfyUI/main.py "
    f"--listen 0.0.0.0 --port {COMFYUI_PORT} "
    f"--disable-smart-memory --reserve-vram 1 --gpu-only {EXTRA_ARGS}"
).strip()

# ─────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────
import os
import re
import socket
import subprocess
import threading
import time

# Shared state
public_url   = None
_tunnel_proc = None


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def _is_port_open(port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True
    except OSError:
        return False


def _wait_comfyui(port: int, poll: int = 2) -> None:
    """Block until ComfyUI is accepting connections."""
    print(f"⏳ Waiting for ComfyUI on port {port}...")
    waited = 0
    while not _is_port_open(port):
        time.sleep(poll)
        waited += poll
        if waited % 10 == 0:
            print(f"   Still waiting... ({waited}s elapsed)")
    print("✅ ComfyUI is ready!")
    time.sleep(1)  # brief grace period


def _extract_pinggy_url(text: str):
    """Return the first Pinggy HTTPS URL found in text, or None."""
    patterns = [
        r'https://[a-zA-Z0-9\-]+\.a\.pinggy\.link',
        r'https://[a-zA-Z0-9\-]+\.free\.pinggy\.link',
        r'https://[a-zA-Z0-9\-]+\.pinggy\.link',
        r'https://[a-zA-Z0-9\-]+\.a\.free\.pinggy\.link',
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(0)
    return None


def _print_url_banner(url: str) -> None:
    bar = "█" * 62
    print(f"\n{bar}")
    print(f"█{'':^60}█")
    print(f"█{'  🌐  COMFYUI IS ONLINE':^60}█")
    print(f"█{'':^60}█")
    print(f"█  \033[1;93m{url:<58}\033[0m█")
    print(f"█{'':^60}█")
    print(f"█  \033[90mClick the link above to open ComfyUI\033[0m{'':<23}█")
    print(f"█{'':^60}█")
    print(f"{bar}\n")


# ─────────────────────────────────────────────────────────────
# TUNNEL: PINGGY
# ─────────────────────────────────────────────────────────────

def _pinggy_worker(token: str) -> None:
    """Wait for ComfyUI, then open Pinggy SSH reverse tunnel."""
    global public_url, _tunnel_proc

    _wait_comfyui(COMFYUI_PORT)

    host_info = token.split("@")[1] if "@" in token else token
    print(f"🔗 Starting Pinggy tunnel → {host_info}")

    # SSH command matching Pinggy dashboard recommendation:
    #   ssh -p 443 -R0:localhost:<PORT> -o StrictHostKeyChecking=no
    #       -o ServerAliveInterval=30  TOKEN@pro.pinggy.io
    #
    # Security notes (configure in Pinggy Dashboard → Advanced):
    #   • HTTPS only     : ON  → forces HTTPS, no unencrypted HTTP
    #   • Password Protect: ON  → basic auth before anyone can reach ComfyUI
    #   • Keep Alive     : ON  → stable connection
    #   • Web Debugger   : OFF → avoid traffic inspection
    cmd = [
        "ssh", "-T",
        "-p", "443",
        f"-R0:localhost:{COMFYUI_PORT}",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-o", "ServerAliveCountMax=3",
        "-o", "ConnectTimeout=30",
        "-o", "ExitOnForwardFailure=yes",
        token.strip(),
    ]

    try:
        _tunnel_proc = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except Exception as e:
        print(f"❌ Failed to start Pinggy: {e}")
        return

    for raw_line in iter(_tunnel_proc.stdout.readline, ""):
        line = raw_line.strip()

        # Skip bandwidth stats (noise)
        if "RB:" in line and "SB:" in line:
            continue

        if line:
            # Redact token from console output
            safe = line.replace(token.split("@")[0], "[TOKEN]") if "@" in token else line
            print(f"🌐 {safe}")

        url = _extract_pinggy_url(line)
        if url and not public_url:
            public_url = url
            _print_url_banner(url)
            # Expose to IPython namespace so cell can read it
            try:
                from IPython import get_ipython
                ip = get_ipython()
                if ip:
                    ip.user_ns["public_url"] = url
            except Exception:
                pass
            break   # URL captured; keep tunnel alive via process (not this loop)

    # Keep thread alive while tunnel process runs
    if _tunnel_proc:
        _tunnel_proc.wait()


# ─────────────────────────────────────────────────────────────
# TUNNEL: CLOUDFLARE
# ─────────────────────────────────────────────────────────────

def _cloudflare_worker() -> None:
    global public_url

    if not os.path.exists("/usr/local/bin/cloudflared"):
        print("⬇ Installing cloudflared...")
        os.system(
            "wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/"
            "cloudflared-linux-amd64.deb "
            "&& dpkg -i cloudflared-linux-amd64.deb > /dev/null "
            "&& rm -f cloudflared-linux-amd64.deb"
        )
        print("✅ cloudflared installed")

    _wait_comfyui(COMFYUI_PORT)
    print("🔗 Starting Cloudflare tunnel...")

    p = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", f"http://localhost:{COMFYUI_PORT}"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    for raw_line in iter(p.stdout.readline, ""):
        line = raw_line.strip()
        m = re.search(r"https://[^\s]+\.trycloudflare\.com", line)
        if m and not public_url:
            public_url = m.group()
            # Expose to IPython
            try:
                from IPython import get_ipython
                ip = get_ipython()
                if ip:
                    ip.user_ns["public_url"] = public_url
            except Exception:
                pass
            _print_url_banner(public_url)
            break

    if p.poll() is None:
        p.wait()


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

print("=" * 62)
print(f"  SD Comfy — Start ComfyUI  |  Tunnel: {TUNNEL_TYPE}")
print("=" * 62)

# ── Start tunnel in background ────────────────────────────────
if TUNNEL_TYPE == "Pinggy":
    if "TOKEN@" in PINGGY_TOKEN or not PINGGY_TOKEN.strip():
        raise SystemExit("❌ Set Pinggy_token in the cell before running!")
    t = threading.Thread(target=_pinggy_worker, args=(PINGGY_TOKEN,), daemon=True)
else:
    t = threading.Thread(target=_cloudflare_worker, daemon=True)

t.start()

# ── Launch ComfyUI ─────────────────────────────────────────────
os.chdir("/content/")
print(f"\n🚀 Launching ComfyUI on port {COMFYUI_PORT}...\n")

_comfy_proc = subprocess.Popen(
    f"python {COMFY_CMD}",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    universal_newlines=True,
)

_printed_link  = False
_comfyui_ready = False

for _line in iter(_comfy_proc.stdout.readline, ""):
    print(_line, end="")

    if not _comfyui_ready and (
        "To see the GUI go to" in _line or "FETCH ComfyRegistry Data" in _line
    ):
        _comfyui_ready = True

    # Print public link once both ComfyUI + tunnel are ready
    if _comfyui_ready and not _printed_link and public_url:
        time.sleep(2)
        print(f"\n\n\033[1;96m🌐 COMFYUI PUBLIC LINK: {public_url}\033[0m\n")
        _printed_link = True
