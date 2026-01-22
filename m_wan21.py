import subprocess

def run(cmd):
    print(f"\n RUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

run("bash -c 'source /content/env.txt || true'")

### Large Files
run(
    'aria2c -x 16 -s 16 -k 1M "https://huggingface.co/QingyanBai/Ditto_models/resolve/main/models_comfy/ditto_global_style_comfy.safetensors" '
    '-o "ditto_global_style_comfy.safetensors" '
    # '-d /content/ComfyUI/models/diffusion_models'
)

run(
    'aria2c -x 16 -s 16 -k 1M "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1-T2V-14B_fp8_e4m3fn.safetensors" '
    '-o "Wan2_1-T2V-14B_fp8_e4m3fn.safetensors" '
    # '-d /content/ComfyUI/models/diffusion_models'
)

run(
    'aria2c -x 16 -s 16 -k 1M "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors" '
    '-o "umt5-xxl-enc-fp8_e4m3fn.safetensors" '
    # '-d /content/ComfyUI/models/text_encoders'
)

### Small Files
run(
    'aria2c -x 16 -s 16 -k 1M "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors" '
    '-o "wan_2.1_vae.safetensors" '
    # '-d /content/ComfyUI/models/vae'
)

run(
    'aria2c -x 16 -s 16 -k 1M "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors" '
    '-o "Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors" '
    # '-d /content/ComfyUI/models/loras'
)

run(
    'aria2c -x 16 -s 16 -k 1M "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors" '
    '-o "lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors" '
    # '-d /content/ComfyUI/models/loras'
)

print("\n✅ Tất cả model đã được tải xuống xong!")
