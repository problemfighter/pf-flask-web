from pf_flask_web import Bismillah


def pweb_factory():
    pweb_app = Bismillah(__file__)
    return pweb_app


cli = pweb_factory().cli
wsgi = pweb_factory().get_app()


if __name__ == '__main__':
    pweb_factory().run()
