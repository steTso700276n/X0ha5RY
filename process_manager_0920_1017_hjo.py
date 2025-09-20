# 代码生成时间: 2025-09-20 10:17:29
import os
import subprocess
import tornado.ioloop
import tornado.web
import json

"""
Process Manager using Tornado framework.

This application provides a simple web interface to manage processes.
It allows starting, stopping, and listing system processes.
"""

class ProcessManagerHandler(tornado.web.RequestHandler):
    """
    Tornado request handler for managing processes.
    """
    def get(self):
        """
        GET endpoint to list all processes.
        """
        try:
            # Use subprocess to list all system processes
            p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
            output, error = p.communicate()
            self.write(output.decode('utf-8'))
        except Exception as e:
            self.write(f"Error: {e}")

    def post(self):
        """
        POST endpoint to start a new process.
        """
        try:
            # Get the process command from the request body
            process_info = json.loads(self.request.body)
            command = process_info['command']
            # Use subprocess to start the process
            subprocess.Popen(command, shell=True)
            self.write(f"Process started: {command}")
        except Exception as e:
            self.write(f"Error starting process: {e}")

    def delete(self, process_id):
        """
        DELETE endpoint to stop a process by ID.
        """
        try:
            # Use os.kill to terminate the process
            os.kill(int(process_id), 9)
            self.write(f"Process {process_id} terminated")
        except Exception as e:
            self.write(f"Error terminating process: {e}")

def make_app():
    """
    Create a Tornado application with defined routes.
    """
    return tornado.web.Application([
        (r"/processes", ProcessManagerHandler),
        (r"/processes/([0-9]+)", ProcessManagerHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Process Manager Server started on port 8888")
    tornado.ioloop.IOLoop.current().start()