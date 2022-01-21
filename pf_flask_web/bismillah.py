import os
import typing as t
from flask_cors import CORS
from pf_flask_web.system12.pweb import PWeb
from pf_flask_web.system12.pweb_app_config import PWebAppConfig
from pf_flask_web.system12.pweb_registry import PWebRegistry
from pf_py_ymlenv import yaml_env


class Bismillah(object):
    _pweb_app: PWeb
    _config: PWebAppConfig = None

    def __init__(
        self,
        project_root_path,
        config=PWebAppConfig(),
        name: str = "PWebApp",
        static_url_path: t.Optional[str] = None,
        static_folder: t.Optional[t.Union[str, os.PathLike]] = "static",
        static_host: t.Optional[str] = None,
        host_matching: bool = False,
        subdomain_matching: bool = False,
        template_folder: t.Optional[str] = "templates",
        instance_path: t.Optional[str] = None,
        instance_relative_config: bool = False,
        root_path: t.Optional[str] = None,
    ):
        self._pweb_app = PWeb(
            name,
            static_url_path=static_url_path,
            static_folder=static_folder,
            static_host=static_host,
            host_matching=host_matching,
            subdomain_matching=subdomain_matching,
            template_folder=template_folder,
            instance_path=instance_path,
            instance_relative_config=instance_relative_config,
            root_path=root_path,
        )
        self._config = config
        self._process_project_root_path(root_path=project_root_path)
        self._init_config()
        self._init_cors()

    def run(self):
        self._pweb_app.run(host=self._config.HOST, port=self._config.PORT, load_dotenv=False)

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
