from flask import Flask
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def hello():
    # 顺便显示一下当前的出口 IP，方便调试
    return f"Flux Node is running! Target: {os.getenv('TARGET_COUNTRY', 'US')}"

if __name__ == "__main__":
    # 核心：在 Python 启动时，自动把特种兵脚本带起来
    import subprocess
    subprocess.Popen(["bash", "entrypoint.sh"]) 
    
    app.run(host='0.0.0.0', port=8080)
