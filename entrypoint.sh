#!/bin/bash

# --- 1. 获取当前环境信息 ---
IP_INFO=$(curl -s https://ipinfo.io/json)
COUNTRY=$(echo $IP_INFO | jq -r '.country')
IP=$(echo $IP_INFO | jq -r '.ip')
ORG=$(echo $IP_INFO | jq -r '.org')

# --- 2. 这里的配置可以根据你的 DMIT 修改 ---
SERVER_ADDR="frps.181225.xyz"
SERVER_PORT="7000"
TOKEN="maxking2026"
REMOTE_PORT=$(shuf -i 8100-8900 -n 1) # 避开你已经占用的 8158 等端口

# --- 3. 国籍过滤器 ---
# 如果不是美国节点，直接自杀（触发 Flux 重新调度，实现免费刷 IP）
if [ "$COUNTRY" != "US" ]; then
    echo "Current Country: $COUNTRY. Not US, exiting to trigger re-deploy..."
    exit 1
fi

# --- 4. 生成 frpc 配置文件 ---
cat <<EOF > /tmp/frpc.toml
serverAddr = "${SERVER_ADDR}"
serverPort = ${SERVER_PORT}
auth.token = "${TOKEN}"

[[proxies]]
name = "flux-us-${REMOTE_PORT}"
type = "tcp"
localIP = "127.0.0.1"
localPort = 8080
remotePort = ${REMOTE_PORT}
EOF

# --- 5. 启动代理和服务 ---
# 先启动一个后台的 gost 代理（如果你的镜像环境里有它）
# 如果没有，可以直接让 frpc 转发 app.py 的端口做心跳
echo "Starting FRPC for US Node: ${IP} (${ORG})..."
./frpc -c /tmp/frpc.toml
