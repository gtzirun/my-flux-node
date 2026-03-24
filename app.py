import os
import subprocess
import random
import time
import requests  # 记得在 requirements.txt 加上 requests
from flask import Flask

app = Flask(__name__)

# ==========================================
# 🚀 zirun2022 的指挥中心配置
# ==========================================
CONFIG = {
    "SERVER_ADDR": "frps.181225.xyz",
    "SERVER_PORT": "7000",
    "TOKEN": "maxking2026",
    "REMOTE_PORT": str(random.randint(8600, 8800)),
    "PROXY_NAME": f"flux-python-{int(time.time())}",
    "DING_URL": "你的钉钉机器人WEBHOOK_URL" # <--- 填入你的机器人地址
}

def send_ding(content):
    try:
        data = {
            "msgtype": "text",
            "text": {"content": f"【Flux资产上线】\n{content}"}
        }
        requests.post(CONFIG["DING_URL"], json=data, timeout=5)
    except Exception as e:
        print(f"钉钉发送失败: {e}")

def deploy_soldier():
    # 1. 侦察当前 IP 信息 (为了汇报得更详细)
    try:
        ip_info = requests.get("https://ipinfo.io/json", timeout=5).json()
        target_ip = ip_info.get("ip", "Unknown")
        isp = ip_info.get("org", "Unknown")
        country = ip_info.get("country", "Unknown")
    except:
        target_ip, isp, country = "Scan Failed", "N/A", "N/A"

    # 2. 赋予执行权限并生成配置 (逻辑同前)
    os.chmod("./frpc", 0o755)
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
    
    # 3. 启动隧道
    subprocess.Popen(["./frpc", "-c", "./frpc.toml"])

    # 4. 【核心】补上钉钉通知
    report = f"📍 IP: {target_ip}\n🌐 ISP: {isp}\n🌍 国家: {country}\n🔗 端口: {CONFIG['REMOTE_PORT']}\n🆔 名称: {CONFIG['PROXY_NAME']}"
    send_ding(report)

@app.route('/')
def index():
    return f"<h1>Flux Node Active</h1><p>Running on {CONFIG['REMOTE_PORT']}</p>"

if __name__ == "__main__":
    deploy_soldier()
    app.run(host='0.0.0.0', port=8080)
