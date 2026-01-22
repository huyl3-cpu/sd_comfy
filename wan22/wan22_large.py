"""
wan22_large.py - Download FILES LỚN (>2GB) cho WAN22
Giữ nguyên đường dẫn lưu (-d)
"""

import subprocess

def run(cmd: str):
    print(f"\n RUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

run("bash -c 'source /content/env.txt || true'")

print("""
{'='*70}
📦 WAN22 - FILES LỚN (>2GB)
{'='*70}
""")

# Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors - 17GB
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/Wan22Animate/Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors" '
    '-o "Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)

# umt5-xxl-enc-fp8_e4m3fn.safetensors - 4.8GB
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors" '
    '-o "umt5-xxl-enc-fp8_e4m3fn.safetensors" '
    '-d /content/ComfyUI/models/text_encoders'
)

# lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors - 3.2GB
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors" '
    '-o "lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors" '
    '-d /content/ComfyUI/models/loras'
)

# Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors - 2.1GB
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors" '
    '-o "Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors" '
    '-d /content/ComfyUI/models/loras'
)

# wan_2.1_vae.safetensors - 2.6GB (copy to loras)
run(
    'aria2c "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors" '
    '-o "wan_2.1_vae.safetensors" '
    '-d /content/ComfyUI/models/loras'
)

print("\n✅ Hoàn thành download files lớn cho WAN22!")
