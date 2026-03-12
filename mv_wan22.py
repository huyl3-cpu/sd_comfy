import subprocess
import os

def run(cmd):
    # print(f"\nRUN: {cmd}")  # Hidden
    subprocess.run(cmd, shell=True, check=True)

source_root = "/content/wan22"

files_to_move = [
    ("yolov10m.onnx", "/content/ComfyUI/models/detection"),
    ("vitpose_h_wholebody_data.bin", "/content/ComfyUI/models/detection"),
    ("vitpose_h_wholebody_model.onnx", "/content/ComfyUI/models/detection"),
    ("clip_vision_h.safetensors", "/content/ComfyUI/models/clip_vision"),
    ("WAN22_MoCap_fullbodyCOPY_ED.safetensors", "/content/ComfyUI/models/loras"),
    ("Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors", "/content/ComfyUI/models/loras"),
    ("lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors", "/content/ComfyUI/models/loras"),
    ("WanAnimate_relight_lora_fp16.safetensors", "/content/ComfyUI/models/loras"),
    ("FullDynamic_Ultimate_Fusion_Elite.safetensors", "/content/ComfyUI/models/loras"),
    ("Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors", "/content/ComfyUI/models/loras"),
    ("Wan2.2-Fun-A14B-InP-LOW-HPS2.1_resized_dynamic_avg_rank_15_bf16.safetensors", "/content/ComfyUI/models/loras"),
    ("Wan2.2-Fun-A14B-InP-low-noise-HPS2.1.safetensors", "/content/ComfyUI/models/loras"),
    ("lightx2v_I2V_14B_480p_cfg_step_distill_rank128_bf16.safetensors", "/content/ComfyUI/models/loras"),
    ("Wan21_I2V_14B_lightx2v_cfg_step_distill_lora_rank64.safetensors", "/content/ComfyUI/models/loras"),
    ("wan_2.1_vae.safetensors", "/content/ComfyUI/models/vae"),
    ("Wan2_2-Animate-14B_bf16.safetensors", "/content/ComfyUI/models/diffusion_models"),
    ("umt5-xxl-enc-fp8_e4m3fn.safetensors", "/content/ComfyUI/models/text_encoders"),
]

# print(f"🚀 Bắt đầu di chuyển {len(files_to_move)} file từ {source_root}...")  # Hidden

for filename, dest_dir in files_to_move:
    source_path = f"{source_root}/{filename}"
    
    if not os.path.exists(dest_dir):
        run(f"mkdir -p {dest_dir}")
    
    check_cmd = f"test -f {source_path}"
    try:
        subprocess.run(check_cmd, shell=True, check=True)
        run(f"mv {source_path} {dest_dir}/")
    except subprocess.CalledProcessError:
        print(f"⚠️  Không tìm thấy file nguồn: {filename} - Bỏ qua.")

# print("\n✅ Hoàn tất di chuyển file!")  # Hidden
