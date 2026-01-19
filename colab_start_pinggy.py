#@title 🚀 2A. Start ComfyUI - Pinggy { display-mode: "form" }
#@markdown ### Cấu hình Pinggy
PINGGY_TOKEN = "rrkChZfV3L1@pro.pinggy.io" #@param {type:"string"}
PINGGY_PORT = "9999" #@param {type:"string"}

# Cài đặt dependencies
!pip install -r /content/ComfyUI/requirements.txt
!pip install watchdog vtracer torchsde replicate llama-cpp-python
!pip install flash-attn --no-build-isolation
!pip install transformers==4.57.3

# Cấu hình Pinggy
PINGGY_LOCAL_PORT = f"{PINGGY_PORT}:localhost:4300"
CONF = "/content/sd_comfy/user.conf"

# Tạo file cấu hình
import os
with open(CONF, "w") as f:
    f.write(PINGGY_TOKEN.strip() + "\n")
    f.write(PINGGY_LOCAL_PORT.strip() + "\n")

# Chạy Pinggy
%run /content/sd_comfy/pinggy.py

# Khởi động ComfyUI
%cd /content/
!python /content/ComfyUI/main.py --listen 0.0.0.0 --port 8188 --dont-print-server --disable-metadata
