# 代码生成时间: 2025-09-22 22:50:02
import os
import shutil
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

"""
Folder Structure Manager
This application provides functionality to organize the structure of folders.
"""

class FolderStructureManager:
    def __init__(self, root_path):
        self.root_path = root_path

    def organize(self, target_path):
        """
        Organize the files in the given target path to the root path.
        Creates directories if they do not exist.
        """
        try:
            for item in os.listdir(target_path):
                item_path = os.path.join(target_path, item)
                if os.path.isfile(item_path):
                    self.move_file(item_path, self.root_path)
                elif os.path.isdir(item_path):
                    self.organize(item_path)
        except Exception as e:
            raise Exception(f"Error organizing files: {e}")

    def move_file(self, file_path, new_path):
        """
        Move a file from its current path to a new path.
        """
        try:
            shutil.move(file_path, new_path)
        except Exception as e:
            raise Exception(f"Error moving file: {e}")

class FolderStructureHandler(RequestHandler):
    def get(self):
        try:
            self.manager = FolderStructureManager(self.get_argument('root_path', ''))
            self.manager.organize(self.get_argument('target_path', ''))
            self.write({"message": "Files organized successfully"})
        except Exception as e:
            self.write({"error": str(e)})

def make_app():
    return Application([
        (r"/organize", FolderStructureHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()
