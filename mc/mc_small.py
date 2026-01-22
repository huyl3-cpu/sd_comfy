"""
mc_small.py - Download FILES NHỎ (<2GB) cho MC vào thư mục hiện tại
BỎ đường dẫn lưu (không có -d) để download về /content/mc/
Sau đó dùng mv để di chuyển về đúng vị trí
"""

import subprocess
import os

def run(cmd: str):
    print(f"\n RUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

run("bash -c 'source /content/env.txt || true'")

print("""
{'='*70}
📦 MC - FILES NHỎ (<2GB)
Download về thư mục hiện tại: /content/mc/
{'='*70}
""")

# MelBandRoformer_fp32.safetensors - 1.9GB
print("\n📥 Downloading MelBandRoformer_fp32.safetensors (1.9GB)...")
run(
    'aria2c "https://huggingface.co/Kijai/MelBandRoFormer_comfy/resolve/main/MelBandRoformer_fp32.safetensors" '
    '-o "MelBandRoformer_fp32.safetensors"'
)

# clip_vision_h.safetensors - 1.3GB
print("\n📥 Downloading clip_vision_h.safetensors (1.3GB)...")
run(
    'aria2c "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors" '
    '-o "clip_vision_h.safetensors"'
)

print(f"""
{'='*70}
✅ Hoàn thành download files nhỏ cho MC!
{'='*70}

📂 Files đã download vào: /content/mc/
   - MelBandRoformer_fp32.safetensors (1.9GB)
   - clip_vision_h.safetensors (1.3GB)

🚀 BƯỚC TIẾP THEO:
   1. Upload thư mục /content/mc/ lên HuggingFace:
      !huggingface-cli upload banhkeomath2/mc /content/mc --repo-type=model
   
   2. Sau khi download về, di chuyển files về đúng vị trí:
      !mv /content/mc/MelBandRoformer_fp32.safetensors /content/ComfyUI/models/diffusion_models/
      !mv /content/mc/clip_vision_h.safetensors /content/ComfyUI/models/clip_vision/

{'='*70}
""")
