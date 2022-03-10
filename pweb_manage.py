from pf_flask_web.pweb import PWeb

pweb_app = PWeb.init("PWeb", __file__)
cli = pweb_app.cli
wsgi = pweb_app.get_app()

if __name__ == '__main__':
    pweb_app.run()

