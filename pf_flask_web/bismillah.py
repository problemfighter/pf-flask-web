import os

from flask_cors import CORS
from flask import Flask
from pf_flask_web.system12.pweb_app_config import PWebAppConfig
from pf_flask_web.system12.pweb_registry import PWebRegistry
from pf_py_ymlenv import yaml_env


class Bismillah(object):
    _pweb_app: Flask
    _config: PWebAppConfig = None

    def __init__(self, project_root_path, config=PWebAppConfig(), name="PWebApp"):
        self._pweb_app = Flask(name)
        self._config = config
        self._process_project_root_path(root_path=project_root_path)
        self._init_config()
        self._init_cors()

    def run(self):
        self._pweb_app.run(host=self._config.HOST, port=self._config.PORT)

    def get_app(self):
        return self._pweb_app

    def add_before_request_fun(self, function):
        self._pweb_app.before_request_funcs.setdefault(None, []).append(function)

    def _init_config(self):
        self._merge_config()
        PWebRegistry.config = self._config
        self._register_app_config()

    def _register_app_config(self):
        self._pweb_app.config.from_object(self._config)

    def _init_cors(self):
        CORS(self._pweb_app, resources={
            r"/api/*": {"origins": self._config.ALLOW_CORS_ORIGINS, "Access-Control-Allow-Origin": self._config.ALLOW_ACCESS_CONTROL_ORIGIN},
            r"/static/*": {"origins": self._config.ALLOW_CORS_ORIGINS, "Access-Control-Allow-Origin": self._config.ALLOW_ACCESS_CONTROL_ORIGIN}
        })

    def _merge_config(self):
        self._config = yaml_env.load(project_root_path=self._config.APP_CONFIG_PATH, config_obj=self._config)

    def _process_project_root_path(self, root_path):
        root_dir = os.path.dirname(os.path.abspath(root_path))
        self._config.set_base_dir(root_dir)
