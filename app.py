import os
import subprocess
import json
from urllib import request
from flask import Flask

app = Flask(__name__)

# ==========================================
# 🚀 zirun2022 的全自动白嫖配置 (防弹版)
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
    """原生 urllib 发送钉钉，绝不因为缺少 requests 库而崩溃"""
    try:
        data = {
            "msgtype": "text",
            "text": {
                # 严格包含 A 关键词
                "content": f"【A-美国节点上线】\n\n🇺 目标达成！(Flux防弹装甲版)\n\n{content}"
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
    
    # 获取当前代码运行的绝对目录
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    frpc_path = os.path.join(curr_dir, "frpc")
    gost_path = os.path.join(curr_dir, "gost")
    
    # 【核心防御】：把配置文件写到 /tmp，绕过 Flux 的 Read-Only 锁定
    toml_path = "/tmp/frpc.toml"
    
    try:
        # 1. 尝试赋予执行权限 (加 try 保护，防止没权限导致整个 Python 崩溃)
        for p in [frpc_path, gost_path]:
            if os.path.exists(p):
                try:
                    os.chmod(p, 0o755)
                    print(f"[*] 已确认执行权限: {p}")
                except Exception as chmod_e:
                    print(f"[!] 警告：无法修改 {p} 的权限 ({chmod_e})")
            else:
                print(f"[!] 致命错误：找不到二进制文件 {p}")
                return # 文件都不在，直接撤退，保证 Flask 存活

        # 2. 启动 GOST 哨兵 (本地 10080 端口)
        try:
            subprocess.Popen([gost_path, "-L", "socks5://:10080"])
            print("[*] Gost 哨兵已就位，监听 10080")
        except Exception as e:
            print(f"[!!!] Gost 启动失败: {e}")

        # 3. 动态生成 TOML 到 /tmp 目录
        toml_content = f"""
serverAddr = "{CONFIG['SERVER_ADDR']}"
serverPort = {CONFIG['SERVER_PORT']}
auth.token = "{CONFIG['TOKEN']}"

[[proxies]]
name = "{CONFIG['PROXY_NAME']}"
type = "tcp"
localIP = "127.0.0.1"
localPort = 10080  # 指向内部的 gost
remotePort = {CONFIG['REMOTE_PORT']}
"""
        with open(toml_path, "w") as f:
            f.write(toml_content)
        print(f"[*] 配置已写入安全区: {toml_path}")
        
        # 4. 启动 FRPC 建立隧道
        try:
            subprocess.Popen([frpc_path, "-c", toml_path])
            print("[*] FRPC 隧道正在建立...")
        except Exception as e:
            print(f"[!!!] FRPC 启动失败: {e}")
        
        # 5. 任务完成，发送钉钉报喜
        send_ding_raw(f"📍 端口: {CONFIG['REMOTE_PORT']}\n🆔 节点: {CONFIG['PROXY_NAME']}\n🚀 代理: SOCKS5 已就绪，请连接测试！")
        
    except Exception as overall_e:
        print(f"[!!!] 部署脚本发生全局异常: {overall_e}")

# 网页端，用来应付 Flux 的健康检查
@app.route('/')
def health():
    return "<h1>Flux Node Active (Armor Version)</h1><p>Running stably!</p>"

if __name__ == "__main__":
    # 容器启动时，先执行核心逻辑
    deploy_soldier()
    # 占住 8080 端口，确保容器不会被判死刑
    app.run(host='0.0.0.0', port=8080)
