from setuptools import setup, find_packages
import os
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent
README = (CURRENT_DIR / "readme.md").read_text()

env = os.environ.get('dev')


def get_dependencies():
    dependency = ['Flask', 'gunicorn']

    if env and env == "dev":
        return dependency

    return dependency + [
        "PF-Flask-DB", "PF-Flask-REST", "PF-Flask-Swagger",
        "PF-PY-YMLEnv", "PF-Flask-Mail", "PF-Flask-Notify",
        "PF-Flask-Auth",
    ]


setup(
    name='PF-Flask-Web',
    version='1.0.0',
    url='https://github.com/problemfighter/pf-flask-web',
    license='Apache 2.0',
    author='Problem Fighter',
    author_email='problemfighter.com@gmail.com',
    description='Flask Web DRY full-stack framework by Problem Fighter',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_dependencies(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ]
)