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
PINGGY_USER = ""
PINGGY_PASS = ""
# Password protection is configured in Pinggy Dashboard -> Token settings
# Not passed via command line (avoids 403 when not configured in dashboard)

COMFY_CMD = (
    f"/content/ComfyUI/main.py "
    f"--listen 0.0.0.0 --port {COMFYUI_PORT} "
    f"--disable-smart-memory --reserve-vram 1 --gpu-only {EXTRA_ARGS}"
).strip()

# ─────────────────────────────────────────────────────────────
# SAFE PRINT — must be defined BEFORE stop signals are sent so
# that existing threads can still call it during shutdown.
# ─────────────────────────────────────────────────────────────
def _safe_print(msg: str) -> None:
    """Strip surrogate characters before printing (avoids Jupyter UnicodeEncodeError)."""
    clean = str(msg).encode('utf-8', errors='replace').decode('utf-8', errors='replace')
    print(clean)

# ─────────────────────────────────────────────────────────────
# STOP OLD THREADS — signal any previous %run to exit cleanly
# This prevents multiple daemon threads when cell is re-run
# ─────────────────────────────────────────────────────────────
_STOP_KEY = "__sd_comfy_stop__"
_stop_event = threading.Event()
try:
    from IPython import get_ipython as _gip
    _ip = _gip()
    if _ip and _STOP_KEY in _ip.user_ns:
        _ip.user_ns[_STOP_KEY].set()   # tell old thread to quit
        try:
            time.sleep(1)               # brief grace period — allow old threads to exit
        except KeyboardInterrupt:
            pass                        # ignore interrupt during grace period
    if _ip:
        _ip.user_ns[_STOP_KEY] = _stop_event
except Exception:
    pass

# ─────────────────────────────────────────────────────────────
# Shared state
# ─────────────────────────────────────────────────────────────
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
    """Return the first Pinggy HTTPS URL found in text, or None.

    Pinggy CLI/SSH outputs http:// URLs even when HTTPS Only is configured.
    We match both http:// and https://, then always return https:// version.
    """
    # Match http or https for all known Pinggy URL formats:
    #   Pro:  http(s)://xxx.a.pinggy.link
    #   Free: http(s)://xxx-IP.run.pinggy-free.link
    #   Old:  http(s)://xxx.free.pinggy.link / xxx.pinggy.link
    patterns = [
        r'https?://[a-zA-Z0-9\-]+\.a\.pinggy\.link',
        r'https?://[a-zA-Z0-9\-\.]+\.pinggy-free\.link',
        r'https?://[a-zA-Z0-9\-]+\.free\.pinggy\.link',
        r'https?://[a-zA-Z0-9\-]+\.pinggy\.link',
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            url = m.group(0)
            # Always return https:// (HTTPS Only configured in Pinggy Dashboard)
            if url.startswith('http://'):
                url = 'https://' + url[7:]
            return url
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
        if os.access(PINGGY_CLI_PATH, os.X_OK):
            return
        os.remove(PINGGY_CLI_PATH)  # remove corrupt/non-executable file

    _safe_print("[Pinggy] Installing Pinggy CLI (one-time ~5MB)...")
    # Try curl first (handles GitHub release redirects better), then wget fallback
    ret = os.system(
        f"(curl -fsSL -o {PINGGY_CLI_PATH} '{PINGGY_CLI_URL}' "
        f"|| wget -q -L -O {PINGGY_CLI_PATH} '{PINGGY_CLI_URL}') "
        f"&& chmod +x {PINGGY_CLI_PATH}"
    )
    if ret == 0 and os.path.exists(PINGGY_CLI_PATH) and os.access(PINGGY_CLI_PATH, os.X_OK):
        # Sanity-check: verify it's a real binary (not an HTML error page)
        size = os.path.getsize(PINGGY_CLI_PATH)
        if size > 100_000:  # should be at least ~100KB
            _safe_print(f"[Pinggy] Pinggy CLI installed OK ({size // 1024}KB).")
            return
        os.remove(PINGGY_CLI_PATH)  # too small = download failed
    if os.path.exists(PINGGY_CLI_PATH):
        os.remove(PINGGY_CLI_PATH)
    _safe_print("[Pinggy] WARNING: CLI install failed - using SSH fallback.")


def _pinggy_worker(token: str) -> None:
    """Wait for ComfyUI then start Pinggy tunnel.

    Uses Pinggy CLI (preferred) or SSH (fallback).
    CLI: plain token (CLI handles reconnect natively, +force causes warning).
    SSH: TOKEN+force to force-close existing tunnels.
    """
    global public_url, _tunnel_proc

    # Capture _safe_print locally to avoid NameError if module is re-executed
    # while this thread is still running from a previous %run invocation.
    _print = _safe_print

    _wait_comfyui(COMFYUI_PORT)
    _install_pinggy_cli()

    host_info = token.split("@")[1] if "@" in token else token
    _print(f"[Pinggy] Starting tunnel -> {host_info}")

    parts = token.strip().split("@", 1)
    # CLI: plain token (no +force — causes 'Unknown extended option' warning)
    cli_host  = token.strip()
    # SSH: TOKEN+force to force-close existing tunnels
    ssh_host  = (f"{parts[0]}+force@{parts[1]}"
                 if len(parts) == 2 and "+force" not in parts[0]
                 else token.strip())

    # Prefer Pinggy CLI; fall back to SSH if CLI install failed
    use_cli = os.path.exists(PINGGY_CLI_PATH)

    # Detect token type from host: free.pinggy.io vs pro.pinggy.io
    is_pro = "pro.pinggy.io" in token

    if use_cli:
        # Dashboard HTTPS Only toggle handles HTTPS server-side — no need to
        # pass x:https. The -t flag requires a real PTY which Colab does not
        # provide ("Pseudo-terminal will not be allocated" warning).
        cmd = [
            PINGGY_CLI_PATH,
            "-p", "443",
            f"-R0:localhost:{COMFYUI_PORT}",
            "-o", "StrictHostKeyChecking=no",
            "-o", "ServerAliveInterval=30",
            cli_host,   # plain token — HTTPS + Force handled via dashboard
        ]
    else:
        # SSH fallback: +force in username to terminate stale tunnels.
        # HTTPS handled by Pinggy Dashboard HTTPS Only toggle (server-side).
        # Omit -t/x:https: -t requires real PTY unavailable in Colab.
        cmd = [
            "ssh",
            "-p", "443",
            f"-R0:127.0.0.1:{COMFYUI_PORT}",
            "-o", "StrictHostKeyChecking=no",
            "-o", "ServerAliveInterval=30",
            "-o", "ServerAliveCountMax=3",
            ssh_host,   # +force in username to terminate existing tunnel
        ]


    # CLI has built-in autoreconnect; outer loop is only a crash-recovery backup
    RECONNECT_DELAY = 120 if use_cli else 30

    _print(f"[Pinggy] Using {'CLI' if use_cli else 'SSH fallback'} | {'Pro' if is_pro else 'Free'} token")

    # Stop watcher: forcefully kill tunnel process when stop_event fires.
    # This unblocks readline() which would otherwise block indefinitely.
    def _stop_watcher():
        _stop_event.wait()          # blocks until stop_event.set() is called
        try:
            global _tunnel_proc     # must be explicit in nested function
            if _tunnel_proc:
                _tunnel_proc.terminate()
        except (NameError, Exception):
            pass
    threading.Thread(target=_stop_watcher, daemon=True).start()

    while not _stop_event.is_set():
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
            _print(f"[Pinggy] Failed to start tunnel: {e}")
            time.sleep(RECONNECT_DELAY)
            continue

        for raw_bytes in iter(_tunnel_proc.stdout.readline, b""):
            if _stop_event.is_set():
                _tunnel_proc.terminate()
                break

            line = raw_bytes.decode('utf-8', errors='replace').strip()
            line = _ANSI_RE.sub('', line)  # strip VT100/ANSI from SSH -tt terminal mode

            # Skip noise lines
            if "RB:" in line and "SB:" in line:
                continue
            if "Unable to initiate the TUI" in line:
                continue  # suppress noisy CLI warning - expected in headless mode
            if not line:
                continue

            safe = line
            if "@" in token:
                safe = safe.replace(token.split("@")[0], "[TOKEN]")
            _print(f"[Pinggy] {safe}")

            if "already active" in line:
                _print("[Pinggy] Conflict — 'force' will close it on reconnect.")
                _print("[Pinggy] Or terminate at: https://dashboard.pinggy.io/activetunnels")

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

        if _stop_event.is_set():
            _print("[Pinggy] Stopped (new run detected).")
            break

        # Process ended — reconnect after delay
        ret = _tunnel_proc.poll() if _tunnel_proc else -1
        if ret is not None and ret != 0:
            _print(f"[Pinggy] Disconnected (exit {ret}), reconnecting in {RECONNECT_DELAY}s...")
        else:
            _print(f"[Pinggy] Ended, reconnecting in {RECONNECT_DELAY}s...")
        public_url = None
        _tunnel_proc = None
        time.sleep(RECONNECT_DELAY)


# ─────────────────────────────────────────────────────────────
# TUNNEL: CLOUDFLARE
# ─────────────────────────────────────────────────────────────

def _cloudflare_worker() -> None:
    global public_url, _tunnel_proc

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

    # Stop watcher: kill cloudflare process when stop_event fires
    def _cf_stop_watcher():
        _stop_event.wait()
        try:
            global _tunnel_proc
            if _tunnel_proc:
                _tunnel_proc.terminate()
        except (NameError, Exception):
            pass
    threading.Thread(target=_cf_stop_watcher, daemon=True).start()

    _tunnel_proc = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", f"http://localhost:{COMFYUI_PORT}"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    for raw_line in iter(_tunnel_proc.stdout.readline, ""):
        if _stop_event.is_set():
            _tunnel_proc.terminate()
            break
        line = _ANSI_RE.sub("", raw_line).strip()  # strip ANSI codes
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

    if _tunnel_proc.poll() is None:
        _tunnel_proc.wait()


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
        args=(PINGGY_TOKEN,),
        daemon=True
    )
else:
    t = threading.Thread(target=_cloudflare_worker, daemon=True)

t.start()

# ── Cleanup previous ComfyUI instance ─────────────────────────
# Old ComfyUI subprocess survives kernel restart and holds port + db lock.
# Use -9 (SIGKILL) for immediate kill; lsof catches any process on the port.
_safe_print(f"[SD-Comfy] Stopping any existing ComfyUI process...")
os.system("pkill -9 -f 'ComfyUI/main.py' 2>/dev/null || true")
os.system(
    f"PID=$(lsof -t -i:{COMFYUI_PORT} 2>/dev/null); "
    f"[ -n \"$PID\" ] && kill -9 $PID 2>/dev/null || true"
)
# Remove SQLite WAL/SHM lock files (prevents 'cannot acquire lock' error)
os.system("rm -f /content/ComfyUI/user/comfyui.db-wal "
          "/content/ComfyUI/user/comfyui.db-shm 2>/dev/null || true")
time.sleep(2)  # wait for port to fully release

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
