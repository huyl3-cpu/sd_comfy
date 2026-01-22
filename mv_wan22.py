import subprocess
import os

def run(cmd):
    print(f"\nRUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

# Nguồn: Tất cả file nằm trong /content/wan22
source_root = "/content/wan22"

# Danh sách file và đích đến (trích xuất từ m_wan22.py)
# Format: (filename, destination_folder)
files_to_move = [
    # Detection
    ("yolov10m.onnx", "/content/ComfyUI/models/detection"),
    ("vitpose_h_wholebody_data.bin", "/content/ComfyUI/models/detection"),
    ("vitpose_h_wholebody_model.onnx", "/content/ComfyUI/models/detection"),
    
    # Clip Vision
    ("clip_vision_h.safetensors", "/content/ComfyUI/models/clip_vision"),
    
    # Loras
    ("WAN22_MoCap_fullbodyCOPY_ED.safetensors", "/content/ComfyUI/models/loras"),
    ("Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors", "/content/ComfyUI/models/loras"),
    ("lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors", "/content/ComfyUI/models/loras"),
    ("WanAnimate_relight_lora_fp16.safetensors", "/content/ComfyUI/models/loras"),
    ("FullDynamic_Ultimate_Fusion_Elite.safetensors", "/content/ComfyUI/models/loras"),
    ("Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors", "/content/ComfyUI/models/loras"),
    ("wan_2.1_vae.safetensors", "/content/ComfyUI/models/loras"), # Theo m_wan22.py file này vào loras
    
    # Diffusion Models
    ("Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors", "/content/ComfyUI/models/diffusion_models"),
    
    # Text Encoders
    ("umt5-xxl-enc-fp8_e4m3fn.safetensors", "/content/ComfyUI/models/text_encoders"),
]

print(f"🚀 Bắt đầu di chuyển {len(files_to_move)} file từ {source_root}...")

for filename, dest_dir in files_to_move:
    source_path = f"{source_root}/{filename}"
    
    # 1. Tạo thư mục đích nếu chưa tồn tại
    run(f"mkdir -p {dest_dir}")
    
    # 2. Di chuyển file
    # Sử dụng lệnh mv (tương đương !mv trên Colab)
    # Kiểm tra file nguồn có tồn tại không để tránh lỗi
    check_cmd = f"test -f {source_path}"
    try:
        subprocess.run(check_cmd, shell=True, check=True)
        # File tồn tại, tiến hành move
        run(f"mv {source_path} {dest_dir}/")
    except subprocess.CalledProcessError:
        print(f"⚠️  Không tìm thấy file nguồn: {filename} - Bỏ qua.")

print("\n✅ Hoàn tất di chuyển file!")
