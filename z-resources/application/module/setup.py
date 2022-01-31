import os.path
import pathlib
from os.path import exists
from setuptools import setup, find_packages


CURRENT_DIR = pathlib.Path(__file__).parent
long_description = ""
readme_md_file = os.path.join(CURRENT_DIR, "readme.md")
if exists(readme_md_file):
    long_description = pathlib.Path(readme_md_file).read_text()

env = os.environ.get('source')


def get_dependencies():
    dependency = []

    if env and env == "dev":
        return dependency

    return dependency + []


setup(
    name='__MODULE_NAME__',
    version='1.0.0',
    url='__REPOSITORY_URL__',
    license='__LICENSE_NAME__',
    author='__AUTHOR_NAME__',
    author_email='__AUTHOR_EMAIL__',
    description='__DESCRIPTION__',
    long_description=long_description,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_dependencies(),
    classifiers=[]
)
