"""
SD Comfy - ComfyUI Custom Nodes for Google Colab Optimization

Nodes:
- ColabKeepAlive: Prevents Google Colab from disconnecting due to inactivity
- TunnelAutoReconnect: Auto-reconnects tunnel services (Pinggy, ngrok, etc.)
"""

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

WEB_DIRECTORY = "./web"
