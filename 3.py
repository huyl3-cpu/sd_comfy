import os
import subprocess

def run(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_show(cmd):
    subprocess.run(cmd, shell=True)

print("🔧 Installing ComfyUI custom nodes...")

os.chdir("/content/ComfyUI/custom_nodes")

print("📥 Installing ComfyUI-Manager...")
run_show("git clone https://github.com/Comfy-Org/ComfyUI-Manager.git")
os.chdir("/content/ComfyUI/custom_nodes/ComfyUI-Manager")
run_show("pip install -r requirements.txt")
run_show("pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130")

os.chdir("/content/ComfyUI/custom_nodes")
print("📥 Installing Easy-Use...")
run_show("git clone https://github.com/yolain/ComfyUI-Easy-Use.git")
run_show("pip install -r ./ComfyUI-Easy-Use/requirements.txt")

print("📥 Installing Custom Scripts...")
run_show("git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git")
run_show("wget https://huggingface.co/banhkeomath2/sound/resolve/main/note.mp3 -P /content/ComfyUI/custom_nodes/ComfyUI-Custom-Scripts/web/js/assets/")
run_show("hf download banhkeomath2/sound --local-dir /content/ComfyUI/custom_nodes/ComfyUI-Custom-Scripts/web/js/assets")

print("📥 Installing Crystools...")
run_show("git clone https://github.com/crystian/ComfyUI-Crystools.git")
run_show("pip install -r ComfyUI-Crystools/requirements.txt")

print("📥 Installing Essentials...")
run_show("git clone https://github.com/cubiq/ComfyUI_essentials.git")
run_show("pip install -r ComfyUI_essentials/requirements.txt")

print("📥 Installing AlekPet Nodes...")
run_show("git clone https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet.git")

print("📥 Installing Custom Scripts (2nd clone)...")
run_show("git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git")

print("📥 Installing Photopea...")
run_show("git clone https://github.com/coolzilj/ComfyUI-Photopea.git")

print("📥 Installing SortList...")
run_show("git clone https://github.com/huyl3-cpu/comfyui-sortlist.git")

print("📥 Installing WanAnimatePreprocess...")
run_show("git clone https://github.com/kijai/ComfyUI-WanAnimatePreprocess.git")
run_show("pip install -r ComfyUI-WanAnimatePreprocess/requirements.txt")

print("📥 Installing Unsafe Torch...")
run_show("git clone https://github.com/ltdrdata/comfyui-unsafe-torch.git")

print("📥 Installing rgthree-comfy...")
run_show("git clone https://github.com/rgthree/rgthree-comfy.git")
run_show("pip install -r rgthree-comfy/requirements.txt")

print("📥 Installing Unload-Model...")
run_show("git clone https://github.com/SeanScripts/ComfyUI-Unload-Model.git")

print("📥 Installing QwenVL...")
run_show("git clone https://github.com/1038lab/ComfyUI-QwenVL.git")
run_show("pip install -r ./ComfyUI-QwenVL/requirements.txt")

print("📥 Installing GIMM-VFI...")
run_show("git clone https://github.com/kijai/ComfyUI-GIMM-VFI.git")
run_show("pip install -r ComfyUI-GIMM-VFI/requirements.txt")

print("📥 Installing Various Nodes...")
run_show("git clone https://github.com/jamesWalker55/comfyui-various.git")

print("📥 Installing YMC Node Suite...")
run_show("git clone https://github.com/YMC-GitHub/ymc-node-suite-comfyui.git")
run_show("pip install -r ymc-node-suite-comfyui/requirements.txt")

print("📥 Installing YouTube Video Player...")
run_show("git clone https://github.com/daxcay/ComfyUI-YouTubeVideoPlayer.git")

print("📥 Installing TinyBee...")
run_show("git clone https://github.com/TinyBeeman/ComfyUI-TinyBee.git")
run_show("pip install -r ComfyUI-TinyBee/requirements.txt")

print("📥 Installing WanVideoWrapper...")
run_show("git clone https://github.com/kijai/ComfyUI-WanVideoWrapper.git")
run_show("pip install -r ComfyUI-WanVideoWrapper/requirements.txt")

print("📥 Installing Impact Pack...")
run_show("git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git")
run_show("pip install -r ComfyUI-Impact-Pack/requirements.txt")

print("📥 Installing KJNodes...")
run_show("git clone https://github.com/kijai/ComfyUI-KJNodes.git")
run_show("pip install -r ComfyUI-KJNodes/requirements.txt")

print("📥 Installing VideoHelperSuite...")
run_show("git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git")
run_show("pip install -r ComfyUI-VideoHelperSuite/requirements.txt")

print("📥 Installing Bjornulf custom nodes...")
run_show("git clone https://github.com/justUmen/Bjornulf_custom_nodes.git")
run_show("pip install -r Bjornulf_custom_nodes/requirements.txt")

# ⭐⭐⭐ NEW: Installing ComfyUI-Florence2 ⭐⭐⭐
print("📥 Installing ComfyUI-Florence2...")
run_show("git clone https://github.com/kijai/ComfyUI-Florence2.git")
run_show("pip install -r comfyui-florence2/requirements.txt")

print("\n🎉 ALL CUSTOM NODES INSTALLED SUCCESSFULLY!\n")
