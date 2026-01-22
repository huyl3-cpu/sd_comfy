"""
mc_large.py - Download FILES LỚN (>2GB) cho MC
Giữ nguyên đường dẫn lưu (-d)
"""

import subprocess

def run(cmd: str):
    print(f"\n RUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

run("bash -c 'source /content/env.txt || true'")

print("""
{'='*70}
📦 MC - FILES LỚN (>2GB)
{'='*70}
""")

# Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors - 8GB
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/InfiniteTalk/Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors" '
    '-o "Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)

# Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors - 17GB
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/6714d2392c4a3a2119834b8d45c5666c9bf9328c/Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors" '
    '-o "Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)

# umt5-xxl-enc-fp8_e4m3fn.safetensors - 4.8GB
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors" '
    '-o "umt5-xxl-enc-fp8_e4m3fn.safetensors" '
    '-d /content/ComfyUI/models/text_encoders'
)

# wan_2.1_vae.safetensors - 2.6GB
run(
    'aria2c "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors" '
    '-o "wan_2.1_vae.safetensors" '
    '-d /content/ComfyUI/models/vae'
)

# lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors - 3.2GB
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors" '
    '-o "lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors" '
    '-d /content/ComfyUI/models/loras'
)

print("\n✅ Hoàn thành download files lớn cho MC!")
