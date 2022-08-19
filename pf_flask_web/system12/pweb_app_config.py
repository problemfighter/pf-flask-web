import os
from pf_flask_auth.dto.default_dto import OperatorDTO
from pf_py_ymlenv.pfpy_config_obj import PFPYConfigObj
from pf_flask_auth.model.pffa_abstract_model import OperatorAbstract, OperatorTokenAbstract


class PWebAppConfig(PFPYConfigObj):
    BASE_DIR: str = None
    APP_CONFIG_PATH: str = None
    DEBUG: bool = True
    STRING_IMPORT_SILENT: bool = False
    SECRET_KEY: str = 'random_secret_key_base'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = None
    SWAGGER_ENABLE: bool = False
    DEFAULT_URL: str = None
    DEFAULT_HTML: str = 'bismillah.html'
    ALLOW_CORS_ORIGINS: list = ["*"]
    ALLOW_ACCESS_CONTROL_ORIGIN: str = "*"
    PORT: int = 1200
    HOST: str = "127.0.0.1"
    MODULE_REGISTRY_PACKAGE: list = ["application.config.registry.Register"]
    APPLICATION_CONFIGURATION: str = "application.config.app_config.Config"

    PWEB_LOG_ENABLE: bool = False
    PWEB_LOG_FILE: str = None

    # Auth Configuration
    ENABLE_AUTH_SYSTEM: bool = True
    LOGIN_IDENTIFIER: str = "email"  # email, username
    AUTH_INTERCEPT_ON_VERIFY: str = "application.config.auth_intercept.AuthInterceptOnVerify"
    AUTH_INTERCEPT_API_LOGIN_TOKEN: str = "application.config.auth_intercept.AuthInterceptAPILoginToken"
    AUTH_INTERCEPT_RENEW_TOKEN: str = "application.config.auth_intercept.AuthInterceptRenewToken"
    AUTH_INTERCEPT_ON_ACL: str = "application.config.auth_intercept.AuthInterceptOnAcl"
    AUTH_CUSTOM_LOGIN_PROCESSOR: str = "application.config.auth_intercept.AuthCustomLogin"

    JWT_SECRET: str = "PleaseChangeTheToken"
    JWT_REFRESH_TOKEN_VALIDITY_MIN: int = 45
    JWT_ACCESS_TOKEN_VALIDITY_MIN: int = 30
    RESET_PASSWORD_TOKEN_VALID_MIN: int = 150

    SKIP_URL_LIST: list = []
    SKIP_START_WITH_URL_LIST: list = []

    ENABLE_API_AUTH: bool = False
    ENABLE_API_END_POINTS: bool = False
    ENABLE_SESSION_AUTH: bool = True
    ENABLE_FORM_END_POINTS: bool = True

    CHECK_IS_ACTIVE: bool = True
    CHECK_IS_VERIFIED: bool = True

    # Model Customization
    ENABLE_DEFAULT_AUTH_MODEL: bool = True
    CUSTOM_OPERATOR_MODEL: OperatorAbstract = None
    CUSTOM_OPERATOR_TOKEN_MODEL: OperatorTokenAbstract = None
    CUSTOM_OPERATOR_DTO: OperatorDTO = None
    CUSTOM_OPERATOR_ADDITIONAL_FIELDS: list = None

    # Basic Configuration
    APP_NAME = "PWeb"

    # Auth End Points
    LOGIN_VIEW_NAME = None
    FORM_URL_PREFIX = "/"
    API_URL_START_WITH = "/api"
    API_URL_PREFIX = "/api/v1/operator"
    SUCCESS_REDIRECT = "/dashboard"

    # Auth Email Configuration
    AUTH_EMAIL_FORM_APP_BASE_URL: str = None
    AUTH_EMAIL_REST_APP_BASE_URL: str = None
    AUTH_EMAIL_TEMPLATE_PATH: str = None

    # Swagger Configuration
    ENABLE_SWAGGER_VIEW_PAGE: bool = False
    ENABLE_SWAGGER_PAGE_AUTH: bool = False
    SWAGGER_PAGE_AUTH_USER: str = "pweb"
    SWAGGER_PAGE_AUTH_PASSWORD: str = "pweb12#"
    SWAGGER_TITLE: str = None
    SWAGGER_VERSION: str = "1.0.0"
    SWAGGER_ENABLE_JWT_AUTH_GLOBAL: bool = False

    # Email Configuration
    EMAIL_SMTP_SERVER: str = None
    EMAIL_SMTP_SENDER_EMAIL: str = None
    EMAIL_SMTP_USER: str = None
    EMAIL_SMTP_PASSWORD: str = None
    EMAIL_SMTP_PORT: int = None
    EMAIL_SMTP_ENCRYPTION: str = "ssl"  # ssl or tls

    # Resource Management
    TEMP_DIR: str = None
    INTERNAL_DATA_DIR: str = None
    UPLOADED_STATIC_RESOURCES: str = None
    UPLOADED_STATIC_RESOURCES_URL: str = "/assets"

    pWebCustomConfiguration: dict = {}

    def get_custom_conf(self, key, default=None):
        if key in self.pWebCustomConfiguration:
            return self.pWebCustomConfiguration[key]
        return default

    def set_base_dir(self, path):
        if not self.BASE_DIR:
            self.BASE_DIR = path
            self.APP_CONFIG_PATH = path
            if not self.SQLALCHEMY_DATABASE_URI:
                self.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(self.BASE_DIR, 'pweb.sqlite3')
        if not self.UPLOADED_STATIC_RESOURCES:
            self.UPLOADED_STATIC_RESOURCES = os.path.join(self.BASE_DIR, "uploaded-resources")
        if not self.TEMP_DIR:
            self.TEMP_DIR = os.path.join(self.BASE_DIR, "pweb-temp")
        if not self.INTERNAL_DATA_DIR:
            self.INTERNAL_DATA_DIR = os.path.join(self.BASE_DIR, "pweb-internal")
        return self
