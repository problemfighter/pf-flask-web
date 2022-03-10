import sys

from setuptools import setup
from pf_flask_web import Bismillah
from pf_py_text.pfpt_string_util import PFPTStringUtil


class PWeb(Bismillah):
    _project_name = "PWebApp"

    def __init__(self, name, project_root_path, **kwargs):
        super().__init__(project_root_path=project_root_path, *kwargs)
        self._project_name = name

    def setup_script(self):
        if self._project_name:
            name = PFPTStringUtil.system_readable(self._project_name)
            setup(name=name, entry_points={'console_scripts': ['pweb=pweb:cli']})

    def run(self):
        cli_args = sys.argv
        if "install" in cli_args:
            self.setup_script()
            self.color_print("Successfully Install Completed!", color="green", bold=True)
        else:
            super(PWeb, self).run()

    @staticmethod
    def init(name, project_root_path, **kwargs):
        return PWeb(name=name, project_root_path=project_root_path, **kwargs)
