import os
import subprocess
import json
from urllib import request
from flask import Flask

app = Flask(__name__)

# ==========================================
# 🚀 zirun2022 的全自动白嫖配置
# ==========================================
CONFIG = {
    "SERVER_ADDR": "frps.181225.xyz",
    "SERVER_PORT": "7000",
    "TOKEN": "maxking2026",
    "REMOTE_PORT": "8588", 
    "PROXY_NAME": "flux-free-8588",
    "DING_URL": "https://oapi.dingtalk.com/robot/send?access_token=fada04a2261f76607eea6d0203def79d8f0597ba03718e9a8edb2ee5b8ecf628" 
}

def send_ding_raw(content):
    """使用原生 urllib 发送，绝对不依赖额外的 requests 库，确保在任何极简环境都能发声"""
    try:
        # 严格包含 A 关键词，满足你的钉钉安全设置
        data = {
            "msgtype": "text",
            "text": {
                "content": f"【A-美国节点上线】\n\n🇺 目标达成！(Flux白嫖版)\n\n{content}"
            }
        }
        req = request.Request(CONFIG["DING_URL"], data=json.dumps(data).encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        with request.urlopen(req, timeout=10) as response:
            print(f"[*] 钉钉汇报状态: {response.getcode()}")
    except Exception as e:
        print(f"[!] 钉钉发送失败: {e}")

def deploy_soldier():
    print(f"[*] 准备唤醒特种兵: {CONFIG['PROXY_NAME']}")
    
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    frpc_path = os.path.join(curr_dir, "frpc")
    gost_path = os.path.join(curr_dir, "gost")
    
    # 1. 赋予执行权限
    for p in [frpc_path, gost_path]:
        if os.path.exists(p):
            os.chmod(p, 0o755)
        else:
            print(f"[!] 致命错误：找不到二进制文件 {p}")
            return # 如果找不到文件，就没必要继续了

    # 2. 启动 GOST (这是真正干活的代理)
    subprocess.Popen([gost_path, "-L", "socks5://:10080"])
    print("[*] Gost 哨兵已就位，监听 10080")

    # 3. 动态生成 TOML
    toml_content = f"""
serverAddr = "{CONFIG['SERVER_ADDR']}"
serverPort = {CONFIG['SERVER_PORT']}
auth.token = "{CONFIG['TOKEN']}"

[[proxies]]
name = "{CONFIG['PROXY_NAME']}"
type = "tcp"
localIP = "127.0.0.1"
localPort = 10080  # 关键：将外部请求引流给内部的 gost
remotePort = {CONFIG['REMOTE_PORT']}
"""
    with open(os.path.join(curr_dir, "frpc.toml"), "w") as f:
        f.write(toml_content)
    
    # 4. 启动 FRPC (这是打通内网的隧道)
    subprocess.Popen([frpc_path, "-c", os.path.join(curr_dir, "frpc.toml")])
    
    # 5. 立刻发送钉钉通知
    send_ding_raw(f"📍 端口: {CONFIG['REMOTE_PORT']}\n🆔 节点: {CONFIG['PROXY_NAME']}\n🚀 代理: SOCKS5 已就绪，请连接测试！")

@app.route('/')
def health():
    return "<h1>Flux Node Active</h1><p>Gost and FRPC are running in the background.</p>"

if __name__ == "__main__":
    # 容器一启动，立刻执行部署逻辑
    deploy_soldier()
    # 占住 8080 端口，应付 Flux 的健康检查
    app.run(host='0.0.0.0', port=8080)
