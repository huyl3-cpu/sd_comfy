import subprocess

def run(cmd: str):
    print(f"\n RUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

run("bash -c 'source /content/env.txt || true'")

run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/InfiniteTalk/Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors" '
    '-o "Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)

run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/6714d2392c4a3a2119834b8d45c5666c9bf9328c/Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors" '
    '-o "Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)

run(
    'aria2c "https://huggingface.co/Kijai/MelBandRoFormer_comfy/resolve/main/MelBandRoformer_fp32.safetensors" '
    '-o "MelBandRoformer_fp32.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)

run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors" '
    '-o "umt5-xxl-enc-fp8_e4m3fn.safetensors" '
    '-d /content/ComfyUI/models/text_encoders'
)

run(
    'wget https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors '
    '-P /content/ComfyUI/models/vae/'
)

run(
    'wget https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors '
    '-P /content/ComfyUI/models/loras'
)

run(
    "wget https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors "
    "-P /content/ComfyUI/models/clip_vision"
)

print("\n✅ Tất cả model đã được tải xuống xong!")
