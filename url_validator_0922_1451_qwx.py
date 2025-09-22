# 代码生成时间: 2025-09-22 14:51:37
import tornado.ioloop
import tornado.web
import requests
def is_valid_url(url):
    # 尝试对URL进行请求，以检查其有效性
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        # 检查状态码是否为200
        return response.status_code == 200
    except requests.RequestException as e:
        # 如果请求过程中出现异常，则认为URL无效
        return False
def make_app():
    return tornado.web.Application([
        (r"/validate_url", ValidateUrlHandler),
    ])
def start_server(port):
    app = make_app()
    app.listen(port)
    print(f"Server started on port {port}.")
    tornado.ioloop.IOLoop.current().start()
class ValidateUrlHandler(tornado.web.RequestHandler):
    # 处理HTTP GET请求，用于验证URL有效性
    def get(self):
        # 获取URL参数
        url = self.get_argument("url")
        # 验证URL是否有效
        if is_valid_url(url):
            self.write({"status": "valid"})
        else:
            self.write({"status": "invalid"})

# 如果脚本被直接执行，则启动服务器
if __name__ == "__main__":
    port = 8888
    start_server(port)