# 导入 Flask 框架，用于创建 Web 应用
from flask import Flask

# 初始化 Flask 应用实例
app = Flask(__name__)

# 定义根路由，返回简单的欢迎消息
@app.route('/')
def home():
    # 返回 HTML 内容，显示欢迎信息
    return '<h1>欢迎使用 Flask 应用！</h1>'

# 当直接运行此脚本时，启动 Flask 开发服务器
if __name__ == '__main__':
    # 监听所有网络接口，端口为 5000，启用调试模式
    app.run(host='0.0.0.0', port=5000, debug=True)