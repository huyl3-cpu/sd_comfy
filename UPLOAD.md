# 1. Cài đặt lại để chắc chắn
pip install -U huggingface_hub
# 2. Set Token
export HF_TOKEN="YOUR_HF_TOKEN_HERE"
# 3. Tạo Repo (dùng --repo-type)
hf repo create banhkeomath2/wan21 --repo-type model
# 4. Upload file
hf upload banhkeomath2/small /content/all
# 5.Delete repo
hf repo delete banhkeomath2/wan22 --repo-type model

