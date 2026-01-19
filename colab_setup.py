#@title 🔑 1. Setup ComfyUI { display-mode: "form" }
#@markdown ## 🎯 CẤU HÌNH CHẾ ĐỘ
mode = "MC" #@param ["Chuyển_Style", "Dancing", "Chuyển_Style&Dancing", "MC"]

#@markdown ---
#@markdown ##### 💾 Tuỳ chọn Google Drive *(nếu cần lưu trữ)*
login_drive = True #@param {type:"boolean"}

if login_drive:
    from google.colab import drive
    drive.mount('/content/drive')
%cd /content/
!git clone https://github.com/huyl3-cpu/sd_comfy.git
!hf download banhkeomath2/sound --local-dir /content/sound/
from IPython.display import Audio, Javascript, display
def play(mp3):
    display(Audio(mp3, autoplay=True))
    display(Javascript('document.querySelector("audio").style.display="none"'))
!python /content/sd_comfy/init.py
play("/content/sound/1.mp3")

if mode == "Chuyển_Style":
    !python /content/sd_comfy/m_ditto.py
elif mode == "Dancing":
    !python /content/sd_comfy/m_wan22.py
elif mode == "Chuyển_Style&Dancing":
    !python /content/sd_comfy/m_wan212.py
elif mode == "MC":
    !python /content/sd_comfy/m_mc.py

!python /content/sd_comfy/custom_nodes.py
%cd /content/ComfyUI/
!pip install onnxruntime-gpu==1.23.2
!pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python-headless opencv-contrib-python
!pip install opencv-python opencv-python-headless opencv-contrib-python-headless
!pip install opencv-contrib-python
!pip uninstall pynvml nvidia-ml-py -y && pip install nvidia-ml-py
play("/content/sound/start.mp3")
print(f"✅ Setup hoàn tất! Mode: {mode}")
