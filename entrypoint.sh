#!/bin/bash

# --- 1. 下载 frpc (Linux amd64 通用版) ---
FRP_VER="0.68.0"
echo "Downloading frp v${FRP_VER}..."
curl -L -o frp.tar.gz "https://github.com/fatedier/frp/releases/download/v${FRP_VER}/frp_${FRP_VER}_linux_amd64.tar.gz"
tar -zxvf frp.tar.gz
cp frp_${FRP_VER}_linux_amd64/frpc ./
chmod +x ./frpc

# --- 2. 自动生成配置 ---
# 随机一个 8500-8900 的端口，避免和你现有的费城/朱诺冲突
MY_PORT=$(shuf -i 8500-8900 -n 1)
cat <<EOF > frpc.toml
serverAddr = "frps.181225.xyz"
serverPort = 7000
auth.token = "maxking2026"

[[proxies]]
name = "flux-free-${MY_PORT}"
type = "tcp"
localIP = "127.0.0.1"
localPort = 8080
remotePort = ${MY_PORT}
EOF

# --- 3. 启动并向中控报到 ---
echo "Node starting on port ${MY_PORT}..."
# 如果你已经跑了 master_control.py，这一行会让你在面板上看到它
curl -s -X POST "http://frps.181225.xyz:5000/api/register" \
     -H "Content-Type: application/json" \
     -d "{\"port\": \"${MY_PORT}\", \"isp\": \"Flux-Free\", \"country\": \"Global\"}"

./frpc -c frpc.toml
