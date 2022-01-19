from pf_flask_web.bismillah import Bismillah

pweb_app = Bismillah(__name__)
wsgi = pweb_app.get_app()

if __name__ == '__main__':
    pweb_app.run()
