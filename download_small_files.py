"""
download_small_files.py - Download TẤT CẢ FILES NHỎ (<2GB)
Tổng hợp từ: m_ditto, m_mc, m_wan22, m_wan212
"""

import subprocess

def run(cmd: str):
    print(f"\n RUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

run("bash -c 'source /content/env.txt || true'")

print("""
{'='*70}
📦 DOWNLOAD FILES NHỎ (<2GB)
Tổng hợp từ: m_ditto, m_mc, m_wan22, m_wan212
{'='*70}
""")

# ================================================================
# DIFFUSION MODELS - FILES NHỎ
# ================================================================

print("\n🔷 DIFFUSION MODELS (Files <2GB)\n")

# 1. MelBandRoformer_fp32.safetensors - 1.9GB
# Nguồn: m_mc
run(
    'aria2c "https://huggingface.co/Kijai/MelBandRoFormer_comfy/resolve/main/MelBandRoformer_fp32.safetensors" '
    '-o "MelBandRoformer_fp32.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)
print("✅ MelBandRoformer_fp32.safetensors (~1.9GB) - Từ: m_mc")

# ================================================================
# CLIP VISION - FILES NHỎ
# ================================================================

print("\n🔷 CLIP VISION (Files <2GB)\n")

# 2. clip_vision_h.safetensors - 1.3GB
# Nguồn: m_mc, m_wan22, m_wan212
run(
    'aria2c "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors" '
    '-o "clip_vision_h.safetensors" '
    '-d /content/ComfyUI/models/clip_vision'
)
print("✅ clip_vision_h.safetensors (~1.3GB) - Từ: m_mc, m_wan22, m_wan212")

# ================================================================
# DETECTION - FILES NHỎ
# ================================================================

print("\n🔷 DETECTION (Files <2GB)\n")

# 3. yolov10m.onnx - 60MB
# Nguồn: m_wan22, m_wan212
run(
    'aria2c "https://huggingface.co/Wan-AI/Wan2.2-Animate-14B/resolve/main/process_checkpoint/det/yolov10m.onnx" '
    '-o "yolov10m.onnx" '
    '-d /content/ComfyUI/models/detection'
)
print("✅ yolov10m.onnx (~60MB) - Từ: m_wan22, m_wan212")

# 4. vitpose_h_wholebody_data.bin - 300MB
# Nguồn: m_wan22, m_wan212
run(
    'aria2c "https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_data.bin" '
    '-o "vitpose_h_wholebody_data.bin" '
    '-d /content/ComfyUI/models/detection'
)
print("✅ vitpose_h_wholebody_data.bin (~300MB) - Từ: m_wan22, m_wan212")

# 5. vitpose_h_wholebody_model.onnx - 700MB
# Nguồn: m_wan22, m_wan212
run(
    'aria2c "https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_model.onnx" '
    '-o "vitpose_h_wholebody_model.onnx" '
    '-d /content/ComfyUI/models/detection'
)
print("✅ vitpose_h_wholebody_model.onnx (~700MB) - Từ: m_wan22, m_wan212")

# ================================================================
# LORAS - FILES NHỎ
# ================================================================

print("\n🔷 LORAS (Files <2GB)\n")

# 6. WAN22_MoCap_fullbodyCOPY_ED.safetensors - 900MB
# Nguồn: m_wan22, m_wan212
run(
    'aria2c "https://huggingface.co/banhkeomath2/wan22/resolve/main/WAN22_MoCap_fullbodyCOPY_ED.safetensors" '
    '-o "WAN22_MoCap_fullbodyCOPY_ED.safetensors" '
    '-d /content/ComfyUI/models/loras'
)
print("✅ WAN22_MoCap_fullbodyCOPY_ED.safetensors (~900MB) - Từ: m_wan22, m_wan212")

# 7. Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors - 1GB
# Nguồn: m_wan22, m_wan212
run(
    'aria2c "https://huggingface.co/banhkeomath2/wan22/resolve/main/Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors" '
    '-o "Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors" '
    '-d /content/ComfyUI/models/loras'
)
print("✅ Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors (~1GB) - Từ: m_wan22, m_wan212")

# 8. WanAnimate_relight_lora_fp16.safetensors - 800MB
# Nguồn: m_wan22, m_wan212
run(
    'aria2c "https://huggingface.co/banhkeomath2/wan22/resolve/main/WanAnimate_relight_lora_fp16.safetensors" '
    '-o "WanAnimate_relight_lora_fp16.safetensors" '
    '-d /content/ComfyUI/models/loras'
)
print("✅ WanAnimate_relight_lora_fp16.safetensors (~800MB) - Từ: m_wan22, m_wan212")

# 9. FullDynamic_Ultimate_Fusion_Elite.safetensors - 1.1GB
# Nguồn: m_wan22, m_wan212
run(
    'aria2c "https://huggingface.co/banhkeomath2/wan22/resolve/main/FullDynamic_Ultimate_Fusion_Elite.safetensors" '
    '-o "FullDynamic_Ultimate_Fusion_Elite.safetensors" '
    '-d /content/ComfyUI/models/loras'
)
print("✅ FullDynamic_Ultimate_Fusion_Elite.safetensors (~1.1GB) - Từ: m_wan22, m_wan212")

# ================================================================
# INPUT IMAGES - FILES NHỎ
# ================================================================

print("\n🔷 INPUT IMAGES (Files <2GB)\n")

# 10. ComfyUI_00004_.png - 1MB
# Nguồn: m_wan212
run(
    'aria2c "https://huggingface.co/banhkeomath1/and/resolve/main/ComfyUI_00004_.png" '
    '-o "ComfyUI_00004_.png" '
    '-d /content/ComfyUI/input'
)
print("✅ ComfyUI_00004_.png (~1MB) - Từ: m_wan212")

# 11. ComfyUI_00006_.png - 1MB
# Nguồn: m_wan212
run(
    'aria2c "https://huggingface.co/banhkeomath1/and/resolve/main/ComfyUI_00006_.png" '
    '-o "ComfyUI_00006_.png" '
    '-d /content/ComfyUI/input'
)
print("✅ ComfyUI_00006_.png (~1MB) - Từ: m_wan212")

# ================================================================
# SUMMARY
# ================================================================

print(f"""
{'='*70}
✅ HOÀN THÀNH DOWNLOAD FILES NHỎ!
{'='*70}

📊 TỔNG KẾT:
   ✅ Diffusion Models: 1 file (~1.9GB)
      - MelBandRoformer_fp32.safetensors (1.9GB)
   
   ✅ CLIP Vision: 1 file (~1.3GB)
      - clip_vision_h.safetensors (1.3GB)
   
   ✅ Detection: 3 files (~1GB)
      - yolov10m.onnx (60MB)
      - vitpose_h_wholebody_data.bin (300MB)
      - vitpose_h_wholebody_model.onnx (700MB)
   
   ✅ Loras: 4 files (~3.8GB)
      - WAN22_MoCap_fullbodyCOPY_ED.safetensors (900MB)
      - Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors (1GB)
      - WanAnimate_relight_lora_fp16.safetensors (800MB)
      - FullDynamic_Ultimate_Fusion_Elite.safetensors (1.1GB)
   
   ✅ Input Images: 2 files (~2MB)
      - ComfyUI_00004_.png (1MB)
      - ComfyUI_00006_.png (1MB)

💾 TỔNG DUNG LƯỢNG: ~8GB
⏱️  THỜI GIAN: ~5-8 phút

📂 Nguồn:
   - m_mc: 2 files (MelBandRoformer, CLIP Vision)
   - m_wan22: 7 files (Detection + Loras)
   - m_wan212: 9 files (Detection + Loras + Images)

💡 LƯU Ý:
   - Files này nhanh hơn, có thể download song song
   - m_ditto chỉ có files LỚN (không có files nhỏ độc quyền ngoài images)

{'='*70}
""")
