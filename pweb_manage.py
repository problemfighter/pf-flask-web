import click
from flask.cli import FlaskGroup
from pf_flask_web import Bismillah


def pweb_factory():
    pweb_app = Bismillah(__file__)
    return pweb_app.get_app()


@click.group(cls=FlaskGroup, create_app=pweb_factory)
def cli():
    print("Welcome to PWeb CLI")


if __name__ == '__main__':
    pweb_factory().run()
