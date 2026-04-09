import subprocess
import os

def run(cmd):
    # print(f"\nRUN: {cmd}")  # Hidden
    subprocess.run(cmd, shell=True, check=True)

source_root = "/content/Multi"

files_to_move = [
    ("Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors", "/content/ComfyUI/models/loras"),
    ("qwen-image-edit-2511-multiple-angles-lora.safetensors", "/content/ComfyUI/models/loras"),
    ("qwen_2.5_vl_7b_fp8_scaled.safetensors", "/content/ComfyUI/models/text_encoders"),
    ("qwen_image_edit_2511_fp8_e4m3fn_scaled.safetensors", "/content/ComfyUI/models/diffusion_models"),
    ("qwen_image_vae.safetensors", "/content/ComfyUI/models/vae"),
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
