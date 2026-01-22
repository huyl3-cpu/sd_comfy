"""
ditto_small.py - Download FILES NHỎ (<2GB) cho DITTO vào thư mục hiện tại
BỎ đường dẫn lưu (không có -d) để download về /content/ditto/
Sau đó dùng mv để di chuyển về đúng vị trí
"""

import subprocess
import os

def run(cmd: str):
    print(f"\n RUN: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

run("bash -c 'source /content/env.txt || true'")

print("""
{'='*70}
📦 DITTO - FILES NHỎ (<2GB)
Download về thư mục hiện tại: /content/ditto/
{'='*70}
""")

# DITTO không có files nhỏ độc quyền
# Tất cả files của ditto đều >2GB

print("\n⚠️  DITTO không có files nhỏ (<2GB)")
print("Tất cả files đã được download bởi ditto_large.py")

print("""
{'='*70}
📝 README cho repo banhkeomath2/ditto
{'='*70}
""")

# Tạo README
readme = '''# Ditto Models

## Files trong repo này
Repo này chỉ chứa README vì ditto không có files nhỏ (<2GB) độc quyền.

## Files lớn (>2GB)
Tất cả files lớn được download trực tiếp bằng aria2c:
- ditto_global_style_comfy.safetensors (5.4GB)
- Wan2_1-T2V-14B_fp8_e4m3fn.safetensors (15GB)
- umt5-xxl-enc-fp8_e4m3fn.safetensors (4.8GB)
- wan_2.1_vae.safetensors (2.6GB)
- Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors (2.1GB)
- lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors (3.2GB)

## Cách sử dụng
1. Download files lớn: `python ditto_large.py`
2. Cài đặt dependencies (nếu cần)

Total: ~33GB
'''

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)

print("✅ Đã tạo README.md")
print("\n✅ Hoàn thành! Upload thư mục này lên banhkeomath2/ditto")
