import os
from pf_py_ymlenv.pfpy_config_obj import PFPYConfigObj


class PWebAppConfig(PFPYConfigObj):
    BASE_DIR: str = None
    APP_CONFIG_PATH: str = None
    DEBUG: bool = True
    STRING_IMPORT_SILENT: bool = True
    SECRET_KEY: str = 'random_secret_key_base'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = None
    SWAGGER_ENABLE: bool = False
    DEFAULT_URL: str = '/'
    DEFAULT_HTML: str = 'bismillah.html'
    ALLOW_CORS_ORIGINS: list = ["*"]
    ALLOW_ACCESS_CONTROL_ORIGIN: str = "*"
    PORT: int = 1200
    HOST: str = "127.0.0.1"
    MODULE_REGISTRY_PACKAGE: list = ["application.config.registry.Register"]
    APPLICATION_CONFIGURATION: str = "application.config.app_config.Config"

    # Auth Configuration
    LOGIN_IDENTIFIER: str = "email"
    ENABLE_AUTH_SYSTEM: bool = True
    AUTH_INTERCEPT_ON_VERIFY: str = "application.config.auth_intercept.AuthInterceptOnVerify"
    AUTH_INTERCEPT_API_LOGIN_TOKEN: str = "application.config.auth_intercept.AuthInterceptAPILoginToken"
    AUTH_INTERCEPT_RENEW_TOKEN: str = "application.config.auth_intercept.AuthInterceptRenewToken"
    AUTH_INTERCEPT_ON_ACL: str = "application.config.auth_intercept.AuthInterceptOnAcl"

    JWT_SECRET: str = "PleaseChangeTheToken"
    JWT_REFRESH_TOKEN_VALIDITY_MIN: int = 45
    JWT_ACCESS_TOKEN_VALIDITY_MIN: int = 30
    RESET_PASSWORD_TOKEN_VALID_MIN: int = 150

    SKIP_URL_LIST: list = []
    SKIP_START_WITH_URL_LIST: list = []

    def set_base_dir(self, path):
        if not self.BASE_DIR:
            self.BASE_DIR = path
            self.APP_CONFIG_PATH = path
            if not self.SQLALCHEMY_DATABASE_URI:
                self.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(self.BASE_DIR, 'pweb.sqlite3')
        return self
