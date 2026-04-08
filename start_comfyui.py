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
# IMPORTS (must be first)
# ─────────────────────────────────────────────────────────────
import builtins as _builtins
import os
import re
import socket
import subprocess
import sys
import threading
import time

# Strip ANSI/VT100 escape sequences emitted by SSH -tt terminal mode
_ANSI_RE = re.compile(r'\x1b\[[0-9;?]*[a-zA-Z]|\x1b[^\[]')

# ─────────────────────────────────────────────────────────────
# SANITIZE sys.stdout — intercept ALL output, strip surrogates
# This MUST run before any print() to prevent Jupyter
# UnicodeEncodeError from surrogate characters in subprocess output
# ─────────────────────────────────────────────────────────────
class _SanitizingStream:
    """Wraps stdout to strip UTF-8 surrogate chars before Jupyter serializes them."""
    def __init__(self, wrapped):
        self._w = wrapped
    def write(self, s: str) -> int:
        if isinstance(s, str) and s:
            s = s.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
        return self._w.write(s)
    def flush(self):
        self._w.flush()
    def __getattr__(self, name):
        return getattr(self._w, name)

_orig_stdout = sys.stdout
sys.stdout = _SanitizingStream(sys.stdout)


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


TUNNEL_TYPE   = _cfg("Tunnel_Type",   "Pinggy")              # "Pinggy" | "Cloudflare"
PINGGY_TOKEN  = _cfg("Pinggy_token",  "TOKEN@pro.pinggy.io") # set in cell
COMFYUI_PORT  = _cfg("Comfy_Port",    8188)
EXTRA_ARGS    = _cfg("Comfy_ExtraArgs", "")                   # optional extra ComfyUI flags

# ── Pinggy Basic Auth (Password Protect) ──────────────────────
# These are the credentials users enter in the BROWSER when visiting the Pinggy URL.
# Do NOT put them in the cell form — store in Colab Secrets instead:
#   Runtime → Manage secrets → Add: PINGGY_USER / PINGGY_PASS
# Or set them as hidden variables BEFORE %run in your cell:
#   Pinggy_user = "your_user" ; Pinggy_pass = "your_pass"
PINGGY_USER = (
    os.environ.get("PINGGY_USER")
    or _cfg("Pinggy_user", "")
)
PINGGY_PASS = (
    os.environ.get("PINGGY_PASS")
    or _cfg("Pinggy_pass", "")
)

COMFY_CMD = (
    f"/content/ComfyUI/main.py "
    f"--listen 0.0.0.0 --port {COMFYUI_PORT} "
    f"--disable-smart-memory --reserve-vram 1 --gpu-only {EXTRA_ARGS}"
).strip()

# ─────────────────────────────────────────────────────────────
# Shared state
# ─────────────────────────────────────────────────────────────
public_url   = None
_tunnel_proc = None


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def _safe_print(msg: str) -> None:
    """Strip surrogate characters before printing to avoid Jupyter UnicodeEncodeError."""
    clean = msg.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
    print(clean)


def _is_port_open(port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True
    except OSError:
        return False


def _wait_comfyui(port: int, poll: int = 2) -> None:
    """Block until ComfyUI is accepting connections."""
    _safe_print(f"[SD-Comfy] Waiting for ComfyUI on port {port}...")
    waited = 0
    while not _is_port_open(port):
        time.sleep(poll)
        waited += poll
        if waited % 10 == 0:
            _safe_print(f"[SD-Comfy] Still waiting... ({waited}s elapsed)")
    _safe_print("[SD-Comfy] ComfyUI is ready!")
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
    bar = "=" * 62
    _safe_print(f"\n{bar}")
    _safe_print(f"  [SD-Comfy] COMFYUI IS ONLINE")
    _safe_print(f"  {url}")
    _safe_print(f"  (Click the link above to open ComfyUI)")
    _safe_print(f"{bar}\n")


# ─────────────────────────────────────────────────────────────
# TUNNEL: PINGGY
# ─────────────────────────────────────────────────────────────

PINGGY_CLI_PATH = "/usr/local/bin/pinggy"
PINGGY_CLI_URL  = (
    "https://github.com/Pinggy-io/cli-js/releases/download/v0.3.9/pinggy-linux-x64"
)


def _install_pinggy_cli() -> None:
    """Download Pinggy CLI binary for Linux x86-64 if not already installed."""
    if os.path.exists(PINGGY_CLI_PATH):
        # Verify it's actually executable
        if os.access(PINGGY_CLI_PATH, os.X_OK):
            return
        os.remove(PINGGY_CLI_PATH)  # remove corrupt file

    _safe_print("[Pinggy] Installing Pinggy CLI (one-time ~5MB)...")
    # -L follows GitHub release redirects, -f fails on HTTP errors
    ret = os.system(
        f"wget -q -L -f -O {PINGGY_CLI_PATH} '{PINGGY_CLI_URL}' "
        f"&& chmod +x {PINGGY_CLI_PATH} "
        f"&& echo 'Pinggy CLI OK'"
    )
    if ret == 0 and os.path.exists(PINGGY_CLI_PATH) and os.access(PINGGY_CLI_PATH, os.X_OK):
        _safe_print("[Pinggy] Pinggy CLI installed OK.")
    else:
        # Clean up partial download
        if os.path.exists(PINGGY_CLI_PATH):
            os.remove(PINGGY_CLI_PATH)
        _safe_print("[Pinggy] WARNING: CLI install failed - using SSH fallback.")


def _pinggy_worker(token: str, user: str = "", passwd: str = "") -> None:
    """Wait for ComfyUI then start Pinggy tunnel.

    Uses Pinggy CLI (preferred) or SSH (fallback).
    TOKEN+force@pro.pinggy.io forces-close any existing tunnel on connect.
    Remote opts x:https and b:user:pass are passed as CLI remote args.
    """
    global public_url, _tunnel_proc

    _wait_comfyui(COMFYUI_PORT)
    _install_pinggy_cli()

    host_info = token.split("@")[1] if "@" in token else token
    _safe_print(f"[Pinggy] Starting tunnel -> {host_info}")
    if user:
        _safe_print(f"[Pinggy] Password Protect: ON (user: {user})")
    _safe_print("[Pinggy] HTTPS only: ON | Force: ON")

    # Build TOKEN+force@pro.pinggy.io
    # 'force' is a USERNAME keyword per Pinggy docs:
    #   https://pinggy.io/docs/usages/ (section 4)
    # Syntax: TOKEN+force@pro.pinggy.io
    parts = token.strip().split("@", 1)
    if len(parts) == 2 and "+force" not in parts[0]:
        cli_host = f"{parts[0]}+force@{parts[1]}"
    else:
        cli_host = token.strip()

    # Prefer Pinggy CLI; fall back to SSH if CLI install failed
    use_cli = os.path.exists(PINGGY_CLI_PATH)

    if use_cli:
        # Pinggy CLI: clean binary, no PTY issues, supports all remote opts
        # https://pinggy.io/docs/cli/
        base = [
            PINGGY_CLI_PATH,
            "-p", "443",
            f"-R0:127.0.0.1:{COMFYUI_PORT}",
            "-o", "StrictHostKeyChecking=no",
            cli_host,
        ]
    else:
        # SSH fallback with -tt (force PTY for Pinggy interactive mode)
        base = [
            "ssh", "-tt",
            "-p", "443",
            f"-R0:127.0.0.1:{COMFYUI_PORT}",
            "-o", "StrictHostKeyChecking=no",
            "-o", "ServerAliveInterval=30",
            "-o", "ServerAliveCountMax=3",
            cli_host,
        ]

    # Remote options passed after hostname:
    #   x:https      -> HTTPS only redirect
    #   b:user:pass  -> Basic Auth (browser password prompt)
    remote_opts = ["x:https"]
    if user and passwd:
        remote_opts.append(f"b:{user}:{passwd}")

    cmd = base + remote_opts
    RECONNECT_DELAY = 30  # longer delay to avoid Pinggy rate-limit

    _safe_print(f"[Pinggy] Using {'CLI' if use_cli else 'SSH fallback'}")

    while True:
        try:
            _tunnel_proc = subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=False,   # binary mode → manual decode → no surrogate issues
                bufsize=0,
            )
        except Exception as e:
            _safe_print(f"[Pinggy] Failed to start tunnel: {e}")
            time.sleep(RECONNECT_DELAY)
            continue

        for raw_bytes in iter(_tunnel_proc.stdout.readline, b""):
            line = raw_bytes.decode('utf-8', errors='replace').strip()
            line = _ANSI_RE.sub('', line)  # strip VT100/ANSI from SSH -tt terminal mode

            # Skip noise (bandwidth stats lines)
            if "RB:" in line and "SB:" in line:
                continue
            # Skip blank lines after ANSI stripping
            if not line:
                continue

            safe = line
            if passwd:
                safe = safe.replace(passwd, "[PASS]")
            if "@" in token:
                safe = safe.replace(token.split("@")[0], "[TOKEN]")
            _safe_print(f"[Pinggy] {safe}")

            if "already active" in line:
                _safe_print("[Pinggy] Conflict - 'force' will close it on reconnect.")
                _safe_print("[Pinggy] Or terminate at: https://dashboard.pinggy.io/activetunnels")

            url = _extract_pinggy_url(line)
            if url and not public_url:
                public_url = url
                _print_url_banner(url)
                try:
                    from IPython import get_ipython
                    ip = get_ipython()
                    if ip:
                        ip.user_ns["public_url"] = url
                except Exception:
                    pass

        # Process ended — reconnect after delay
        ret = _tunnel_proc.poll() if _tunnel_proc else -1
        if ret is not None and ret != 0:
            _safe_print(f"[Pinggy] Disconnected (exit {ret}), reconnecting in {RECONNECT_DELAY}s...")
        else:
            _safe_print(f"[Pinggy] Ended, reconnecting in {RECONNECT_DELAY}s...")
        public_url = None
        _tunnel_proc = None
        time.sleep(RECONNECT_DELAY)


# ─────────────────────────────────────────────────────────────
# TUNNEL: CLOUDFLARE
# ─────────────────────────────────────────────────────────────

def _cloudflare_worker() -> None:
    global public_url

    if not os.path.exists("/usr/local/bin/cloudflared"):
        _safe_print("[Cloudflare] Installing cloudflared...")
        os.system(
            "wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/"
            "cloudflared-linux-amd64.deb "
            "&& dpkg -i cloudflared-linux-amd64.deb > /dev/null "
            "&& rm -f cloudflared-linux-amd64.deb"
        )
        _safe_print("[Cloudflare] cloudflared installed")

    _wait_comfyui(COMFYUI_PORT)
    _safe_print("[Cloudflare] Starting tunnel...")

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
_safe_print(f"  SD Comfy | ComfyUI + {TUNNEL_TYPE} Tunnel")
print("=" * 62)

# ── Start tunnel in background ────────────────────────────────
if TUNNEL_TYPE == "Pinggy":
    if "TOKEN@" in PINGGY_TOKEN or not PINGGY_TOKEN.strip():
        raise SystemExit("❌ Set Pinggy_token in the cell before running!")
    t = threading.Thread(
        target=_pinggy_worker,
        args=(PINGGY_TOKEN, PINGGY_USER, PINGGY_PASS),
        daemon=True
    )
else:
    t = threading.Thread(target=_cloudflare_worker, daemon=True)

t.start()

# ── Launch ComfyUI ─────────────────────────────────────────────
os.chdir("/content/")
_safe_print(f"\n[SD-Comfy] Launching ComfyUI on port {COMFYUI_PORT}...\n")

_comfy_proc = subprocess.Popen(
    f"python {COMFY_CMD}",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=False,      # binary mode to prevent surrogate creation
    bufsize=0,
)

_printed_link  = False
_comfyui_ready = False

for _raw in iter(_comfy_proc.stdout.readline, b""):
    _line = _raw.decode('utf-8', errors='replace')
    _safe_print(_line.rstrip('\n'))

    if not _comfyui_ready and (
        "To see the GUI go to" in _line or "FETCH ComfyRegistry Data" in _line
    ):
        _comfyui_ready = True

    if _comfyui_ready and not _printed_link and public_url:
        time.sleep(2)
        _safe_print(f"\n[SD-Comfy] PUBLIC LINK: {public_url}\n")
        _printed_link = True
