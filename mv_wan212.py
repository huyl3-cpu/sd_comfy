import subprocess
import os

def run(cmd):
    print(f"\nRUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

# Nguồn: /content/wan212
source_root = "/content/wan212"

files_to_move = [
    # Diffusion Models
    ("ditto_global_style_comfy.safetensors", "/content/ComfyUI/models/diffusion_models"),
    ("Wan2_1-T2V-14B_fp8_e4m3fn.safetensors", "/content/ComfyUI/models/diffusion_models"),
    ("Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors", "/content/ComfyUI/models/diffusion_models"),
    
    # Text Encoders
    ("umt5-xxl-enc-fp8_e4m3fn.safetensors", "/content/ComfyUI/models/text_encoders"),
    
    # VAE
    ("wan_2.1_vae.safetensors", "/content/ComfyUI/models/vae"),
    
    # Loras (theo m_wan212.py, file này được map vào loras ở nhiều chỗ)
    ("wan_2.1_vae.safetensors", "/content/ComfyUI/models/loras"), # Cóp nhặt từ script gốc
    ("Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors", "/content/ComfyUI/models/loras"),
    ("lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors", "/content/ComfyUI/models/loras"),
    ("WAN22_MoCap_fullbodyCOPY_ED.safetensors", "/content/ComfyUI/models/loras"),
    ("Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors", "/content/ComfyUI/models/loras"),
    ("WanAnimate_relight_lora_fp16.safetensors", "/content/ComfyUI/models/loras"),
    ("FullDynamic_Ultimate_Fusion_Elite.safetensors", "/content/ComfyUI/models/loras"),
    
    # Detection
    ("yolov10m.onnx", "/content/ComfyUI/models/detection"),
    ("vitpose_h_wholebody_data.bin", "/content/ComfyUI/models/detection"),
    ("vitpose_h_wholebody_model.onnx", "/content/ComfyUI/models/detection"),
    
    # Clip Vision
    ("clip_vision_h.safetensors", "/content/ComfyUI/models/clip_vision"),
]

print(f"🚀 Bắt đầu di chuyển {len(files_to_move)} file từ {source_root}...")

for filename, dest_dir in files_to_move:
    source_path = f"{source_root}/{filename}"
    
    # 1. Tạo thư mục đích nếu chưa tồn tại
    run(f"mkdir -p {dest_dir}")
    
    # 2. Di chuyển file
    check_cmd = f"test -f {source_path}"
    try:
        subprocess.run(check_cmd, shell=True, check=True)
        run(f"mv {source_path} {dest_dir}/")
    except subprocess.CalledProcessError:
        print(f"⚠️  Không tìm thấy file nguồn: {filename} - Bỏ qua.")

print("\n✅ Hoàn tất di chuyển file!")
