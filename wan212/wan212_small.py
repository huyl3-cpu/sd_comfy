"""
wan212_small.py - Download FILES NHỎ (<2GB) cho WAN212 vào thư mục hiện tại
BỎ đường dẫn lưu (không có -d) để download về /content/wan212/
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
📦 WAN212 - FILES NHỎ (<2GB) - TẤT CẢ
Download về thư mục hiện tại: /content/wan212/
{'='*70}
""")

# === DETECTION MODELS ===
print("\n🔷 DETECTION MODELS")

# yolov10m.onnx - 60MB
run(
    'aria2c "https://huggingface.co/Wan-AI/Wan2.2-Animate-14B/resolve/main/process_checkpoint/det/yolov10m.onnx" '
    '-o "yolov10m.onnx"'
)

# vitpose_h_wholebody_data.bin - 300MB
run(
    'aria2c "https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_data.bin" '
    '-o "vitpose_h_wholebody_data.bin"'
)

# vitpose_h_wholebody_model.onnx - 700MB
run(
    'aria2c "https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_model.onnx" '
    '-o "vitpose_h_wholebody_model.onnx"'
)

# === CLIP VISION ===
print("\n🔷 CLIP VISION")

# clip_vision_h.safetensors - 1.3GB
run(
    'aria2c "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors" '
    '-o "clip_vision_h.safetensors"'
)

# === LORAS ===
print("\n🔷 LORAS")

# WAN22_MoCap_fullbodyCOPY_ED.safetensors - 900MB
run(
    'aria2c "https://huggingface.co/banhkeomath2/wan22/resolve/main/WAN22_MoCap_fullbodyCOPY_ED.safetensors" '
    '-o "WAN22_MoCap_fullbodyCOPY_ED.safetensors"'
)

# Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors - 1GB
run(
    'aria2c "https://huggingface.co/banhkeomath2/wan22/resolve/main/Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors" '
    '-o "Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors"'
)

# WanAnimate_relight_lora_fp16.safetensors - 800MB
run(
    'aria2c "https://huggingface.co/banhkeomath2/wan22/resolve/main/WanAnimate_relight_lora_fp16.safetensors" '
    '-o "WanAnimate_relight_lora_fp16.safetensors"'
)

# FullDynamic_Ultimate_Fusion_Elite.safetensors - 1.1GB
run(
    'aria2c "https://huggingface.co/banhkeomath2/wan22/resolve/main/FullDynamic_Ultimate_Fusion_Elite.safetensors" '
    '-o "FullDynamic_Ultimate_Fusion_Elite.safetensors"'
)

# === INPUT IMAGES ===
print("\n🔷 INPUT IMAGES")

# ComfyUI_00004_.png - 1MB
run(
    'aria2c "https://huggingface.co/banhkeomath1/and/resolve/main/ComfyUI_00004_.png" '
    '-o "ComfyUI_00004_.png"'
)

# ComfyUI_00006_.png - 1MB
run(
    'aria2c "https://huggingface.co/banhkeomath1/and/resolve/main/ComfyUI_00006_.png" '
    '-o "ComfyUI_00006_.png"'
)

print(f"""
{'='*70}
✅ Hoàn thành download files nhỏ cho WAN212!
{'='*70}

📂 Files đã download vào: /content/wan212/
   🔷 Detection (3 files, ~1GB)
   🔷 CLIP Vision (1 file, ~1.3GB)
   🔷 Loras (4 files, ~3.8GB)
   🔷 Input Images (2 files, ~2MB)

🚀 BƯỚC TIẾP THEO:
   1. Upload thư mục /content/wan212/ lên HuggingFace:
      !huggingface-cli upload banhkeomath2/wan212 /content/wan212 --repo-type=model
   
   2. Sau khi download về, di chuyển files về đúng vị trí:
      !mv /content/wan212/*.onnx /content/ComfyUI/models/detection/
      !mv /content/wan212/*.bin /content/ComfyUI/models/detection/
      !mv /content/wan212/clip_vision_h.safetensors /content/ComfyUI/models/clip_vision/
      !mv /content/wan212/WAN*.safetensors /content/ComfyUI/models/loras/
      !mv /content/wan212/FullDynamic*.safetensors /content/ComfyUI/models/loras/
      !mv /content/wan212/*.png /content/ComfyUI/input/

{'='*70}
""")
