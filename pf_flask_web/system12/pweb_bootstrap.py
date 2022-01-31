from typing import Optional
from flask import render_template
from pf_flask_rest.pf_flask_rest import pf_flask_rest
from pf_flask_swagger.flask.pf_flask_swagger import PFFlaskSwagger
from pf_flask_web.system12.pweb import PWeb
from pf_flask_web.system12.pweb_app_config import PWebAppConfig
from pf_flask_web.system12.pweb_db import pweb_db
from pf_flask_web.system12.pweb_flask_util import PWebFlaskUtil
from pf_flask_web.system12.pweb_interfaces import PWebRegisterModule
from pf_py_common.pf_exception import PFException
from pf_py_common.py_common import PyCommon


class PwebBootstrap:
    _pweb_app: PWeb
    _config: PWebAppConfig = None

    def init_app(self, pweb_app, config: PWebAppConfig):
        self._config = config
        self._pweb_app = pweb_app
        self._register_modules()
        self._init_default_page()
        self._init_db()
        self._init_swagger_doc()

    def _init_swagger_doc(self):
        PFFlaskSwagger(self._pweb_app)

    def _init_db(self):
        pweb_db.init_app(self._pweb_app)

    def _init_rest_engine(self):
        pf_flask_rest.init_app(self._pweb_app)

    def _default_html(self):
        return render_template(self._config.DEFAULT_HTML)

    def _init_default_page(self):
        is_slash_registered = PWebFlaskUtil.is_url_register(self._pweb_app, self._config.DEFAULT_URL)
        if not is_slash_registered:
            self._pweb_app.add_url_rule(self._config.DEFAULT_URL, view_func=self._default_html)

    def _get_modules(self, module_registry_package) -> Optional[PWebRegisterModule]:
        app_config = PyCommon.import_from_string(module_registry_package, self._config.STRING_IMPORT_SILENT)
        if app_config:
            if not issubclass(app_config, PWebRegisterModule):
                raise PFException("Register Should be Implementation of PWebRegisterModule")
            return app_config()
        return None

    def _register_modules(self):
        module_registry_packages = self._config.MODULE_REGISTRY_PACKAGE
        if module_registry_packages and isinstance(module_registry_packages, list):
            for module_registry_package in module_registry_packages:
                modules = self._get_modules(module_registry_package)
                if modules:
                    with self._pweb_app.app_context():
                        modules.register_controller(self._pweb_app)
                        modules.register_model(pweb_db)
                        modules.run_on_start(self._pweb_app)
