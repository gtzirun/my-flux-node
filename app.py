import os
import subprocess
import json
import shutil
import ssl
from urllib import request
from flask import Flask

app = Flask(__name__)

# ==========================================
# 🚀 zirun2022 的全自动白嫖配置 (终极破壁版)
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
    """强行关闭 SSL 校验，确保钉钉在任何简陋容器里都能发声"""
    try:
        data = {
            "msgtype": "text",
            "text": {
                "content": f"【A-美国节点上线】\n\n🇺 目标达成！(Flux终极破壁版)\n\n{content}"
            }
        }
        req = request.Request(CONFIG["DING_URL"], data=json.dumps(data).encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        
        # 核心：忽略极简容器缺失 SSL 证书的问题
        ctx = ssl._create_unverified_context()
        with request.urlopen(req, timeout=10, context=ctx) as response:
            print(f"[*] 钉钉汇报状态: {response.getcode()}")
    except Exception as e:
        print(f"[!] 钉钉发送失败: {e}")

def deploy_soldier():
    print(f"[*] 准备唤醒特种兵: {CONFIG['PROXY_NAME']}")
    
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    orig_frpc = os.path.join(curr_dir, "frpc")
    orig_gost = os.path.join(curr_dir, "gost")
    
    # 【核心防御】：把战场转移到 /tmp 目录
    tmp_frpc = "/tmp/frpc"
    tmp_gost = "/tmp/gost"
    toml_path = "/tmp/frpc.toml"
    
    try:
        # 1. 偷天换日：复制到 /tmp 并强行赋权
        for src, dst in [(orig_frpc, tmp_frpc), (orig_gost, tmp_gost)]:
            if os.path.exists(src):
                shutil.copy2(src, dst)
                os.chmod(dst, 0o755)  # 在 /tmp 下，我们有绝对的权限！
                print(f"[*] 已在 /tmp 成功集结并赋权: {dst}")
            else:
                print(f"[!] 致命错误：找不到源文件 {src}")
                return

        # 2. 启动 GOST 哨兵 (运行 /tmp 下的版本)
        try:
            subprocess.Popen([tmp_gost, "-L", "socks5://:10080"])
            print("[*] Gost 哨兵已就位，监听 10080")
        except Exception as e:
            print(f"[!!!] Gost 启动失败: {e}")

        # 3. 动态生成 TOML 到 /tmp
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
        with open(toml_path, "w") as f:
            f.write(toml_content)
        
        # 4. 启动 FRPC 建立隧道 (运行 /tmp 下的版本)
        try:
            subprocess.Popen([tmp_frpc, "-c", toml_path])
            print("[*] FRPC 隧道正在建立...")
        except Exception as e:
            print(f"[!!!] FRPC 启动失败: {e}")
        
        # 5. 任务完成，发送钉钉报喜
        send_ding_raw(f"📍 端口: {CONFIG['REMOTE_PORT']}\n🆔 节点: {CONFIG['PROXY_NAME']}\n🚀 代理: SOCKS5 已就绪，请免密连接！")
        
    except Exception as overall_e:
        print(f"[!!!] 部署脚本发生全局异常: {overall_e}")

@app.route('/')
def health():
    return "<h1>Flux Node Active (Ultimate Breakout)</h1><p>Running securely from /tmp.</p>"

if __name__ == "__main__":
    deploy_soldier()
    app.run(host='0.0.0.0', port=8080)
