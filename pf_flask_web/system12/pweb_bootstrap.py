from flask import render_template

from pf_flask_web.system12.pweb import PWeb
from pf_flask_web.system12.pweb_app_config import PWebAppConfig
from pf_flask_web.system12.pweb_flask_util import PWebFlaskUtil


class PwebBootstrap:
    _pweb_app: PWeb
    _config: PWebAppConfig = None

    def init_app(self, pweb_app, config: PWebAppConfig):
        self._config = config
        self._pweb_app = pweb_app
        self._init_default_page()

    def _init_swagger_doc(self):
        pass

    def _init_db(self):
        pass

    def _init_rest_engine(self):
        pass

    def _default_html(self):
        return render_template(self._config.DEFAULT_HTML)

    def _init_default_page(self):
        is_slash_registered = PWebFlaskUtil.is_url_register(self._pweb_app, self._config.DEFAULT_URL)
        if not is_slash_registered:
            self._pweb_app.add_url_rule(self._config.DEFAULT_URL, view_func=self._default_html)
