"""
SD Comfy Custom Nodes - Colab Optimization
Two nodes for keeping Colab sessions alive and auto-reconnecting tunnels.
"""

import os
import time
import threading
import subprocess
import socket
from typing import Optional, Tuple, Any

# Global state for background threads
_keepalive_thread: Optional[threading.Thread] = None
_keepalive_running = False
_tunnel_thread: Optional[threading.Thread] = None
_tunnel_running = False
_tunnel_proc: Optional[subprocess.Popen] = None


class ColabKeepAlive:
    """
    Node to prevent Google Colab from disconnecting due to inactivity.
    Creates periodic activity to keep the session alive.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True}),
                "interval_seconds": ("INT", {
                    "default": 60,
                    "min": 30,
                    "max": 300,
                    "step": 10,
                    "display": "slider"
                }),
                "method": (["memory_touch", "file_touch", "gpu_ping"], {"default": "memory_touch"}),
            },
            "optional": {
                "any_input": ("*",),  # Passthrough for workflow chaining
            }
        }
    
    RETURN_TYPES = ("STRING", "*")
    RETURN_NAMES = ("status", "passthrough")
    FUNCTION = "execute"
    CATEGORY = "SD_Comfy/Utils"
    
    def execute(self, enabled: bool, interval_seconds: int, method: str, any_input=None) -> Tuple[str, Any]:
        global _keepalive_thread, _keepalive_running
        
        if not enabled:
            _keepalive_running = False
            return ("⏹️ KeepAlive disabled", any_input)
        
        if _keepalive_thread is not None and _keepalive_thread.is_alive():
            return (f"✅ KeepAlive running ({method}, {interval_seconds}s)", any_input)
        
        _keepalive_running = True
        
        def keepalive_worker():
            import gc
            touch_file = "/tmp/.colab_keepalive"
            
            while _keepalive_running:
                try:
                    if method == "memory_touch":
                        # Allocate and free memory to create activity
                        _ = [0] * 1000000
                        del _
                        gc.collect()
                    
                    elif method == "file_touch":
                        # Touch a temp file
                        with open(touch_file, "w") as f:
                            f.write(str(time.time()))
                    
                    elif method == "gpu_ping":
                        # Quick GPU operation if available
                        try:
                            import torch
                            if torch.cuda.is_available():
                                x = torch.zeros(1, device="cuda")
                                del x
                                torch.cuda.empty_cache()
                        except ImportError:
                            pass
                    
                    time.sleep(interval_seconds)
                    
                except Exception as e:
                    print(f"[KeepAlive] Error: {e}")
                    time.sleep(interval_seconds)
        
        _keepalive_thread = threading.Thread(target=keepalive_worker, daemon=True)
        _keepalive_thread.start()
        
        return (f"🟢 KeepAlive started ({method}, every {interval_seconds}s)", any_input)


class TunnelAutoReconnect:
    """
    Node to manage tunnel connections (Pinggy, ngrok, etc.) with auto-reconnect.
    Monitors tunnel health and automatically reconnects on failure.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True}),
                "tunnel_type": (["pinggy", "ngrok", "localtunnel", "custom"], {"default": "pinggy"}),
                "local_port": ("INT", {
                    "default": 8188,
                    "min": 1024,
                    "max": 65535,
                }),
                "check_interval": ("INT", {
                    "default": 30,
                    "min": 10,
                    "max": 120,
                    "step": 5,
                    "display": "slider"
                }),
                "max_retries": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 20,
                }),
            },
            "optional": {
                "token": ("STRING", {"default": "", "multiline": False}),
                "custom_command": ("STRING", {"default": "", "multiline": True}),
                "any_input": ("*",),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "*")
    RETURN_NAMES = ("status", "tunnel_url", "passthrough")
    FUNCTION = "execute"
    CATEGORY = "SD_Comfy/Utils"
    
    def execute(
        self, 
        enabled: bool, 
        tunnel_type: str, 
        local_port: int,
        check_interval: int,
        max_retries: int,
        token: str = "",
        custom_command: str = "",
        any_input=None
    ) -> Tuple[str, str, Any]:
        global _tunnel_thread, _tunnel_running, _tunnel_proc
        
        if not enabled:
            _tunnel_running = False
            if _tunnel_proc:
                _tunnel_proc.terminate()
                _tunnel_proc = None
            return ("⏹️ Tunnel disabled", "", any_input)
        
        # Check if already running
        if _tunnel_thread is not None and _tunnel_thread.is_alive():
            url = self._get_current_url()
            return (f"✅ Tunnel running ({tunnel_type})", url, any_input)
        
        _tunnel_running = True
        tunnel_url_holder = {"url": ""}
        
        def get_tunnel_command() -> list:
            if tunnel_type == "pinggy" and token:
                return [
                    "ssh", "-p", "443",
                    f"-R0:localhost:{local_port}",
                    "-o", "StrictHostKeyChecking=no",
                    "-o", "ServerAliveInterval=30",
                    token
                ]
            elif tunnel_type == "ngrok" and token:
                return ["ngrok", "http", str(local_port), "--authtoken", token]
            elif tunnel_type == "localtunnel":
                return ["lt", "--port", str(local_port)]
            elif tunnel_type == "custom" and custom_command:
                return custom_command.split()
            else:
                return []
        
        def is_port_available(port: int) -> bool:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result == 0
        
        def start_tunnel():
            global _tunnel_proc
            cmd = get_tunnel_command()
            if not cmd:
                return None
            
            try:
                _tunnel_proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                return _tunnel_proc
            except Exception as e:
                print(f"[Tunnel] Failed to start: {e}")
                return None
        
        def extract_url_from_output(text: str) -> Optional[str]:
            import re
            patterns = [
                r'https://[a-zA-Z0-9\-]+\.free\.pinggy\.link',
                r'https://[a-zA-Z0-9\-]+\.ngrok\.io',
                r'https://[a-zA-Z0-9\-]+\.loca\.lt',
                r'https://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?::[0-9]+)?',
            ]
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(0)
            return None
        
        def tunnel_worker():
            global _tunnel_proc
            retries = 0
            
            while _tunnel_running and retries < max_retries:
                # Wait for local service to be available
                if not is_port_available(local_port):
                    print(f"[Tunnel] Waiting for port {local_port}...")
                    time.sleep(check_interval)
                    continue
                
                # Start tunnel
                proc = start_tunnel()
                if proc is None:
                    retries += 1
                    time.sleep(check_interval)
                    continue
                
                print(f"[Tunnel] Started {tunnel_type} tunnel")
                
                # Monitor output for URL and health
                output_buffer = ""
                while _tunnel_running and proc.poll() is None:
                    try:
                        line = proc.stdout.readline()
                        if line:
                            output_buffer += line
                            print(f"[Tunnel] {line.strip()}")
                            
                            # Extract URL
                            url = extract_url_from_output(output_buffer)
                            if url:
                                tunnel_url_holder["url"] = url
                                print(f"[Tunnel] URL: {url}")
                    except Exception:
                        pass
                
                # Process ended - attempt reconnect
                if _tunnel_running:
                    retries += 1
                    print(f"[Tunnel] Disconnected. Retry {retries}/{max_retries}...")
                    time.sleep(5)
            
            if retries >= max_retries:
                print(f"[Tunnel] Max retries reached. Giving up.")
        
        _tunnel_thread = threading.Thread(target=tunnel_worker, daemon=True)
        _tunnel_thread.start()
        
        # Wait briefly for initial connection
        time.sleep(3)
        
        url = tunnel_url_holder.get("url", "")
        status = f"🟢 Tunnel starting ({tunnel_type}, port {local_port})"
        
        return (status, url, any_input)
    
    def _get_current_url(self) -> str:
        return ""  # URL is managed by background thread


# Node registration
NODE_CLASS_MAPPINGS = {
    "ColabKeepAlive": ColabKeepAlive,
    "TunnelAutoReconnect": TunnelAutoReconnect,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ColabKeepAlive": "🔋 Colab Keep Alive",
    "TunnelAutoReconnect": "🔗 Tunnel Auto Reconnect",
}
