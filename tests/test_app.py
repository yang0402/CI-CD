# tests/test_app.py

import sys
import os

# --- 明确地将项目根目录添加到 sys.path ---
# 获取当前文件 (test_app.py) 所在的目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录 (tests/ 的父目录)
# os.path.join(current_dir, os.pardir) 会得到 'tests/..'，os.path.abspath 会解析它
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))

# 如果项目根目录不在 Python 的模块搜索路径 (sys.path) 中，就将其添加到最前面
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --- 导入路径设置结束 ---


# 现在可以安全地导入 app 模块了
# from app import create_app
import pytest
from app import create_app # 导入 Flask 应用工厂函数

@pytest.fixture
def app():
    """
    pytest fixture：为测试提供一个 Flask 应用实例。
    每个测试函数如果需要 'app' 这个 fixture，pytest 都会调用此函数。
    """
    test_app = create_app()
    test_app.config['TESTING'] = True
    yield test_app

@pytest.fixture
def client(app):
    """
    pytest fixture：为测试提供一个 Flask 测试客户端。
    """
    return app.test_client()

def test_home_page_status_code(client):
    """
    测试根路由 ('/') 是否返回 HTTP 200 (OK) 状态码。
    """
    response = client.get('/')
    assert response.status_code == 200, "根路由应返回 200 OK 状态码"

def test_home_page_content(client):
    """
    测试根路由 ('/') 返回的内容是否包含预期的欢迎消息。
    """
    response = client.get('/')
    expected_string = '<h1>欢迎使用 Flask 应用！</h1>'
    expected_bytes = expected_string.encode('utf-8')
    assert expected_bytes in response.data, "根路由内容应包含欢迎消息"

def test_home_page_content_type(client):
    """
    测试根路由 ('/') 返回的 HTTP 响应头中的 Content-Type 是否正确。
    """
    response = client.get('/')
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8', "Content-Type 应为 text/html; charset=utf-8"