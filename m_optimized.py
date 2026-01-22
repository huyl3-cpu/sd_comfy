import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

def run(cmd: str):
    """Execute command and print output"""
    print(f"\n🚀 RUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def aria_download(url: str, output_file: str, output_dir: str, max_conn: int = 16):
    """
    Ultra-fast download with aria2c
    -x: max connections per server
    -s: split download into N parts
    -k: min split size (1M = 1MB chunks)
    -j: max concurrent downloads
    --file-allocation=none: fastest on Linux
    --retry-wait=2: wait 2s before retry
    -m 5: max retries
    """
    output_path = os.path.join(output_dir, output_file)
    
    # Skip if already exists
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path) / (1024**3)  # GB
        print(f"✅ SKIP: {output_file} ({file_size:.2f}GB) already exists")
        return True
    
    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = (
        f'aria2c -x {max_conn} -s {max_conn} -k 1M '
        f'--file-allocation=none --retry-wait=2 -m 5 '
        f'--max-download-limit=0 '
        f'--allow-overwrite=true --auto-file-renaming=false '
        f'"{url}" -o "{output_file}" -d "{output_dir}"'
    )
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except Exception as e:
        print(f"❌ FAILED: {output_file} - {e}")
        return False

def create_symlink(src: str, dst: str):
    """Create symlink for duplicate files"""
    if os.path.exists(dst):
        print(f"✅ SKIP: {dst} already exists")
        return
    
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        # Try symlink first (Linux/Mac)
        os.symlink(src, dst)
        print(f"🔗 SYMLINK: {dst} -> {src}")
    except:
        # Fallback to copy on Windows/Colab
        import shutil
        shutil.copy2(src, dst)
        print(f"📋 COPY: {dst} <- {src}")

# ============================================
# ĐỊNH NGHĨA TẤT CẢ MODELS
# ============================================
# Format: (url, filename, output_dir, size_gb, priority)
# priority: 1=highest (large files first), 2=medium, 3=low

MODELS = [
    # ========== PRIORITY 1: FILE LỚN (>10GB) ==========
    ("https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/Wan22Animate/Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors", 
     "Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors", 
     "/content/ComfyUI/models/diffusion_models", 17, 1),
    
    ("https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1-T2V-14B_fp8_e4m3fn.safetensors", 
     "Wan2_1-T2V-14B_fp8_e4m3fn.safetensors", 
     "/content/ComfyUI/models/diffusion_models", 15, 1),
    
    ("https://huggingface.co/Kijai/WanVideo_comfy/resolve/6714d2392c4a3a2119834b8d45c5666c9bf9328c/Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors", 
     "Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors", 
     "/content/ComfyUI/models/diffusion_models", 17, 1),
    
    # ========== PRIORITY 2: FILE TRUNG BÌNH (2-10GB) ==========
    ("https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors", 
     "umt5-xxl-enc-fp8_e4m3fn.safetensors", 
     "/content/ComfyUI/models/text_encoders", 7, 2),
    
    ("https://huggingface.co/QingyanBai/Ditto_models/resolve/main/models_comfy/ditto_global_style_comfy.safetensors", 
     "ditto_global_style_comfy.safetensors", 
     "/content/ComfyUI/models/diffusion_models", 6, 2),
    
    ("https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/InfiniteTalk/Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors", 
     "Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors", 
     "/content/ComfyUI/models/diffusion_models", 2.7, 2),
    
    ("https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/InfiniteTalk/Wan2_1-InfiniteTalk-Multi_fp8_e4m3fn_scaled_KJ.safetensors", 
     "Wan2_1-InfiniteTalk-Multi_fp8_e4m3fn_scaled_KJ.safetensors", 
     "/content/ComfyUI/models/diffusion_models", 2.7, 2),
    
    ("https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_model.onnx", 
     "vitpose_h_wholebody_model.onnx", 
     "/content/ComfyUI/models/detection", 2.5, 2),
    
    ("https://huggingface.co/banhkeomath2/wan22/resolve/main/WAN22_MoCap_fullbodyCOPY_ED.safetensors", 
     "WAN22_MoCap_fullbodyCOPY_ED.safetensors", 
     "/content/ComfyUI/models/loras", 2, 2),
    
    ("https://huggingface.co/banhkeomath2/wan22/resolve/main/WanAnimate_relight_lora_fp16.safetensors", 
     "WanAnimate_relight_lora_fp16.safetensors", 
     "/content/ComfyUI/models/loras", 1.5, 2),
    
    ("https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors", 
     "clip_vision_h.safetensors", 
     "/content/ComfyUI/models/clip_vision", 1.3, 2),
    
    ("https://huggingface.co/Kijai/MelBandRoFormer_comfy/resolve/main/MelBandRoformer_fp32.safetensors", 
     "MelBandRoformer_fp32.safetensors", 
     "/content/ComfyUI/models/diffusion_models", 1, 2),
    
    ("https://huggingface.co/banhkeomath2/wan22/resolve/main/Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors", 
     "Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors", 
     "/content/ComfyUI/models/loras", 1, 2),
    
    ("https://huggingface.co/banhkeomath2/wan22/resolve/main/FullDynamic_Ultimate_Fusion_Elite.safetensors", 
     "FullDynamic_Ultimate_Fusion_Elite.safetensors", 
     "/content/ComfyUI/models/loras", 1, 2),
    
    # ========== PRIORITY 3: FILE NHỎ (<1GB) ==========
    ("https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors", 
     "lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors", 
     "/content/ComfyUI/models/loras", 0.6, 3),
    
    ("https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors", 
     "Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors", 
     "/content/ComfyUI/models/loras", 0.2, 3),
    
    ("https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors", 
     "wan_2.1_vae.safetensors", 
     "/content/ComfyUI/models/vae", 0.2, 3),
    
    ("https://huggingface.co/Wan-AI/Wan2.2-Animate-14B/resolve/main/process_checkpoint/det/yolov10m.onnx", 
     "yolov10m.onnx", 
     "/content/ComfyUI/models/detection", 0.1, 3),
    
    ("https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_data.bin", 
     "vitpose_h_wholebody_data.bin", 
     "/content/ComfyUI/models/detection", 0.1, 3),
]

# Files cần symlink (tránh download trùng)
SYMLINKS = [
    # VAE copy to loras
    ("/content/ComfyUI/models/vae/wan_2.1_vae.safetensors", 
     "/content/ComfyUI/models/loras/wan_2.1_vae.safetensors"),
]

def download_worker(task):
    """Worker function for parallel downloads"""
    url, filename, output_dir, size, priority = task
    print(f"\n📥 [{priority}] Downloading {filename} ({size}GB)...")
    return aria_download(url, filename, output_dir, max_conn=16)

def main():
    print("=" * 80)
    print("🚀 OPTIMIZED PARALLEL DOWNLOAD - MAXIMUM SPEED")
    print("=" * 80)
    
    run("bash -c 'source /content/env.txt || true'")
    
    # Sort by priority (1=first) and size (larger first within same priority)
    sorted_models = sorted(MODELS, key=lambda x: (x[4], -x[3]))
    
    # Calculate total size
    total_size = sum(m[3] for m in sorted_models)
    print(f"\n📊 Total models: {len(sorted_models)} files, ~{total_size:.1f}GB")
    print(f"⚡ Parallel downloads: 5 files at once, 16 connections per file")
    print(f"⏱️  Estimated time: ~20-25 minutes (on good connection)\n")
    
    # Download in parallel batches - 5 concurrent downloads
    MAX_WORKERS = 5
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download_worker, task): task for task in sorted_models}
        
        completed = 0
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
                completed += 1
                print(f"\n✅ Progress: {completed}/{len(sorted_models)} completed")
            except Exception as e:
                print(f"\n❌ Error downloading {task[1]}: {e}")
    
    # Create symlinks for duplicate files
    print("\n" + "=" * 80)
    print("🔗 Creating symlinks for duplicate files...")
    print("=" * 80)
    for src, dst in SYMLINKS:
        create_symlink(src, dst)
    
    print("\n" + "=" * 80)
    print("✅ ALL DOWNLOADS COMPLETED!")
    print("=" * 80)
    print(f"📁 Models location: /content/ComfyUI/models/")
    print(f"💾 Total downloaded: ~{total_size:.1f}GB")

if __name__ == "__main__":
    main()
