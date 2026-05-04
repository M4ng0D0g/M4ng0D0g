import urllib.request
import json
import re
import sys

# ====== 系統設定 ======
# 請將這裡替換成你在 Hugging Face 上的真實使用者名稱
HF_USERNAME = "M4ng0D0g" 
README_PATH = "README.md"
# ======================

def fetch_training_metrics():
    url = f"https://huggingface.co/api/models?author={HF_USERNAME}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if not data:
                return "> [Warning] No training checkpoints found for this user."
            
            total_models = len(data)
            total_downloads = sum(model.get('downloads', 0) for model in data)
            total_likes = sum(model.get('likes', 0) for model in data)
            
            # 組合終端機風格的輸出字串
            stats_output = (
                f"> Tracked Checkpoints : {total_models}\n"
                f"> Total Downloads     : {total_downloads}\n"
                f"> Community Likes     : {total_likes}\n"
                f"> Sync Status         : Data structure intact."
            )
            return stats_output
            
    except Exception as e:
        print(f"Error fetching data: {e}")
        return "> [Error] Connection to Hugging Face API failed."

def inject_to_readme(stats_text):
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 使用正規表達式鎖定 START 與 END 標籤，並替換中間的內容
        pattern = re.compile(r"(<!-- START_HF_STATS -->\n).*?(\n\s*<!-- END_HF_STATS -->)", re.DOTALL)
        
        # 確認標籤是否存在
        if not pattern.search(content):
            print("Error: Could not find START_HF_STATS / END_HF_STATS tags in README.md")
            sys.exit(1)
            
        new_content = pattern.sub(r"\g<1>" + stats_text + r"\g<2>", content)
        
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print("Successfully injected HF metrics into README.md")
        
    except FileNotFoundError:
        print(f"Error: {README_PATH} not found.")
        sys.exit(1)

if __name__ == "__main__":
    print(f"Initiating Hugging Face API connection for user: {HF_USERNAME}...")
    metrics = fetch_training_metrics()
    inject_to_readme(metrics)
