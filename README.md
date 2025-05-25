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
1. 不能直接使用 docker/login-action 插件在远程服务器上登录 ACR。docker/login-action 是 GitHub Actions Runner 专用的。
2. 当 docker/build-push-action 插件解析 tags 参数时，它会将 tags 下面的每一行作为一个完整的标签传递给底层的 Docker 命令。Docker 镜像的标签（tag）是用来标识镜像版本的字符串，它有严格的命名规范，不能包含空格、# 符号以及 # 后面的任何注释内容。

## 补充说明
还有一种方法可以绕过ACR或者CHCR（未实验）
1. CI/CD 工作流构建 Docker 镜像。
2. 使用 docker save -o my_image.tar my_image_name:tag 将镜像导出为 my_image.tar 文件。
3. actions/upload-artifact 上传 my_image.tar到上传到 GitHub Actions 提供的专用 Artifacts 存储服务。
4. 部署 Job 下载 my_image.tar。
5. 部署 Job 通过 SSH 连接到阿里云服务器。
6. 将 my_image.tar 通过 scp 传输到阿里云服务器。
7. 在阿里云服务器上使用 docker load -i my_image.tar 加载镜像。
8. docker run 运行容器。
#### actions/upload-artifact 的核心功能是：将 GitHub Actions 工作流在运行过程中生成的文件，从 Runner 上传到 GitHub 的云端存储，从而实现这些文件的持久化、共享和后续的下载。

## 测试
1. 在项目根目录运行 pytest 命令,pytest 会自动发现 tests/ 目录中的 test_app.py 文件，并执行其中的测试函数。
2. 运行 pytest 命令的根目录（即 app.py 所在的目录）被自动添加到了 Python 的模块搜索路径 sys.path 中，使得 app.py 可以被视为一个可以直接导入的顶级模块。但是，仅仅路径在 sys.path 中还不够，Python 还需要将目录识别为包，才能正确地处理目录内的模块导入。


## 未来更新
1. 更新action的具体用法详解
2. RAM 子账号 + AccessKey 来替代当前中文用户名登录ACR