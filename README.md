# 📂 Tổng Hợp Model ComfyUI & Script Tải Xuống

Tài liệu này tổng hợp danh sách các models và hướng dẫn sử dụng các script tải xuống/di chuyển file.

## 🚀 Quy trình làm việc (Workflow)

1.  **Tải xuống:** Chạy các script `m_*.py` để tải model về thư mục hiện tại.
2.  **Di chuyển (Move):** Chạy các script `mv_*.py` để đưa file vào đúng thư mục ComfyUI (nếu chạy trên Colab/Server).
3.  **Upload (Tùy chọn):** Sử dụng hướng dẫn trong `UPLOAD.md` để đưa file lên Hugging Face.

---

## 🛠️ Danh sách Script Hỗ trợ

| Tên File | Chức năng | Ghi chú |
| :--- | :--- | :--- |
| [`download_small_files.py`](./download_small_files.py) | Tải **tất cả** các file nhỏ (<2GB) | Tải về thư mục hiện tại. Đã tối ưu tốc độ. |
| [`UPLOAD.md`](./UPLOAD.md) | **Hướng dẫn Upload** lên Hugging Face | Các lệnh tạo repo và upload nhanh. |

---

## 📦 Script Tải & Di Chuyển (Theo nhóm)

Các file `m_*.py` đã được **vô hiệu hóa đường dẫn lưu mặc định**, nghĩa là file sẽ được tải ngay tại thư mục bạn đang đứng. Để di chuyển chúng vào đúng chỗ trong ComfyUI, hãy chạy script `mv_*.py` tương ứng.

### 1. Nhóm `Ditto` / `Wan2.1`
*   📥 **Tải xuống:** [`m_ditto.py`](./m_ditto.py)
*   path **Di chuyển:** [`mv_ditto.py`](./mv_ditto.py)

### 2. Nhóm `MC`
*   📥 **Tải xuống:** [`m_mc.py`](./m_mc.py)
*   path **Di chuyển:** [`mv_mc.py`](./mv_mc.py)

### 3. Nhóm `Wan2.2`
*   📥 **Tải xuống:** [`m_wan22.py`](./m_wan22.py)
*   path **Di chuyển:** [`mv_wan22.py`](./mv_wan22.py)

### 4. Nhóm `Wan2.1 & 2.2` (Tổng hợp)
*   📥 **Tải xuống:** [`m_wan212.py`](./m_wan212.py)
*   path **Di chuyển:** [`mv_wan212.py`](./mv_wan212.py)

---

## 📋 Chi tiết File & Đường dẫn gốc
*(Dưới đây là danh sách file chi tiết và nơi chúng sẽ được chuyển đến khi chạy script `mv`)*

### 1. 📄 `m_ditto.py`
**🐘 Large Files (>2GB)**
| Tên File | Đường dẫn đích (khi chạy `mv_ditto.py`) | Link |
| :--- | :--- | :--- |
| `ditto_global_style_comfy.safetensors` | `/content/ComfyUI/models/diffusion_models` | [Download](https://huggingface.co/QingyanBai/Ditto_models/resolve/main/models_comfy/ditto_global_style_comfy.safetensors) |
| `Wan2_1-T2V-14B_fp8_e4m3fn.safetensors` | `/content/ComfyUI/models/diffusion_models` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1-T2V-14B_fp8_e4m3fn.safetensors) |
| `umt5-xxl-enc-fp8_e4m3fn.safetensors` | `/content/ComfyUI/models/text_encoders` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors) |

**📦 Small Files (<2GB)**
| Tên File | Đường dẫn đích (khi chạy `mv_ditto.py`) | Link |
| :--- | :--- | :--- |
| `wan_2.1_vae.safetensors` | `/content/ComfyUI/models/vae` | [Download](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors) |
| `Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors) |
| `lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors) |

---

### 2. 📄 `m_mc.py`
**🐘 Large Files (>2GB)**
| Tên File | Đường dẫn đích (khi chạy `mv_mc.py`) | Link |
| :--- | :--- | :--- |
| `Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors` | `/content/ComfyUI/models/diffusion_models` | [Download](https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/InfiniteTalk/Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors) |
| `Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors` | `/content/ComfyUI/models/diffusion_models` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/6714d2392c4a3a2119834b8d45c5666c9bf9328c/Wan2_1-I2V-14B-720P_fp8_e4m3fn.safetensors) |
| `MelBandRoformer_fp32.safetensors` | `/content/ComfyUI/models/diffusion_models` | [Download](https://huggingface.co/Kijai/MelBandRoFormer_comfy/resolve/main/MelBandRoformer_fp32.safetensors) |
| `umt5-xxl-enc-fp8_e4m3fn.safetensors` | `/content/ComfyUI/models/text_encoders` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors) |

**📦 Small Files (<2GB)**
| Tên File | Đường dẫn đích (khi chạy `mv_mc.py`) | Link |
| :--- | :--- | :--- |
| `wan_2.1_vae.safetensors` | `/content/ComfyUI/models/vae` | [Download](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors) |
| `lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors) |
| `clip_vision_h.safetensors` | `/content/ComfyUI/models/clip_vision` | [Download](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors) |

---

### 3. 📄 `m_wan22.py`
**🐘 Large Files (>2GB)**
| Tên File | Đường dẫn đích (khi chạy `mv_wan22.py`) | Link |
| :--- | :--- | :--- |
| `Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors` | `/content/ComfyUI/models/diffusion_models` | [Download](https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/Wan22Animate/Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors) |
| `umt5-xxl-enc-fp8_e4m3fn.safetensors` | `/content/ComfyUI/models/text_encoders` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors) |

**📦 Small Files (<2GB)**
| Tên File | Đường dẫn đích (khi chạy `mv_wan22.py`) | Link |
| :--- | :--- | :--- |
| `yolov10m.onnx` | `/content/ComfyUI/models/detection` | [Download](https://huggingface.co/Wan-AI/Wan2.2-Animate-14B/resolve/main/process_checkpoint/det/yolov10m.onnx) |
| `vitpose_h_wholebody_data.bin` | `/content/ComfyUI/models/detection` | [Download](https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_data.bin) |
| `vitpose_h_wholebody_model.onnx` | `/content/ComfyUI/models/detection` | [Download](https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_model.onnx) |
| `clip_vision_h.safetensors` | `/content/ComfyUI/models/clip_vision` | [Download](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors) |
| `WAN22_MoCap_fullbodyCOPY_ED.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/banhkeomath2/wan22/resolve/main/WAN22_MoCap_fullbodyCOPY_ED.safetensors) |
| `Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/banhkeomath2/wan22/resolve/main/Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors) |
| `lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors) |
| `WanAnimate_relight_lora_fp16.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/banhkeomath2/wan22/resolve/main/WanAnimate_relight_lora_fp16.safetensors) |
| `FullDynamic_Ultimate_Fusion_Elite.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/banhkeomath2/wan22/resolve/main/FullDynamic_Ultimate_Fusion_Elite.safetensors) |
| `Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors) |
| `wan_2.1_vae.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors) |

---

### 4. 📄 `m_wan212.py`
**🐘 Large Files (>2GB)**
| Tên File | Đường dẫn đích (khi chạy `mv_wan212.py`) | Link |
| :--- | :--- | :--- |
| `ditto_global_style_comfy.safetensors` | `/content/ComfyUI/models/diffusion_models` | [Download](https://huggingface.co/QingyanBai/Ditto_models/resolve/main/models_comfy/ditto_global_style_comfy.safetensors) |
| `Wan2_1-T2V-14B_fp8_e4m3fn.safetensors` | `/content/ComfyUI/models/diffusion_models` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1-T2V-14B_fp8_e4m3fn.safetensors) |
| `Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors` | `/content/ComfyUI/models/diffusion_models` | [Download](https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/Wan22Animate/Wan2_2-Animate-14B_fp8_scaled_e4m3fn_KJ_v2.safetensors) |
| `umt5-xxl-enc-fp8_e4m3fn.safetensors` | `/content/ComfyUI/models/text_encoders` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors) |

**📦 Small Files (<2GB)**
| Tên File | Đường dẫn đích (khi chạy `mv_wan212.py`) | Link |
| :--- | :--- | :--- |
| `wan_2.1_vae.safetensors` | `/content/ComfyUI/models/vae` | [Download](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors) |
| `wan_2.1_vae.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors) |
| `Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors) |
| `lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors) |
| `WAN22_MoCap_fullbodyCOPY_ED.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/banhkeomath2/wan22/resolve/main/WAN22_MoCap_fullbodyCOPY_ED.safetensors) |
| `Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/banhkeomath2/wan22/resolve/main/Wan2.2-Fun-A14B-InP-Fusion-Elite.safetensors) |
| `WanAnimate_relight_lora_fp16.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/banhkeomath2/wan22/resolve/main/WanAnimate_relight_lora_fp16.safetensors) |
| `FullDynamic_Ultimate_Fusion_Elite.safetensors` | `/content/ComfyUI/models/loras` | [Download](https://huggingface.co/banhkeomath2/wan22/resolve/main/FullDynamic_Ultimate_Fusion_Elite.safetensors) |
| `yolov10m.onnx` | `/content/ComfyUI/models/detection` | [Download](https://huggingface.co/Wan-AI/Wan2.2-Animate-14B/resolve/main/process_checkpoint/det/yolov10m.onnx) |
| `vitpose_h_wholebody_data.bin` | `/content/ComfyUI/models/detection` | [Download](https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_data.bin) |
| `vitpose_h_wholebody_model.onnx` | `/content/ComfyUI/models/detection` | [Download](https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_model.onnx) |
| `clip_vision_h.safetensors` | `/content/ComfyUI/models/clip_vision` | [Download](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors) |
