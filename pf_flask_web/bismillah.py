from flask import Flask


class Bismillah(object):
    pweb_app: Flask

    def __init__(self, name):
        self.pweb_app = Flask(name)

    def run(self):
        self.pweb_app.run()

    def get_app(self):
        return self.pweb_app

