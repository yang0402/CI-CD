# 简单 Flask GHCR 项目
## 项目概述
这是一个基于 Docker 容器化的 Flask Web 应用，通过 GitHub Actions 实现 CI/CD，部署到阿里云服务器，使用 GitHub Container Registry (GHCR) 存储镜像。

## 前提条件
1. 阿里云服务器已安装 Docker
2. 服务器已配置 SSH 访问
3. GitHub 个人访问令牌 (PAT) 已创建，包含 write:packages 权限
4. GitHub 仓库已配置以下 Secrets：
GHCR_TOKEN：GitHub 个人访问令牌
SSH_PRIVATE_KEY：本地机器生成的私钥放在action里面的secrets即SSH_PRIVATE_KEY,将公钥添加到远程服务器的 ~/.ssh/authorized_keys 文件中,这样你可以通过私钥连接到远程服务器。

## CI/CD 部署过程中代码拉取的位置
Runner 是一个虚拟机或容器（由 GitHub 提供或你自己搭建的自托管 runner）,
当你触发一个 workflow（例如 push 到 main 分支），GitHub 会启动一个临时的 runner 实例。
代码会被自动拉取到 runner 的工作目录,进行构建和打包。


## 部署步骤
1. GitHub Actions 自动创建一个虚拟机（runner）。runner 从你的仓库中拉取代码。
2. 使用 docker/build-push-action 构建本地 Docker 镜像。构建完成后打上标签（如 ghcr.io/xxx/simple-flask-app:latest 和 commit hash 标签）。
3. 登录 GHCR 并将本地构建好的镜像推送到远程仓库。这样远程服务器就可以从公网访问这个镜像。
4. runner 通过 SSH 连接到你的远程服务器。在远程服务器上进行安装 Docker（如果没安装）,登录GHCR,拉取刚刚推送上去的镜像,停止旧容器、启动新容器,清理缓存和认证信息等操作。


## 服务器配置
确保服务器已安装 Docker：
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker


## 确保防火墙允许 5000 端口访问：
ufw allow 5000

## 注意事项
替换 deploy.yml 中的 SERVER_IP 和 SERVER_USER（如果需要）
确保 GitHub 个人访问令牌具有 write:packages 权限
确保服务器上的 Docker 已正确配置并具有拉取镜像的权限
建议使用 Nginx 反向代理以增强安全性

## 扩展建议
配置 HTTPS，使用 Let's Encrypt 获取免费 SSL 证书
添加健康检查到 Dockerfile
使用 Docker Compose 管理多容器应用
## 为什么先把依赖文件移到容器里面安装依赖再把项目移到容器里面,而不是直接先把整个项目移到容器里面安装依赖？
因为docker是分层构建,这样方便只更新代码不更新依赖文件时不需要每次都更新依赖层。

# update
## 由于阿里云服务器拉取 GHCR 镜像会慢,因此本项目更新采用使用阿里云容器镜像服务（ACR）中转
由于/etc/docker/daemon.json里面设置代理不能做token转发（可能,没试验过）,自建国内Runner不现实,因此这就是最好的办法。因此我将原先的适用于GitHub Container Registry的配置文件变成GHCR.txt以供参考,更新适合阿里云ACR的deploy.yml。为了安全可以将阿里云的ACR_USERNAME和ACR_PASSWORD。
## 避坑指南
1. 请使用docker/login-action插件在远程服务器（runner链接到了远程服务器）上登陆ACR，因为mkdir -p ~/.docker echo "{\"auths\":{\"crpi-jus3outykfqe01tn.cn-hangzhou.personal.cr.aliyuncs.com\":{\"auth\":\"$(echo -n \"${ACR_USERNAME}:${ACR_PASSWORD}\" | base64)\"}}}" > ~/.docker/config.json 这种只是生成了一个认证文件，并没有真正测试是否能成功登录 ACR,同时构建时仍然可能因为权限不足或认证失败而推送失败，还缺乏对错误的检测机制（比如用户名密码错误、网络不通等。