import os
import subprocess
import random
import time
from flask import Flask

app = Flask(__name__)

# ==========================================
# 🚀 zirun2022 的指挥中心配置 (硬编码区)
# ==========================================
CONFIG = {
    "SERVER_ADDR": "frps.181225.xyz",
    "SERVER_PORT": "7000",
    "TOKEN": "maxking2026",
    "REMOTE_PORT": str(random.randint(8600, 8800)),
    "PROXY_NAME": f"flux-python-{int(time.time())}"
}

def deploy_soldier():
    print(f"[*] 正在初始化特种兵: {CONFIG['PROXY_NAME']}")
    
    # 1. 赋予执行权限
    try:
        os.chmod("./frpc", 0o755)
    except Exception as e:
        print(f"[!] 权限设置失败: {e}")

    # 2. 动态生成 TOML 配置内容
    toml_content = f"""
serverAddr = "{CONFIG['SERVER_ADDR']}"
serverPort = {CONFIG['SERVER_PORT']}
auth.token = "{CONFIG['TOKEN']}"

[[proxies]]
name = "{CONFIG['PROXY_NAME']}"
type = "tcp"
localIP = "127.0.0.1"
localPort = 8080
remotePort = {CONFIG['REMOTE_PORT']}
"""
    with open("frpc.toml", "w") as f:
        f.write(toml_content)
    
    # 3. 异步启动 frpc 并持续监控输出
    print(f"[*] 正在建立隧道，目标端口: {CONFIG['REMOTE_PORT']}")
    subprocess.Popen(["./frpc", "-c", "./frpc.toml"])

@app.route('/')
def index():
    # 增加一个简单的状态显示，方便你在浏览器验证
    return f"<h1>Flux Node Active</h1><p>Proxy: {CONFIG['PROXY_NAME']} | Port: {CONFIG['REMOTE_PORT']}</p>"

if __name__ == "__main__":
    # 启动前先空降特种兵
    deploy_soldier()
    # Flux 默认监听端口
    app.run(host='0.0.0.0', port=8080)
