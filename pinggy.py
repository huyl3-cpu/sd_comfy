"""
SD Comfy - Pinggy Tunnel Script (Security Enhanced)
Auto-reconnect, token redaction, and improved error handling.
"""

import os
import subprocess
import threading
import time
import socket
import re
from typing import Optional

try:
    from IPython.display import Audio, Javascript, display
except ImportError:
    pass

# ============ Configuration ============
CONF = "/content/sd_comfy/user.conf"
COMFYUI_PORT = 8188
MAX_RETRIES = 5
RETRY_DELAY = 10

# ============ Public export for notebook ============
public_url = None  # Will be set when tunnel is ready

# ============ Global State ============
tunnel_proc: Optional[subprocess.Popen] = None
tunnel_url: Optional[str] = None
tunnel_ready = False
_tunnel_running = True


def redact_token(text: str, token: str) -> str:
    """Redact sensitive token from log output."""
    if not token or len(token) < 10:
        return text
    # Show first 4 and last 4 characters only
    redacted = f"{token[:4]}...{token[-4:]}"
    return text.replace(token, f"[REDACTED:{redacted}]")


def safe_print(message: str, token: str = "") -> None:
    """Print message with token redacted."""
    print(redact_token(message, token))


def load_config(config_path: str) -> tuple:
    """Load and validate configuration file. Returns (token,) only."""
    if not os.path.exists(config_path):
        raise SystemExit(f"❌ Config not found: {config_path}")
    
    with open(config_path, "r") as f:
        lines = [x.strip() for x in f.readlines() if x.strip() and not x.startswith("#")]
    
    if len(lines) < 1:
        raise SystemExit("❌ user.conf invalid — need at least 1 line: TOKEN")
    
    token = lines[0]
    
    # Validate token format (basic check)
    if "@" not in token and "pinggy" not in token.lower():
        print("⚠ Warning: Token format may be incorrect (expected: TOKEN@free.pinggy.io)")
    
    return token


def extract_tunnel_url(text: str) -> Optional[str]:
    """Extract tunnel URL from output - supports multiple tunnel services."""
    patterns = [
        # Pinggy patterns
        r'https://[a-zA-Z0-9\-]+\.a\.free\.pinggy\.link',
        r'https://[a-zA-Z0-9\-]+\.free\.pinggy\.link',
        r'https://[a-zA-Z0-9\-]+\.pinggy\.link',
        r'tcp://[a-zA-Z0-9\-]+\.a\.free\.pinggy\.link',
        r'tcp://[a-zA-Z0-9\-]+\.free\.pinggy\.link',
        # Cloudflare
        r'https://[a-zA-Z0-9\-]+\.trycloudflare\.com',
        # ngrok
        r'https://[a-zA-Z0-9\-]+\.ngrok\.io',
        r'https://[a-zA-Z0-9\-]+\.ngrok-free\.app',
        # localtunnel
        r'https://[a-zA-Z0-9\-]+\.loca\.lt',
        # Generic patterns
        r'Forwarding.*?(https://[^\s]+)',
        r'Your.*URL.*?(https://[^\s]+)',
        r'Tunnel.*URL.*?(https://[^\s]+)',
    ]
    
    exclude_keywords = [
        'dashboard', 'docs', 'support', 'github', 'gitlab',
        'localhost', '127.0.0.1', 'example.com', 'test.com'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            url = match.group(1) if match.lastindex else match.group(0)
            if url.startswith('tcp://'):
                url = url.replace('tcp://', 'https://')
            url = url.rstrip('/')
            
            if not any(exclude in url.lower() for exclude in exclude_keywords):
                if re.match(r'https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}', url):
                    return url
    return None


def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """Check if a port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((host, port)) == 0
    except Exception:
        return False


def start_tunnel(token: str) -> Optional[subprocess.Popen]:
    """Start Pinggy SSH reverse tunnel to expose ComfyUI.
    
    Token format:
      Free : NyiGDbViHdm@free.pinggy.io
      Pro  : fn5MdCAn86q@pro.pinggy.io
    
    '+t' appended to host disables Pinggy Password Protection (fixes 403).
    """
    global tunnel_proc
    
    # Detect host from token and append '+t' to disable password protection
    # token = "MYTOKEN@free.pinggy.io"  or  "MYTOKEN@pro.pinggy.io"
    if '@' in token:
        user_part, host_part = token.rsplit('@', 1)
        # '+t' = disable basic auth (password protection) on Pinggy
        host_with_noauth = host_part + '+t'
        ssh_target = f"{user_part}@{host_with_noauth}"
    else:
        ssh_target = token  # fallback: use as-is
    
    cmd = [
        'ssh',
        '-T',                         # disable pseudo-terminal (no TTY needed)
        '-p', '443',
        f'-R0:localhost:{COMFYUI_PORT}',
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'ServerAliveInterval=30',
        '-o', 'ServerAliveCountMax=3',
        '-o', 'ConnectTimeout=30',
        '-o', 'ExitOnForwardFailure=yes',
        ssh_target
    ]
    
    print(f"🔗 SSH → {ssh_target.split('@')[1]} (password protection: OFF)")
    
    try:
        tunnel_proc = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,  # no interactive input
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        return tunnel_proc
    except Exception as e:
        print(f"❌ Failed to start tunnel: {e}")
        return None


def monitor_tunnel(token: str) -> None:
    """Monitor tunnel output and extract URL. Sets module-level public_url."""
    global tunnel_url, tunnel_ready, public_url
    
    if tunnel_proc is None:
        return
    
    import sys
    this_module = sys.modules[__name__]
    
    try:
        output_buffer = ""
        line_count = 0
        max_lines = 100  # increase to catch URL which may appear later
        
        while tunnel_proc.poll() is None and line_count < max_lines:
            line = tunnel_proc.stdout.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            line_str = line.strip()
            # Filter out bandwidth stats (RB: ..., SB: ...)
            if "RB:" in line_str and "SB:" in line_str:
                continue
            
            # Try to extract URL
            url = extract_tunnel_url(line_str)
            
            if url and url.startswith("https://"):
                if not tunnel_url:
                    tunnel_url = url
                    public_url = url  # export for notebook cell
                    # Also set on module so notebook %run can access it
                    setattr(this_module, 'public_url', url)
                    tunnel_ready = True
                    print("\n" + "█" * 60)
                    print("█" + " " * 58 + "█")
                    print(f"█   \033[1;32mCOMFYUI PUBLIC URL\033[0m" + " " * 40 + "█")
                    print("█" + " " * 58 + "█")
                    print(f"█   \033[1;93m{tunnel_url}\033[0m")
                    print("█" + " " * 58 + "█")
                    print("█   \033[1;30m(Click the link above to open ComfyUI)\033[0m" + " " * 20 + "█")
                    print("█" + " " * 58 + "█")
                    print("█" * 60 + "\n")
                    break
                continue

            output_buffer += line_str + "\n"
            line_count += 1
            
            # Print other lines with redacted token
            if line_str:
                safe_print(f"🌐 Tunnel: {line_str}", token)
            
            # Check for errors
            if any(err in line_str.lower() for err in ["permission denied", "connection refused", "network error"]):
                safe_print(f"❌ Tunnel error: {line_str}", token)
                break
        
        # Fallback: search entire buffer
        if not tunnel_url and output_buffer:
            url = extract_tunnel_url(output_buffer)
            if url and url.startswith("https://"):
                tunnel_url = url
                public_url = url
                setattr(this_module, 'public_url', url)
                tunnel_ready = True
                print(f"\n\033[1;32m🎉 COMFYUI PUBLIC LINK: {tunnel_url}\033[0m")
    
    except Exception as e:
        print(f"❌ Monitor error: {e}")


def tunnel_worker(token: str) -> None:
    """Main tunnel worker with auto-reconnect."""
    global tunnel_url, tunnel_ready, _tunnel_running
    
    retries = 0
    
    while _tunnel_running and retries < MAX_RETRIES:
        # Wait for ComfyUI to be ready
        print(f"⏳ Waiting for ComfyUI on port {COMFYUI_PORT}...")
        waited = 0
        while _tunnel_running and not is_port_open('127.0.0.1', COMFYUI_PORT):
            time.sleep(2)
            waited += 2
            if waited % 10 == 0:
                print(f"   Still waiting... ({waited}s)")
        
        if not _tunnel_running:
            break
        
        print("✅ ComfyUI is ready! Starting Pinggy tunnel...")
        time.sleep(1)  # Brief pause to ensure ComfyUI fully initialized
        
        # Reset state
        tunnel_url = None
        tunnel_ready = False
        
        proc = start_tunnel(token)
        if proc is None:
            retries += 1
            print(f"⚠ Retry {retries}/{MAX_RETRIES} in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
            continue
        
        # Monitor output in background thread
        monitor_thread = threading.Thread(target=monitor_tunnel, args=(token,), daemon=True)
        monitor_thread.start()
        
        # Wait up to 45s for URL
        wait_time = 0
        while not tunnel_ready and wait_time < 45:
            time.sleep(1)
            wait_time += 1
        
        if not tunnel_url:
            print("⚠ Warning: Could not extract public URL within 45s")
            print("  Check raw output above for the Pinggy URL")
        
        # Keep alive until tunnel dies
        while _tunnel_running and proc.poll() is None:
            time.sleep(5)
        
        # Process died — auto-reconnect
        if _tunnel_running:
            retries += 1
            print(f"\n⚠ Tunnel disconnected. Retry {retries}/{MAX_RETRIES} in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
    
    if retries >= MAX_RETRIES:
        print("❌ Max retries reached. Giving up.")


def main():
    """Main entry point."""
    print("🚀 SD Comfy - Pinggy Tunnel (Enhanced)")
    print("=" * 50)
    
    # Load configuration (token only)
    token = load_config(CONF)
    safe_print(f"✅ Loaded config — token: {token[:4]}...{token[-8:]}", token)
    
    if "free.pinggy" in token:
        print("📌 Free Pinggy plan detected — URL may change on reconnect")
    
    # Start tunnel worker in background thread
    # It will wait for ComfyUI to be ready before connecting
    worker = threading.Thread(target=tunnel_worker, args=(token,), daemon=True)
    worker.start()
    
    print("🚦 Tunnel worker started — will connect once ComfyUI is ready...")


# Auto-run when imported via %run
main()
