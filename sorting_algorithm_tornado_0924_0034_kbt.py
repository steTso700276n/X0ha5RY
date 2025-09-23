# 代码生成时间: 2025-09-24 00:34:46
import tornado.ioloop
import tornado.web
import json

# 定义一个排序算法类，包含冒泡排序和快速排序两种方法
class SortingAlgorithm:
    def __init__(self):
        pass

    # 冒泡排序算法
    def bubble_sort(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]  # 交换元素
        return arr

    # 快速排序算法
    def quick_sort(self, arr):
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            less = [x for x in arr[1:] if x <= pivot]
            greater = [x for x in arr[1:] if x > pivot]
            return self.quick_sort(less) + [pivot] + self.quick_sort(greater)

# 定义一个Tornado的请求处理类
class SortingHandler(tornado.web.RequestHandler):
    def post(self):
        # 获取JSON请求体
        try:
            data = json.loads(self.request.body)
            arr = data.get('arr')
            if arr is None or not isinstance(arr, list) or not all(isinstance(x, (int, float)) for x in arr):
                self.write(json.dumps({'error': 'Invalid input'}))
                return
        except json.JSONDecodeError:
            self.write(json.dumps({'error': 'Invalid JSON'}))
            return

        # 处理排序请求
        algorithm = SortingAlgorithm()
        if data.get('type') == 'bubble':
            sorted_arr = algorithm.bubble_sort(arr.copy())
        elif data.get('type') == 'quick':
            sorted_arr = algorithm.quick_sort(arr.copy())
        else:
            self.write(json.dumps({'error': 'Invalid sorting type'}))
            return

        # 返回排序结果
        self.write(json.dumps({'sorted_arr': sorted_arr}))

# 设置Tornado路由
def make_app():
    return tornado.web.Application([
        (r"/sort", SortingHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server started on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()