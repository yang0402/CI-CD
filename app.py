# app.py

# 导入 Flask 框架，用于创建 Web 应用
from flask import Flask

def create_app():
    """
    这是一个 Flask 应用工厂函数。
    它的作用是创建并返回一个 Flask 应用实例。
    使用应用工厂模式，可以方便地在不同的环境（例如：开发、测试、生产）
    创建和配置应用实例，使应用更易于测试和管理。
    """
    # 初始化 Flask 应用实例
    app = Flask(__name__)

    # 定义根路由 ('/')，当用户访问应用的根路径时，会执行 home() 函数。
    @app.route('/')
    def home():
        # 返回 HTML 内容，显示欢迎信息。
        # Flask 会自动将 Python 字符串转换为 HTTP 响应体。
        return '<h1>欢迎使用 Flask 应用！</h1>'

    # 你可以在这里添加其他路由、配置、蓝图注册等应用初始化逻辑。
    # 例如：
    # app.config['SECRET_KEY'] = 'your_super_secret_key' # 配置密钥，用于 Session 等
    # from . import auth, blog # 导入其他模块的蓝图
    # app.register_blueprint(auth.bp) # 注册蓝图
    # app.register_blueprint(blog.bp)

    # 返回配置好的应用实例
    return app

# 当直接运行此脚本文件（例如通过 `python app.py`）时，执行以下代码块。
# 这通常用于开发和本地测试。
if __name__ == '__main__':
    # 调用 create_app() 函数来创建应用实例
    app = create_app()
    # 启动 Flask 开发服务器。
    # host='0.0.0.0' 允许从任何 IP 地址访问（在容器化部署中常用）。
    # port=5000 指定服务器监听的端口。
    # debug=True 启用调试模式，这在开发时很有用（会自动重启服务器、提供调试信息），
    # 但在生产环境中应设置为 False，以避免安全风险和性能问题。
    app.run(host='0.0.0.0', port=5000, debug=True)