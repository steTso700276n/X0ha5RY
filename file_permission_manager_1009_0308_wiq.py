# 代码生成时间: 2025-10-09 03:08:20
import os
import stat
import tornado.ioloop
import tornado.web

# 文件权限管理器
class FilePermissionHandler(tornado.web.RequestHandler):
    # 设置文件权限
    def post(self, path):
        # 获取请求参数中的权限值
        try:
            permission = int(self.get_argument('permission'), 8)
            if not 0 <= permission <= 0o7777:
                raise ValueError("Permission value out of range.")
        except ValueError as e:
            self.set_status(400)
            self.write({'error': str(e)})
            return

        try:
            # 尝试改变文件权限
            os.chmod(path, permission)
        except OSError as e:
            self.set_status(500)
            self.write({'error': 'Failed to change file permissions.', 'details': str(e)})
            return

        # 返回成功信息
        self.write({'message': 'File permissions changed successfully.'})

    # 检查文件权限
    def get(self, path):
        try:
            # 获取文件的当前权限
            file_stat = os.stat(path)
            permission = stat.S_IMODE(file_stat.st_mode)
            self.write({'permission': oct(permission).lstrip('0o') if permission else '0'})
        except OSError as e:
            self.set_status(404)
            self.write({'error': 'File not found.', 'details': str(e)})
            return


# 设置路由
def make_app():
    return tornado.web.Application([
        (r"/(.*)", FilePermissionHandler),
    ])

# 启动服务器
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
