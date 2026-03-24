from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    # 顺便显示一下当前的出口 IP，方便调试
    return f"Flux Node is running! Target: {os.getenv('TARGET_COUNTRY', 'US')}"

if __name__ == "__main__":
    # Flux 默认通常检测 80 或 8080 端口
    app.run(host='0.0.0.0', port=8080)
