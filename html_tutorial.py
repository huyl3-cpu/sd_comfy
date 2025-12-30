from IPython.display import display, HTML
import base64, os

# ============================================================
# 1) TẢI ẢNH TUTORIAL NẾU CHƯA CÓ
# ============================================================
IMG_PATH = "/content/tutorial.png"
IMG_URL = "https://huggingface.co/banhkeomath1/and/resolve/main/tutorial.png"

if not os.path.exists(IMG_PATH):
    import urllib.request
    urllib.request.urlretrieve(IMG_URL, IMG_PATH)

# Encode ảnh thành base64
with open(IMG_PATH, "rb") as f:
    html_img = "data:image/png;base64," + base64.b64encode(f.read()).decode()


# ============================================================
# 2) HTML BLOCK
# ============================================================
html_block = f"""
<style>
.guide-title {{
    background: #1a1a1a;
    padding: 12px 16px;
    border-left: 4px solid #00ff9d;
    font-size: 16px;
    font-weight: 600;
    color: #e6e6e6;
    margin-bottom: 5px;
    border-radius: 6px;
}}
.contact {{
    color: #cccccc;
    margin: 4px 0 12px 4px;
    font-size: 14px;
}}
.code-box-container {{
    position: relative;
    background: #111;
    padding: 16px 20px;
    border-radius: 10px;
    border: 1px solid #333;
    font-family: monospace;
    color: #00ff9d;
}}
.copy-btn {{
    position: absolute; 
    top: 8px; 
    right: 10px;
    background: #00ff9d; 
    color: #000;
    border: none; 
    padding: 6px 12px;
    border-radius: 6px; 
    cursor: pointer; 
    font-weight: bold;
}}
.copy-btn:hover {{
    background: #00d786;
}}
img {{
    margin-top: 14px;
    border-radius: 8px;
    border: 1px solid #333;
    max-width: 100%;
}}
</style>

<div class="guide-title">
👉 Anh chị vui lòng thực hiện <b>4 bước hướng dẫn</b> bên dưới để tải model cần thiết:
</div>

<div class="contact">
📞 Liên hệ hỗ trợ khi gặp sự cố: 
<a href="https://zalo.me/0386369365" target="_blank">0386.369.365 (Zalo)</a> — 
<a href="https://fb.com/xanhphoto.offical" target="_blank">fb.com/xanhphoto.offical</a>
</div>

<div class="code-box-container">
    <button class="copy-btn" onclick="copyCmd()">COPY</button>
    <div id="cmdText">source env.txt && chmod +x wan22.sh && bash wan22.sh</div>
</div>

<div>
    <img src="{html_img}">
</div>

<script>
function copyCmd(){{
    navigator.clipboard.writeText(
        document.getElementById("cmdText").innerText
    );
    const btn = document.querySelector(".copy-btn");
    btn.innerText = "COPIED ✔";
    setTimeout(()=>btn.innerText = "COPY",1200);
}}
</script>
"""

display(HTML(html_block))

