#!/bin/bash

# ==========================================
# 🚀 zirun2022 的指挥中心配置 (硬编码区)
# ==========================================
SERVER_ADDR="frps.181225.xyz"
SERVER_PORT="7000"
TOKEN="maxking2026"
# 建议给 Flux 免费版分配一个专属号段，避免冲突
REMOTE_PORT=$(shuf -i 8600-8800 -n 1) 
PROXY_NAME="flux-att-$(date +%s)"
# ==========================================

echo "[*] 特种兵正在空降至 Flux 节点..."

# 1. 动态获取架构并下载 frpc
# Flux 免费版通常是 amd64
FRP_VER="0.68.0"
URL="https://github.com/fatedier/frp/releases/download/v${FRP_VER}/frp_${FRP_VER}_linux_amd64.tar.gz"

echo "[*] 正在拉取装备: $URL"
curl -L -o frp.tar.gz "$URL" && tar -zxvf frp.tar.gz
cp frp_${FRP_VER}_linux_amd64/frpc ./frpc
chmod +x ./frpc

# 2. 侦察环境并打印日志 (方便你在 Flux Logs 里看)
IP_INFO=$(curl -s https://ipinfo.io/json)
echo "[*] 侦察报告: $IP_INFO"

# 3. 现场编写配置文件 (TOML 格式)
cat <<EOF > ./frpc.toml
serverAddr = "${SERVER_ADDR}"
serverPort = ${SERVER_PORT}
auth.token = "${TOKEN}"

[[proxies]]
name = "${PROXY_NAME}"
type = "tcp"
localIP = "127.0.0.1"
localPort = 8080
remotePort = ${REMOTE_PORT}
EOF

echo "[+] 配置文件已就绪，目标端口: ${REMOTE_PORT}"

# 4. 启动特种兵
# 使用 exec 确保 frpc 成为容器的主进程，方便监控
./frpc -c ./frpc.toml
