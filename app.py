# app.py

from flask import Flask

def create_app():
    """
    这是一个 Flask 应用工厂函数。
    它的作用是创建并返回一个 Flask 应用实例。
    """
    app = Flask(__name__)

    @app.route('/')
    def home():
        return '<h1>欢迎使用 Flask 应用！</h1>'

    return app

# Gunicorn 调用的地方：
# 它会导入 app 模块，然后调用 create_app() 函数来获取 Flask 应用实例。
# 所以 Gunicorn 命令应该是 'app:create_app()'
# 或者，我们可以直接在全局作用域暴露一个 app 实例（不推荐工厂模式）
# 或者，更符合工厂模式的 Gunicorn 调用方式是直接指定工厂函数。

# 为了让 Gunicorn 能够直接找到一个可调用的应用实例，
# 我们可以直接在模块级别暴露一个 Flask 应用实例，
# 但这与工厂模式的初衷略有冲突。
# 更常见且推荐的 Gunicorn 与工厂模式配合方式是：
# Gunicorn 命令直接指向工厂函数，例如 `gunicorn --bind 0.0.0.0:5000 "app:create_app()"`
# 或者，为了兼容你现有的 CMD 命令，我们让 create_app() 返回的实例赋给一个全局变量。

# 为了兼容你现在的 CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
# 并且保留工厂模式的结构，你可以这样做：
app = create_app() # 在模块被导入时就调用工厂函数，并将返回的实例赋给全局变量 'app'

# 当直接运行此脚本文件时（通常用于开发）。
if __name__ == '__main__':
    # 这里的 app 变量已经由上面的 `app = create_app()` 赋值。
    # debug=True 在生产环境应为 False
    app.run(host='0.0.0.0', port=5000, debug=True)