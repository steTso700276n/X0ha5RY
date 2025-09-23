# 代码生成时间: 2025-09-23 17:19:48
import tornado.ioloop
import tornado.web
from tornado.options import define, options

# Define the allowed themes
ALLOWED_THEMES = ['light', 'dark', 'colorful']

class ThemeHandler(tornado.web.RequestHandler):
    """
    Handle theme switching requests.
    """
    def get(self):
        # Get the requested theme from the query parameters
        requested_theme = self.get_query_argument('theme', None)

        # Check if the requested theme is allowed
        if requested_theme in ALLOWED_THEMES:
            # Store the theme in the user's session
            self.set_secure_cookie('theme', requested_theme)
            self.write(f"Theme set to {requested_theme}.")
        else:
            # If the theme is not allowed, set it to the first one in the list
            self.set_secure_cookie('theme', ALLOWED_THEMES[0])
            self.write("Invalid theme requested. Defaulting to light theme.")

    def set_default_headers(self):
        # Set the default theme for the user's session
        theme = self.get_secure_cookie('theme')
        if theme:
            self.set_header("X-Theme", theme)
        else:
            self.set_header("X-Theme", "light")

class MainHandler(tornado.web.RequestHandler):
    """
    Handle the main page.
    """
    def get(self):
        self.write("Welcome to the theme switcher!")

# Define the Tornado application
class ThemeSwitcherApp(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/switch-theme", ThemeHandler),
        ]
        settings = dict(
            cookie_secret="your_secret_key",
            template_path="templates",
            static_path="static"
        )
        super(ThemeSwitcherApp, self).__init__(handlers, **settings)

# Define the command line options
define("port", default=8888, help="run on the given port", type=int)

def main():
    # Parse the command line options
    tornado.options.parse_command_line()

    # Create and run the Tornado application
    app = ThemeSwitcherApp()
    app.listen(options.port)
    print(f"Starting server on port {options.port}")
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()