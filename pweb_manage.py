import click
from flask.cli import FlaskGroup
from pf_flask_web import Bismillah


def pweb_factory():
    pweb_app = Bismillah(__file__)
    return pweb_app


@click.group(cls=FlaskGroup, create_app=pweb_factory().get_app)
def cli():
    print("Welcome to PWeb CLI")


wsgi = pweb_factory().get_app()


if __name__ == '__main__':
    pweb_factory().run()
