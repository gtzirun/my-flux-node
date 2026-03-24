import os
import subprocess
import random
import time
import requests
from flask import Flask

app = Flask(__name__)

# ==========================================
# 🚀 zirun2022 的指挥中心配置 (带 A 关键词)
# ==========================================
CONFIG = {
    "SERVER_ADDR": "frps.181225.xyz",
    "SERVER_PORT": "7000",
    "TOKEN": "maxking2026",
    # 随机一个远程端口，避开 8158 等核心资产
    "REMOTE_PORT": str(random.randint(8600, 8888)),
    "PROXY_NAME": f"flux-att-python-{int(time.time())}",
    "DING_URL": "https://oapi.dingtalk.com/robot/send?access_token=fada04a2261f76607eea6d0203def79d8f0597ba03718e9a8edb2ee5b8ecf628" 
}

def send_ding(content):
    try:
        payload = {
            "msgtype": "text",
            "text": {
                "content": f"【A-Flux全武装节点上线】\n\n🇺 目标达成！\n\n{content}"
            }
        }
        headers = {"Content-Type": "application/json"}
        requests.post(CONFIG["DING_URL"], json=payload, headers=headers, timeout=10)
    except Exception as e:
        print(f"钉钉发送失败: {e}")

def deploy_soldier():
    print(f"[*] 正在初始化双特种兵: {CONFIG['PROXY_NAME']}")
    
    # 1. 获取出口 IP 信息 (AT&T 侦察)
    try:
        res = requests.get("https://ipinfo.io/json", timeout=10).json()
        ip, org, city = res.get("ip"), res.get("org"), res.get("city")
    except:
        ip, org, city = "未知", "未知", "未知"

    # 2. 赋予执行权限
    for bin_file in ["./frpc", "./gost"]:
        if os.path.exists(bin_file):
            os.chmod(bin_file, 0o755)
        else:
            print(f"[!] 警告：缺失文件 {bin_file}")

    # 3. 【关键】启动 Gost 监听在 10080 (作为 SOCKS5 代理服务端)
    # 不设密码，方便测试；协议为 socks5
    subprocess.Popen(["./gost", "-L", "socks5://:10080"])
    print("[*] Gost 哨兵已就位，监听 10080")

    # 4. 生成 frpc 配置 (将远程端口指向本地的 Gost 端口 10080)
    toml_content = f"""
serverAddr = "{CONFIG['SERVER_ADDR']}"
serverPort = {CONFIG['SERVER_PORT']}
auth.token = "{CONFIG['TOKEN']}"

[[proxies]]
name = "{CONFIG['PROXY_NAME']}"
type = "tcp"
localIP = "127.0.0.1"
localPort = 10080
remotePort = {CONFIG['REMOTE_PORT']}
"""
    with open("frpc.toml", "w") as f:
        f.write(toml_content)
    
    # 5. 启动 frpc 建立隧道
    subprocess.Popen(["./frpc", "-c", "./frpc.toml"])

    # 6. 发送带 A 关键词的钉钉报喜
    report = (
        f"📍 位置: {city} | {org}\n\n"
        f"🌐 住宅IP: {ip}\n\n"
        f"🔗 代理端口: {CONFIG['REMOTE_PORT']}\n\n"
        f"🆔 节点名称: {CONFIG['PROXY_NAME']}"
    )
    send_ding(report)

@app.route('/')
def index():
    return "<h1>Flux Node Fully Armed</h1><p>A-Status: Gost & FRPC Running</p>"

if __name__ == "__main__":
    deploy_soldier()
    app.run(host='0.0.0.0', port=8080)
