"""
download_large_files.py - Download TẤT CẢ FILES LỚN (>2GB)
Tổng hợp từ: m_ditto, m_mc, m_wan22, m_wan212
"""

import subprocess

def run(cmd: str):
    print(f"\n RUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

run("bash -c 'source /content/env.txt || true'")

print("""
{'='*70}
📦 DOWNLOAD FILES LỚN (>2GB)
Tổng hợp từ: m_ditto, m_mc, m_wan22, m_wan212
{'='*70}
""")

# ================================================================
# DIFFUSION MODELS - FILES LỚN
# ================================================================

print("\n🔷 DIFFUSION MODELS (Files >2GB)\n")

# 1. ditto_global_style_comfy.safetensors - 5.4GB
# Nguồn: m_ditto, m_wan212
run(
    'aria2c "https://huggingface.co/QingyanBai/Ditto_models/resolve/main/models_comfy/ditto_global_style_comfy.safetensors" '
    '-o "ditto_global_style_comfy.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)
print("✅ ditto_global_style_comfy.safetensors (~5.4GB) - Từ: m_ditto, m_wan212")

# 2. Wan2_1-T2V-14B_fp8_e4m3fn.safetensors - 15GB
# Nguồn: m_ditto, m_wan212
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1-T2V-14B_fp8_e4m3fn.safetensors" '
    '-o "Wan2_1-T2V-14B_fp8_e4m3fn.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)
print("✅ Wan2_1-T2V-14B_fp8_e4m3fn.safetensors (~15GB) - Từ: m_ditto, m_wan212")

# 3. Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors - 17GB
# Nguồn: m_wan22, m_wan212
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/Wan22Animate/Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors" '
    '-o "Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)
print("✅ Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors (~17GB) - Từ: m_wan22, m_wan212")

# 4. Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors - 8GB
# Nguồn: m_mc
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/InfiniteTalk/Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors" '
    '-o "Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)
print("✅ Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors (~8GB) - Từ: m_mc")

# 5. Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors - 17GB
# Nguồn: m_mc
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/6714d2392c4a3a2119834b8d45c5666c9bf9328c/Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors" '
    '-o "Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)
print("✅ Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors (~17GB) - Từ: m_mc")

# ================================================================
# TEXT ENCODERS - FILES LỚN
# ================================================================

print("\n🔷 TEXT ENCODERS (Files >2GB)\n")

# 6. umt5-xxl-enc-fp8_e4m3fn.safetensors - 4.8GB
# Nguồn: m_ditto, m_mc, m_wan22, m_wan212 (DÙNG CHUNG)
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors" '
    '-o "umt5-xxl-enc-fp8_e4m3fn.safetensors" '
    '-d /content/ComfyUI/models/text_encoders'
)
print("✅ umt5-xxl-enc-fp8_e4m3fn.safetensors (~4.8GB) - Từ: m_ditto, m_mc, m_wan22, m_wan212 (DÙNG CHUNG)")

# ================================================================
# LORAS - FILES LỚN
# ================================================================

print("\n🔷 LORAS (Files >2GB)\n")

# 7. lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors - 3.2GB
# Nguồn: m_ditto, m_mc, m_wan22, m_wan212 (DÙNG CHUNG)
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors" '
    '-o "lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors" '
    '-d /content/ComfyUI/models/loras'
)
print("✅ lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors (~3.2GB) - Từ: m_ditto, m_mc, m_wan22, m_wan212")

# 8. Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors - 2.1GB
# Nguồn: m_ditto, m_wan22, m_wan212
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors" '
    '-o "Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors" '
    '-d /content/ComfyUI/models/loras'
)
print("✅ Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors (~2.1GB) - Từ: m_ditto, m_wan22, m_wan212")

# ================================================================
# VAE - FILES LỚN
# ================================================================

print("\n🔷 VAE (Files >2GB)\n")

# 9. wan_2.1_vae.safetensors - 2.6GB
# Nguồn: m_ditto, m_mc, m_wan212
run(
    'aria2c "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors" '
    '-o "wan_2.1_vae.safetensors" '
    '-d /content/ComfyUI/models/vae'
)
print("✅ wan_2.1_vae.safetensors (~2.6GB) - Từ: m_ditto, m_mc, m_wan212")

# Copy VAE to loras folder (wan22, wan212 cần)
run(
    'aria2c "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors" '
    '-o "wan_2.1_vae.safetensors" '
    '-d /content/ComfyUI/models/loras'
)
print("✅ wan_2.1_vae.safetensors (~2.6GB) - Copy to loras - Từ: m_wan22, m_wan212")

# ================================================================
# SUMMARY
# ================================================================

print(f"""
{'='*70}
✅ HOÀN THÀNH DOWNLOAD FILES LỚN!
{'='*70}

📊 TỔNG KẾT:
   ✅ Diffusion Models: 5 files (~62GB)
      - ditto_global_style_comfy.safetensors (5.4GB)
      - Wan2_1-T2V-14B_fp8_e4m3fn.safetensors (15GB)
      - Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors (17GB)
      - Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors (8GB)
      - Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors (17GB)
   
   ✅ Text Encoders: 1 file (~5GB)
      - umt5-xxl-enc-fp8_e4m3fn.safetensors (4.8GB)
   
   ✅ Loras: 2 files (~5GB)
      - lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors (3.2GB)
      - Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors (2.1GB)
   
   ✅ VAE: 1 file (~3GB)
      - wan_2.1_vae.safetensors (2.6GB) + copy to loras

💾 TỔNG DUNG LƯỢNG: ~75GB
⏱️  THỜI GIAN: ~25-30 phút

📂 Nguồn:
   - m_ditto: 4 files
   - m_mc: 5 files  
   - m_wan22: 5 files
   - m_wan212: 9 files (tất cả)

{'='*70}
""")
