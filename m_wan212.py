import subprocess

def run(cmd: str):
    print(f"\n RUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

run("bash -c 'source /content/env.txt || true'")
run(
    'aria2c "https://huggingface.co/QingyanBai/Ditto_models/resolve/main/models_comfy/ditto_global_style_comfy.safetensors" '
    '-o "ditto_global_style_comfy.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models'
)
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1-T2V-14B_fp8_e4m3fn.safetensors" '
    '-o "Wan2_1-T2V-14B_fp8_e4m3fn.safetensors" '
    '-d /content/ComfyUI/models/diffusion_models/'
)
run(
    'aria2c "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/Wan22Animate/Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors" '
    '-o "Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors" '
    "-d /content/ComfyUI/models/diffusion_models"
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
    'wget https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors '
    '-P /content/ComfyUI/models/loras'
)

run(
    'wget https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors '
    '-P /content/ComfyUI/models/loras'
)

run(
    "wget https://huggingface.co/banhkeomath2/wan22/resolve/main/WAN22_MoCap_fullbodyCOPY_ED.safetensors "
    "-P /content/ComfyUI/models/loras"
)

run(
    "wget https://huggingface.co/banhkeomath2/wan22/resolve/main/Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors "
    "-P /content/ComfyUI/models/loras"
)

run(
    "wget https://huggingface.co/banhkeomath2/wan22/resolve/main/WanAnimate_relight_lora_fp16.safetensors "
    "-P /content/ComfyUI/models/loras"
)

run(
    "wget https://huggingface.co/banhkeomath2/wan22/resolve/main/FullDynamic_Ultimate_Fusion_Elite.safetensors "
    "-P /content/ComfyUI/models/loras"
)
run(
    "wget https://huggingface.co/Wan-AI/Wan2.2-Animate-14B/resolve/main/process_checkpoint/det/yolov10m.onnx "
    "-P /content/ComfyUI/models/detection"
)

run(
    "wget https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_data.bin "
    "-P /content/ComfyUI/models/detection"
)

run(
    "wget https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_model.onnx "
    "-P /content/ComfyUI/models/detection"
)
run(
    "wget https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors "
    "-P /content/ComfyUI/models/clip_vision"
)
run(
    'wget https://huggingface.co/banhkeomath1/and/resolve/main/ComfyUI_00004_.png '
    '-P /content/ComfyUI/input'
)
run(
    'wget https://huggingface.co/banhkeomath1/and/resolve/main/ComfyUI_00006_.png '
    '-P /content/ComfyUI/input'
)
print("\n✅ Tất cả model đã được tải xuống xong!")

