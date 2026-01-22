import subprocess
import os
from pathlib import Path

def run(cmd: str):
    """Execute command and print output"""
    print(f"\n🚀 RUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def aria_download(url: str, output_file: str, output_dir: str, max_conn: int = 16):
    """
    Ultra-fast download with aria2c for LARGE files
    -x: max connections per server
    -s: split download into N parts
    -k: min split size (1M = 1MB chunks)
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
        f'--max-download-limit=0 --console-log-level=warn '
        f'--allow-overwrite=true --auto-file-renaming=false '
        f'"{url}" -o "{output_file}" -d "{output_dir}"'
    )
    
    print(f"\n⚡ Downloading {output_file} with 16 connections...")
    subprocess.run(cmd, shell=True, check=True)
    return True

def hf_snapshot_download(repo_id: str, local_dir: str, patterns: list = None):
    """
    Download multiple files from HuggingFace repo in parallel
    """
    from huggingface_hub import snapshot_download
    
    print(f"\n📦 HF Snapshot Download: {repo_id}")
    print(f"📁 Destination: {local_dir}")
    
    snapshot_download(
        repo_id=repo_id,
        local_dir=local_dir,
        max_workers=10,  # 10 files in parallel
        resume_download=True,
        allow_patterns=patterns if patterns else None,
        ignore_patterns=["*.md", ".gitattributes", "*.txt"] if not patterns else None
    )
    print(f"✅ HF download completed!")

# ============================================
# PHASE 1: LARGE FILES (>10GB) - ARIA2C
# ============================================
LARGE_FILES = [
    {
        "url": "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/Wan22Animate/Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors",
        "filename": "Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors",
        "output_dir": "/content/ComfyUI/models/diffusion_models",
        "size_gb": 17
    },
    {
        "url": "https://huggingface.co/Kijai/WanVideo_comfy/resolve/6714d2392c4a3a2119834b8d45c5666c9bf9328c/Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors",
        "filename": "Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors",
        "output_dir": "/content/ComfyUI/models/diffusion_models",
        "size_gb": 17
    },
    {
        "url": "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1-T2V-14B_fp8_e4m3fn.safetensors",
        "filename": "Wan2_1-T2V-14B_fp8_e4m3fn.safetensors",
        "output_dir": "/content/ComfyUI/models/diffusion_models",
        "size_gb": 15
    },
]

# ============================================
# PHASE 2: MEDIUM + SMALL FILES - HF SNAPSHOT
# ============================================
# Nếu bạn đã upload tất cả model lên 1 HF repo
HF_REPO_CONFIG = {
    "repo_id": "huyl3-cpu/sd_comfy_models",  # Thay bằng repo của bạn
    "local_dir": "/content/ComfyUI/models",
    # Patterns to include (chỉ lấy những file này)
    "patterns": [
        # Text encoders
        "text_encoders/umt5-xxl-enc-fp8_e4m3fn.safetensors",
        # Diffusion models (medium size)
        "diffusion_models/ditto_global_style_comfy.safetensors",
        "diffusion_models/Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors",
        "diffusion_models/Wan2_1-InfiniteTalk-Multi_fp8_e4m3fn_scaled_KJ.safetensors",
        "diffusion_models/MelBandRoformer_fp32.safetensors",
        # Detection
        "detection/vitpose_h_wholebody_model.onnx",
        "detection/vitpose_h_wholebody_data.bin",
        "detection/yolov10m.onnx",
        # Loras
        "loras/WAN22_MoCap_fullbodyCOPY_ED.safetensors",
        "loras/WanAnimate_relight_lora_fp16.safetensors",
        "loras/Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors",
        "loras/FullDynamic_Ultimate_Fusion_Elite.safetensors",
        "loras/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors",
        "loras/Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors",
        # VAE
        "vae/wan_2.1_vae.safetensors",
        # CLIP Vision
        "clip_vision/clip_vision_h.safetensors",
    ]
}

# ============================================
# ALTERNATIVE: Manual download for each file
# ============================================
MEDIUM_SMALL_FILES = [
    # Text encoders
    ("https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors", 
     "umt5-xxl-enc-fp8_e4m3fn.safetensors", "/content/ComfyUI/models/text_encoders"),
    
    # Diffusion models
    ("https://huggingface.co/QingyanBai/Ditto_models/resolve/main/models_comfy/ditto_global_style_comfy.safetensors", 
     "ditto_global_style_comfy.safetensors", "/content/ComfyUI/models/diffusion_models"),
    ("https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/InfiniteTalk/Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors", 
     "Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors", "/content/ComfyUI/models/diffusion_models"),
    ("https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/InfiniteTalk/Wan2_1-InfiniteTalk-Multi_fp8_e4m3fn_scaled_KJ.safetensors", 
     "Wan2_1-InfiniteTalk-Multi_fp8_e4m3fn_scaled_KJ.safetensors", "/content/ComfyUI/models/diffusion_models"),
    ("https://huggingface.co/Kijai/MelBandRoFormer_comfy/resolve/main/MelBandRoformer_fp32.safetensors", 
     "MelBandRoformer_fp32.safetensors", "/content/ComfyUI/models/diffusion_models"),
    
    # Detection
    ("https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_model.onnx", 
     "vitpose_h_wholebody_model.onnx", "/content/ComfyUI/models/detection"),
    ("https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_data.bin", 
     "vitpose_h_wholebody_data.bin", "/content/ComfyUI/models/detection"),
    ("https://huggingface.co/Wan-AI/Wan2.2-Animate-14B/resolve/main/process_checkpoint/det/yolov10m.onnx", 
     "yolov10m.onnx", "/content/ComfyUI/models/detection"),
    
    # Loras
    ("https://huggingface.co/banhkeomath2/wan22/resolve/main/WAN22_MoCap_fullbodyCOPY_ED.safetensors", 
     "WAN22_MoCap_fullbodyCOPY_ED.safetensors", "/content/ComfyUI/models/loras"),
    ("https://huggingface.co/banhkeomath2/wan22/resolve/main/WanAnimate_relight_lora_fp16.safetensors", 
     "WanAnimate_relight_lora_fp16.safetensors", "/content/ComfyUI/models/loras"),
    ("https://huggingface.co/banhkeomath2/wan22/resolve/main/Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors", 
     "Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors", "/content/ComfyUI/models/loras"),
    ("https://huggingface.co/banhkeomath2/wan22/resolve/main/FullDynamic_Ultimate_Fusion_Elite.safetensors", 
     "FullDynamic_Ultimate_Fusion_Elite.safetensors", "/content/ComfyUI/models/loras"),
    ("https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors", 
     "lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors", "/content/ComfyUI/models/loras"),
    ("https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors", 
     "Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors", "/content/ComfyUI/models/loras"),
    
    # VAE
    ("https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors", 
     "wan_2.1_vae.safetensors", "/content/ComfyUI/models/vae"),
    
    # CLIP Vision
    ("https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors", 
     "clip_vision_h.safetensors", "/content/ComfyUI/models/clip_vision"),
]

def main():
    print("=" * 80)
    print("🚀 HYBRID OPTIMIZED DOWNLOAD - ABSOLUTE MAXIMUM SPEED")
    print("=" * 80)
    print("\n📊 Strategy:")
    print("  Phase 1: Large files (>10GB) → Aria2c with 16 connections (sequential)")
    print("  Phase 2: Medium+Small files → HuggingFace parallel download")
    print("\n⏱️  Estimated total time: ~18-23 minutes")
    print("=" * 80)
    
    run("bash -c 'source /content/env.txt || true'")
    
    # ========================================
    # PHASE 1: LARGE FILES WITH ARIA2C
    # ========================================
    print("\n" + "=" * 80)
    print("⚡ PHASE 1: DOWNLOADING LARGE FILES (49GB)")
    print("=" * 80)
    
    large_total = sum(f["size_gb"] for f in LARGE_FILES)
    print(f"📦 {len(LARGE_FILES)} large files, ~{large_total}GB total")
    print(f"⏱️  Estimated time: ~15-18 minutes\n")
    
    for idx, file_info in enumerate(LARGE_FILES, 1):
        print(f"\n{'─' * 80}")
        print(f"[{idx}/{len(LARGE_FILES)}] {file_info['filename']} ({file_info['size_gb']}GB)")
        print(f"{'─' * 80}")
        aria_download(
            file_info["url"],
            file_info["filename"],
            file_info["output_dir"],
            max_conn=16
        )
    
    print("\n✅ Phase 1 completed!")
    
    # ========================================
    # PHASE 2: MEDIUM + SMALL FILES
    # ========================================
    print("\n" + "=" * 80)
    print("📦 PHASE 2: DOWNLOADING MEDIUM + SMALL FILES (~20GB)")
    print("=" * 80)
    print(f"⏱️  Estimated time: ~5-7 minutes\n")
    
    # Option A: If you have HF repo with all models
    USE_HF_REPO = False  # Set to True if you uploaded models to HF
    
    if USE_HF_REPO:
        print("🔄 Using HuggingFace snapshot_download (parallel)...")
        try:
            hf_snapshot_download(
                HF_REPO_CONFIG["repo_id"],
                HF_REPO_CONFIG["local_dir"],
                HF_REPO_CONFIG["patterns"]
            )
        except Exception as e:
            print(f"⚠️  HF download failed: {e}")
            print("Falling back to manual download...\n")
            USE_HF_REPO = False
    
    # Option B: Manual download with aria2c parallel
    if not USE_HF_REPO:
        print("🔄 Using aria2c parallel download (5 files at once)...")
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        def download_task(args):
            url, filename, output_dir = args
            return aria_download(url, filename, output_dir, max_conn=8)
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(download_task, task): task for task in MEDIUM_SMALL_FILES}
            
            completed = 0
            for future in as_completed(futures):
                task = futures[future]
                try:
                    future.result()
                    completed += 1
                    print(f"✅ Progress: {completed}/{len(MEDIUM_SMALL_FILES)}")
                except Exception as e:
                    print(f"❌ Error: {task[1]} - {e}")
    
    print("\n✅ Phase 2 completed!")
    
    # ========================================
    # CREATE SYMLINKS FOR DUPLICATES
    # ========================================
    print("\n" + "=" * 80)
    print("🔗 Creating symlinks for duplicate files...")
    print("=" * 80)
    
    vae_src = "/content/ComfyUI/models/vae/wan_2.1_vae.safetensors"
    vae_dst = "/content/ComfyUI/models/loras/wan_2.1_vae.safetensors"
    
    if os.path.exists(vae_src) and not os.path.exists(vae_dst):
        import shutil
        shutil.copy2(vae_src, vae_dst)
        print(f"📋 Copied: {vae_dst}")
    
    # ========================================
    # SUMMARY
    # ========================================
    print("\n" + "=" * 80)
    print("✅ ALL DOWNLOADS COMPLETED!")
    print("=" * 80)
    print(f"📁 Models location: /content/ComfyUI/models/")
    print(f"💾 Total downloaded: ~70GB")
    print(f"⚡ Download method: Hybrid (Aria2c + HF parallel)")
    print("=" * 80)

if __name__ == "__main__":
    main()
