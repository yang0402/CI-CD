# 简单 Flask GHCR 项目
## 项目概述
这是一个基于 Docker 容器化的 Flask Web 应用，通过 GitHub Actions 实现 CI/CD，部署到阿里云服务器，使用 GitHub Container Registry (GHCR) 存储镜像。

## 前提条件
阿里云服务器已安装 Docker
服务器已配置 SSH 访问
GitHub 个人访问令牌 (PAT) 已创建，包含 write:packages 权限
GitHub 仓库已配置以下 Secrets：
GHCR_TOKEN：GitHub 个人访问令牌
SSH_PRIVATE_KEY：服务器 SSH 私钥



## 部署步骤

将代码推送到 GitHub 仓库的 main 分支
GitHub Actions 自动构建 Docker 镜像并推送到 GHCR
镜像被拉取到服务器并运行容器
访问 http://<服务器IP>:5000 查看应用

服务器配置

## 确保服务器已安装 Docker：
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker


## 确保防火墙允许 5000 端口访问：
ufw allow 5000


## 配置 GHCR 登录（在服务器上执行）：
docker login ghcr.io -u <GitHub用户名>



### 注意事项

替换 deploy.yml 中的 SERVER_IP 和 SERVER_USER（如果需要）
确保 GitHub 个人访问令牌具有 write:packages 权限
确保服务器上的 Docker 已正确配置并具有拉取镜像的权限
建议使用 Nginx 反向代理以增强安全性

### 扩展建议

配置 HTTPS，使用 Let's Encrypt 获取免费 SSL 证书
添加健康检查到 Dockerfile
使用 Docker Compose 管理多容器应用

