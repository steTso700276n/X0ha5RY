# 代码生成时间: 2025-10-05 19:19:36
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import json

# 定义配置参数
define("port", default=8888, help="run on the given port", type=int)

# 客户类
class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# 客户关系管理类
class CustomerManagement:
    def __init__(self):
        self.customers = []

    def add_customer(self, customer):
        """添加客户"""
        if isinstance(customer, Customer):
            self.customers.append(customer)
            return True
        else:
            return False

    def get_customers(self):
        """获取所有客户"""
        return self.customers

# API路由类
class CustomerAPI(tornado.web.RequestHandler):
    def initialize(self, customer_management):
        self.customer_management = customer_management

    def post(self):
        """添加客户"""
        try:
            customer_data = json.loads(self.request.body)
            customer = Customer(customer_data['name'], customer_data['email'])
            if self.customer_management.add_customer(customer):
                self.write({'status': 'success', 'message': 'Customer added successfully'})
            else:
                self.write({'status': 'error', 'message': 'Invalid customer data'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})

    def get(self):
        """获取所有客户"""
        try:
            customers = self.customer_management.get_customers()
            customer_list = [{'name': customer.name, 'email': customer.email} for customer in customers]
            self.write({'status': 'success', 'data': customer_list})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})

# 设置路由
def make_app():
    customer_management = CustomerManagement()
    return tornado.web.Application([
        (r"/api/customer", CustomerAPI, dict(customer_management=customer_management)),
    ])

# 主函数
def main():
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    print(f"Server is running on port {options.port}")
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()