import subprocess
import os

def run(cmd):
    # print(f"\nRUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

source_root = "/content/mc"

files_to_move = [
    ("Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors", "/content/ComfyUI/models/diffusion_models"),
    ("Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors", "/content/ComfyUI/models/diffusion_models"),
    ("MelBandRoformer_fp32.safetensors", "/content/ComfyUI/models/diffusion_models"),
    ("umt5-xxl-enc-fp8_e4m3fn.safetensors", "/content/ComfyUI/models/text_encoders"),
    ("wan_2.1_vae.safetensors", "/content/ComfyUI/models/vae"),
    ("lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors", "/content/ComfyUI/models/loras"),
    ("clip_vision_h.safetensors", "/content/ComfyUI/models/clip_vision"),
]

print(f"🚀 Bắt đầu di chuyển {len(files_to_move)} file từ {source_root}...")

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

print("\n✅ Hoàn tất di chuyển file!")
