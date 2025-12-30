import os
import subprocess

def run(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_show(cmd):
    subprocess.run(cmd, shell=True)

os.chdir("/content/ComfyUI/custom_nodes")
run_show("git clone https://github.com/yolain/ComfyUI-Easy-Use.git")
run_show("pip install -r ./ComfyUI-Easy-Use/requirements.txt")

run_show("git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git")
run_show("wget https://huggingface.co/banhkeomath2/sound/resolve/main/note.mp3 -P /content/ComfyUI/custom_nodes/ComfyUI-Custom-Scripts/web/js/assets/")
run_show("hf download banhkeomath2/sound --local-dir /content/ComfyUI/custom_nodes/ComfyUI-Custom-Scripts/web/js/assets")

run_show("git clone https://github.com/crystian/ComfyUI-Crystools.git")
run_show("pip install -r ComfyUI-Crystools/requirements.txt")

run_show("git clone https://github.com/cubiq/ComfyUI_essentials.git")
run_show("pip install -r ComfyUI_essentials/requirements.txt")

run_show("git clone https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet.git")
run_show("git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git")
run_show("git clone https://github.com/coolzilj/ComfyUI-Photopea.git")
run_show("git clone https://github.com/huyl3-cpu/comfyui-sortlist.git")

run_show("git clone https://github.com/kijai/ComfyUI-WanAnimatePreprocess.git")
run_show("pip install -r ComfyUI-WanAnimatePreprocess/requirements.txt")

run_show("git clone https://github.com/ltdrdata/comfyui-unsafe-torch.git")

run_show("git clone https://github.com/rgthree/rgthree-comfy.git")
run_show("pip install -r rgthree-comfy/requirements.txt")

run_show("git clone https://github.com/SeanScripts/ComfyUI-Unload-Model.git")

run_show("git clone https://github.com/1038lab/ComfyUI-QwenVL.git")
run_show("pip install -r ./ComfyUI-QwenVL/requirements.txt")

run_show("git clone https://github.com/kijai/ComfyUI-GIMM-VFI.git")
run_show("pip install -r ComfyUI-GIMM-VFI/requirements.txt")

run_show("git clone https://github.com/jamesWalker55/comfyui-various.git")

run_show("git clone https://github.com/YMC-GitHub/ymc-node-suite-comfyui.git")
run_show("pip install -r ymc-node-suite-comfyui/requirements.txt")

run_show("git clone https://github.com/daxcay/ComfyUI-YouTubeVideoPlayer.git")

run_show("git clone https://github.com/TinyBeeman/ComfyUI-TinyBee.git")
run_show("pip install -r ComfyUI-TinyBee/requirements.txt")

run_show("git clone https://github.com/kijai/ComfyUI-WanVideoWrapper.git")
run_show("pip install -r ComfyUI-WanVideoWrapper/requirements.txt")

run_show("git clone https://github.com/kijai/ComfyUI-KJNodes.git")
run_show("pip install -r ComfyUI-KJNodes/requirements.txt")

run_show("git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git")
run_show("pip install -r ComfyUI-VideoHelperSuite/requirements.txt")

run_show("git clone https://github.com/justUmen/Bjornulf_custom_nodes.git")
run_show("pip install -r Bjornulf_custom_nodes/requirements.txt")

run_show("git clone https://github.com/kijai/ComfyUI-Florence2.git")
run_show("pip install -r ComfyUI-Florence2/requirements.txt")

run_show("git clone https://github.com/chflame163/ComfyUI_LayerStyle.git")
run_show("pip install -r ComfyUI_LayerStyle/requirements.txt")

run_show("git clone https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler.git")
run_show("pip install -r /content/ComfyUI/custom_nodes/ComfyUI-SeedVR2_VideoUpscaler/requirements.txt")









