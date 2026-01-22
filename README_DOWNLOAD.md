# 📥 HƯỚNG DẪN DOWNLOAD - 2 FILES TỔNG HỢP

## 📋 Tổng quan

Đã tạo **2 files tổng hợp** từ 4 files gốc (m_ditto, m_mc, m_wan22, m_wan212):

| File | Số lượng | Dung lượng | Thời gian | Mô tả |
|------|----------|------------|-----------|-------|
| **`download_large_files.py`** | 9 files | ~75GB | 25-30 min | Files LỚN >2GB |
| **`download_small_files.py`** | 11 files | ~8GB | 5-8 min | Files NHỎ <2GB |

**TỔNG CỘNG**: 20 files, ~83GB, 30-40 phút

---

## 🎯 PHÂN LOẠI FILES

### 📦 **download_large_files.py** (9 files, ~75GB)

#### 🔷 Diffusion Models (5 files, ~62GB)
1. `ditto_global_style_comfy.safetensors` - **5.4GB**
   - Từ: **m_ditto, m_wan212**

2. `Wan2_1-T2V-14B_fp8_e4m3fn.safetensors` - **15GB**
   - Từ: **m_ditto, m_wan212**

3. `Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors` - **17GB**
   - Từ: **m_wan22, m_wan212**

4. `Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors` - **8GB**
   - Từ: **m_mc**

5. `Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors` - **17GB**
   - Từ: **m_mc**

#### 🔷 Text Encoders (1 file, ~5GB)
6. `umt5-xxl-enc-fp8_e4m3fn.safetensors` - **4.8GB**
   - Từ: **m_ditto, m_mc, m_wan22, m_wan212** (DÙNG CHUNG)

#### 🔷 Loras (2 files, ~5GB)
7. `lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors` - **3.2GB**
   - Từ: **m_ditto, m_mc, m_wan22, m_wan212** (DÙNG CHUNG)

8. `Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors` - **2.1GB**
   - Từ: **m_ditto, m_wan22, m_wan212**

#### 🔷 VAE (1 file, ~3GB)
9. `wan_2.1_vae.safetensors` - **2.6GB**
   - Từ: **m_ditto, m_mc, m_wan212**
   - **Note**: Cũng được copy vào `/models/loras/`

---

### 📦 **download_small_files.py** (11 files, ~8GB)

#### 🔷 Diffusion Models (1 file, ~1.9GB)
1. `MelBandRoformer_fp32.safetensors` - **1.9GB**
   - Từ: **m_mc**

#### 🔷 CLIP Vision (1 file, ~1.3GB)
2. `clip_vision_h.safetensors` - **1.3GB**
   - Từ: **m_mc, m_wan22, m_wan212**

#### 🔷 Detection (3 files, ~1GB)
3. `yolov10m.onnx` - **60MB**
   - Từ: **m_wan22, m_wan212**

4. `vitpose_h_wholebody_data.bin` - **300MB**
   - Từ: **m_wan22, m_wan212**

5. `vitpose_h_wholebody_model.onnx` - **700MB**
   - Từ: **m_wan22, m_wan212**

#### 🔷 Loras (4 files, ~3.8GB)
6. `WAN22_MoCap_fullbodyCOPY_ED.safetensors` - **900MB**
   - Từ: **m_wan22, m_wan212**

7. `Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors` - **1GB**
   - Từ: **m_wan22, m_wan212**

8. `WanAnimate_relight_lora_fp16.safetensors` - **800MB**
   - Từ: **m_wan22, m_wan212**

9. `FullDynamic_Ultimate_Fusion_Elite.safetensors` - **1.1GB**
   - Từ: **m_wan22, m_wan212**

#### 🔷 Input Images (2 files, ~2MB)
10. `ComfyUI_00004_.png` - **1MB**
    - Từ: **m_wan212**

11. `ComfyUI_00006_.png` - **1MB**
    - Từ: **m_wan212**

---

## 🚀 CÁCH SỬ DỤNG

### Phương pháp 1: Download TẤT CẢ (Khuyến nghị)

```bash
# Download files lớn trước (25-30 phút)
!python download_large_files.py

# Sau đó download files nhỏ (5-8 phút)
!python download_small_files.py

# Tổng thời gian: ~30-40 phút
```

### Phương pháp 2: Download song song (Nhanh hơn)

```python
import subprocess
from concurrent.futures import ThreadPoolExecutor

def download_script(script):
    subprocess.run(f"python {script}", shell=True)

# Download song song (nếu có đủ RAM/băng thông)
with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(download_script, "download_large_files.py")
    executor.submit(download_script, "download_small_files.py")
```

### Phương pháp 3: Download riêng lẻ

```bash
# Chỉ download files lớn
!python download_large_files.py     # ~75GB

# Chỉ download files nhỏ
!python download_small_files.py     # ~8GB
```

---

## 📊 THỐNG KÊ THEO NGUỒN

### Files từ **m_ditto** (4 files lớn)
- ditto_global_style_comfy.safetensors (5.4GB)
- Wan2_1-T2V-14B_fp8_e4m3fn.safetensors (15GB)
- umt5-xxl-enc-fp8_e4m3fn.safetensors (4.8GB) - Dùng chung
- lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors (3.2GB) - Dùng chung
- Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors (2.1GB)
- wan_2.1_vae.safetensors (2.6GB)

**Total**: ~33GB (chỉ files lớn)

### Files từ **m_mc** (5 files lớn + 2 files nhỏ)
**Lớn**:
- Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors (8GB)
- Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors (17GB)
- umt5-xxl-enc-fp8_e4m3fn.safetensors (4.8GB) - Dùng chung
- lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors (3.2GB) - Dùng chung
- wan_2.1_vae.safetensors (2.6GB)

**Nhỏ**:
- MelBandRoformer_fp32.safetensors (1.9GB)
- clip_vision_h.safetensors (1.3GB)

**Total**: ~38.8GB

### Files từ **m_wan22** (5 files lớn + 7 files nhỏ)
**Lớn**:
- Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors (17GB)
- umt5-xxl-enc-fp8_e4m3fn.safetensors (4.8GB) - Dùng chung
- lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors (3.2GB) - Dùng chung
- Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors (2.1GB)
- wan_2.1_vae.safetensors (2.6GB)

**Nhỏ**:
- clip_vision_h.safetensors (1.3GB)
- yolov10m.onnx (60MB)
- vitpose_h_wholebody_data.bin (300MB)
- vitpose_h_wholebody_model.onnx (700MB)
- WAN22_MoCap_fullbodyCOPY_ED.safetensors (900MB)
- Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors (1GB)
- WanAnimate_relight_lora_fp16.safetensors (800MB)
- FullDynamic_Ultimate_Fusion_Elite.safetensors (1.1GB)

**Total**: ~35.9GB

### Files từ **m_wan212** (TẤT CẢ - 9 files lớn + 9 files nhỏ)
Bao gồm tất cả files từ m_ditto + m_wan22 + input images

**Total**: ~83GB

---

## 💡 LƯU Ý

### ✅ Ưu điểm của cách chia này:
1. **Dễ quản lý**: Files lớn và nhỏ tách riêng
2. **Linh hoạt**: Có thể download riêng lẻ
3. **Rõ ràng**: Chú thích đầy đủ kích thước và nguồn
4. **Tối ưu**: Download files lớn với aria2c 16 connections

### 📌 Files DÙNG CHUNG (xuất hiện trong nhiều profiles):
- `umt5-xxl-enc-fp8_e4m3fn.safetensors` (4.8GB) - Tất cả 4 files
- `lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors` (3.2GB) - Tất cả 4 files
- `clip_vision_h.safetensors` (1.3GB) - m_mc, m_wan22, m_wan212

### ⚡ Tốc độ download:
- **Files lớn**: ~100-150MB/s (aria2c 16 connections)
- **Files nhỏ**: ~80-120MB/s (aria2c 8 connections)

---

## 🎯 KHUYẾN NGHỊ

**Cho beginner**:
```bash
# Đơn giản nhất - chạy tuần tự
!python download_large_files.py
!python download_small_files.py
```

**Cho advanced**:
```bash
# Tối ưu - chạy song song (cần RAM nhiều)
# Terminal 1:
!python download_large_files.py

# Terminal 2 (trong khi terminal 1 đang chạy):
!python download_small_files.py
```

**Lưu storage**:
```bash
# Chỉ download files cần thiết
# Xem từng file trong script và comment out files không cần
```

---

## 📂 CẤU TRÚC THƯ MỤC SAU KHI DOWNLOAD

```
/content/ComfyUI/models/
├── diffusion_models/
│   ├── ditto_global_style_comfy.safetensors (5.4GB)
│   ├── Wan2_1-T2V-14B_fp8_e4m3fn.safetensors (15GB)
│   ├── Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors (17GB)
│   ├── Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors (8GB)
│   ├── Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors (17GB)
│   └── MelBandRoformer_fp32.safetensors (1.9GB)
│
├── text_encoders/
│   └── umt5-xxl-enc-fp8_e4m3fn.safetensors (4.8GB)
│
├── loras/
│   ├── lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors (3.2GB)
│   ├── Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors (2.1GB)
│   ├── wan_2.1_vae.safetensors (2.6GB) - Copy từ VAE
│   ├── WAN22_MoCap_fullbodyCOPY_ED.safetensors (900MB)
│   ├── Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors (1GB)
│   ├── WanAnimate_relight_lora_fp16.safetensors (800MB)
│   └── FullDynamic_Ultimate_Fusion_Elite.safetensors (1.1GB)
│
├── vae/
│   └── wan_2.1_vae.safetensors (2.6GB)
│
├── clip_vision/
│   └── clip_vision_h.safetensors (1.3GB)
│
└── detection/
    ├── yolov10m.onnx (60MB)
    ├── vitpose_h_wholebody_data.bin (300MB)
    └── vitpose_h_wholebody_model.onnx (700MB)

/content/ComfyUI/input/
├── ComfyUI_00004_.png (1MB)
└── ComfyUI_00006_.png (1MB)
```

---

## ✅ HOÀN TẤT!

Sau khi chạy xong 2 scripts, bạn sẽ có đầy đủ **20 files** (~83GB) cần thiết cho ComfyUI!
