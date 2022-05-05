import os
import sys
from setuptools import setup
from pf_flask_web import Bismillah
from pf_py_text.pfpt_string_util import PFPTStringUtil


env = os.environ.get('source')


class PWebEngine(Bismillah):
    _project_name = "PWebApp"
    version = '0.0.1'
    dependency = []
    source_dependency = []

    def __init__(self, name, project_root_path, **kwargs):
        super().__init__(project_root_path=project_root_path, *kwargs)
        self._project_name = name

    def get_dependencies(self):
        if env and env == "dev":
            return self.dependency
        return self.dependency + self.source_dependency

    def setup_script(self):
        if self._project_name:
            name = PFPTStringUtil.system_readable(self._project_name)
            setup(
                install_requires=self.get_dependencies(),
                version=self.version,
                name=name,
                entry_points={'console_scripts': ['pweb=pweb_cli:cli']}
            )

    def run(self):
        cli_args = sys.argv
        if "develop" in cli_args:
            self.setup_script()
            self.color_print("Successfully Install Completed!", color="green", bold=True)
        else:
            super(PWebEngine, self).run()

    @staticmethod
    def start(name, project_root_path, **kwargs):
        return PWebEngine(name=name, project_root_path=project_root_path, **kwargs)
