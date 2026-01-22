"""
ditto_large.py - Download FILES LỚN (>2GB) cho DITTO
Giữ nguyên đường dẫn lưu (-d)
"""

import subprocess

def run(cmd: str):
    print(f"\n RUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

run("bash -c 'source /content/env.txt || true'")

print("""
{'='*70}
📦 DITTO - FILES LỚN (>2GB)
{'='*70}
""")

# ditto_global_style_comfy.safetensors - 5.4GB
run(
    'aria2c "https://huggingface.co/QingyanBai/Ditto_models/resolve/main/models_comfy/ditto_global_style_comfy.safetensors" '
    '-o "ditto_global_style_comfy.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)

# Wan2_1-T2V-14B_fp8_e4m3fn.safetensors - 15GB
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1-T2V-14B_fp8_e4m3fn.safetensors" '
    '-o "Wan2_1-T2V-14B_fp8_e4m3fn.safetensors" '
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

# Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors - 2.1GB
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors" '
    '-o "Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors" '
    '-d /content/ComfyUI/models/loras'
)

# lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors - 3.2GB
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors" '
    '-o "lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors" '
    '-d /content/ComfyUI/models/loras'
)

print("\n✅ Hoàn thành download files lớn cho DITTO!")
