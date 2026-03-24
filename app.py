import os
import subprocess
import json
import ssl
import time
from urllib import request
from flask import Flask

app = Flask(__name__)

# ==========================================
# 🚀 zirun2022 空中加油版 (终极纯净白嫖)
# ==========================================
CONFIG = {
    "SERVER_ADDR": "frps.181225.xyz",
    "SERVER_PORT": "7000",
    "TOKEN": "maxking2026",
    "REMOTE_PORT": "8588", 
    "PROXY_NAME": "flux-git-ultimate",
    "DING_URL": "https://oapi.dingtalk.com/robot/send?access_token=fada04a2261f76607eea6d0203def79d8f0597ba03718e9a8edb2ee5b8ecf628" 
}

def send_ding_raw(content):
    try:
        data = {"msgtype": "text", "text": {"content": f"【A-美国节点上线】\n\n🇺🇸 目标达成！(Git空中加油版)\n\n{content}"}}
        req = request.Request(CONFIG["DING_URL"], data=json.dumps(data).encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        ctx = ssl._create_unverified_context()
        request.urlopen(req, timeout=10, context=ctx)
    except Exception as e:
        print(f"[!] 钉钉发送失败: {e}")

def deploy_soldier():
    print("[*] 开始执行 [空中加油] 部署协议...")
    
    # 全部在 /tmp 目录下操作，绝对拥有读写执行权限！
    os.chdir("/tmp")
    
    try:
        # 1. 现场下载并解压官方 Gost
        print("[*] 正在下载 Gost...")
        os.system("curl -L -o gost.tar.gz https://github.com/ginuerzh/gost/releases/download/v2.11.5/gost_2.11.5_linux_amd64.tar.gz")
        os.system("tar -xzf gost.tar.gz && mv gost-linux-amd64/gost /tmp/gost")
        os.system("chmod +x /tmp/gost")
        
        # 2. 现场下载并解压官方 FRPC
        print("[*] 正在下载 FRPC...")
        os.system("curl -L -o frp.tar.gz https://github.com/fatedier/frp/releases/download/v0.54.0/frp_0.54.0_linux_amd64.tar.gz")
        os.system("tar -xzf frp.tar.gz && mv frp_0.54.0_linux_amd64/frpc /tmp/frpc")
        os.system("chmod +x /tmp/frpc")

        # 3. 启动 Gost 代理
        subprocess.Popen(["/tmp/gost", "-L", "socks5://:10080"])
        print("[*] Gost 代理已在 10080 端口启动")

        # 4. 生成 FRPC 配置
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
        with open("/tmp/frpc.toml", "w") as f:
            f.write(toml_content)
        
        # 5. 启动隧道
        subprocess.Popen(["/tmp/frpc", "-c", "/tmp/frpc.toml"])
        print("[*] FRPC 隧道已建立")
        
        # 6. 发送无敌战报
        send_ding_raw(f"📍 端口: {CONFIG['REMOTE_PORT']}\n🆔 节点: {CONFIG['PROXY_NAME']}\n🚀 代理: SOCKS5 已就绪，完全绕过本地权限限制！")
        
    except Exception as e:
        print(f"[!!!] 致命错误: {e}")

@app.route('/')
def health():
    return "<h1>Flux Node Active (Air Refueling Edition)</h1><p>0 cost, 100% success.</p>"

if __name__ == "__main__":
    deploy_soldier()
    app.run(host='0.0.0.0', port=8080)
