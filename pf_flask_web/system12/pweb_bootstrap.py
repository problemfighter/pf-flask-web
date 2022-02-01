from typing import Optional
from flask import render_template

from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.pf_flask_auth import pf_flask_auth
from pf_flask_mail.common.pffm_config import PFFMConfig
from pf_flask_rest.pf_flask_rest import pf_flask_rest
from pf_flask_swagger.common.pf_flask_swagger_config import PFFlaskSwaggerConfig
from pf_flask_swagger.flask.pf_flask_swagger import PFFlaskSwagger, pf_flask_swagger
from pf_flask_web.system12.pweb import PWeb
from pf_flask_web.system12.pweb_app_config import PWebAppConfig
from pf_flask_web.system12.pweb_db import pweb_db
from pf_flask_web.system12.pweb_flask_util import PWebFlaskUtil
from pf_flask_web.system12.pweb_interfaces import PWebRegisterModule, PWebAppRegistry
from pf_py_common.pf_exception import PFException
from pf_py_common.py_common import PyCommon


class PwebBootstrap:
    _pweb_app: PWeb
    _config: PWebAppConfig = None
    _email_config: PFFMConfig = None

    def init_app(self, pweb_app, config: PWebAppConfig):
        self._config = config
        self._pweb_app = pweb_app
        self._init_email()
        self._register_modules()
        self._init_default_page()
        self._init_db()
        self._init_swagger_doc()

    def _init_swagger_doc(self):
        PFFlaskSwaggerConfig.enable_pf_api_convention = True
        PFFlaskSwaggerConfig.enable_swagger_view_page = self._config.ENABLE_SWAGGER_VIEW_PAGE
        PFFlaskSwaggerConfig.enable_swagger_page_auth = self._config.ENABLE_SWAGGER_PAGE_AUTH
        PFFlaskSwaggerConfig.swagger_page_auth_user = self._config.SWAGGER_PAGE_AUTH_USER
        PFFlaskSwaggerConfig.swagger_page_auth_password = self._config.SWAGGER_PAGE_AUTH_PASSWORD
        PFFlaskSwaggerConfig.title = self._config.SWAGGER_TITLE
        PFFlaskSwaggerConfig.version = self._config.SWAGGER_VERSION
        PFFlaskSwaggerConfig.enable_jwt_auth_global = self._config.SWAGGER_ENABLE_JWT_AUTH_GLOBAL
        pf_flask_swagger.init_app(self._pweb_app)

    def _init_db(self):
        pweb_db.init_app(self._pweb_app)

    def _init_rest_engine(self):
        pf_flask_rest.init_app(self._pweb_app)

    def _init_email(self):
        self._email_config = PFFMConfig()
        PFFMConfig.smtpServer = self._email_config.smtpServer = PWebAppConfig.EMAIL_SMTP_SERVER
        PFFMConfig.smtpSenderEmail = self._email_config.smtpSenderEmail = PWebAppConfig.EMAIL_SMTP_SENDER_EMAIL
        PFFMConfig.smtpUser = self._email_config.smtpUser = PWebAppConfig.EMAIL_SMTP_USER
        PFFMConfig.smtpPassword = self._email_config.smtpPassword = PWebAppConfig.EMAIL_SMTP_PASSWORD
        PFFMConfig.smtpPort = self._email_config.smtpPort = PWebAppConfig.EMAIL_SMTP_PORT
        PFFMConfig.smtpEncryption = self._email_config.smtpEncryption = PWebAppConfig.EMAIL_SMTP_ENCRYPTION

    def _init_auth_system(self):
        if self._config.ENABLE_AUTH_SYSTEM:
            PFFAuthConfig.loginIdentifier = PWebAppConfig.LOGIN_IDENTIFIER
            PFFAuthConfig.jwtSecret = PWebAppConfig.JWT_SECRET
            PFFAuthConfig.jwtRefreshTokenValidityMin = PWebAppConfig.JWT_REFRESH_TOKEN_VALIDITY_MIN
            PFFAuthConfig.jwtAccessTokenValidityMin = PWebAppConfig.JWT_ACCESS_TOKEN_VALIDITY_MIN
            PFFAuthConfig.resetPasswordTokenValidMin = PWebAppConfig.RESET_PASSWORD_TOKEN_VALID_MIN
            PFFAuthConfig.isStringImportSilent = PWebAppConfig.STRING_IMPORT_SILENT

            if PWebAppConfig.SKIP_URL_LIST:
                PFFAuthConfig.skipUrlList.extend(PWebAppConfig.SKIP_URL_LIST)

            if PWebAppConfig.SKIP_START_WITH_URL_LIST:
                PFFAuthConfig.skipStartWithUrlList.extend(PWebAppConfig.SKIP_START_WITH_URL_LIST)

            PFFAuthConfig.enableAPIAuth = PWebAppConfig.ENABLE_API_AUTH
            PFFAuthConfig.enableSessionAuth = PWebAppConfig.ENABLE_SESSION_AUTH
            PFFAuthConfig.enableAPIEndPoints = PWebAppConfig.ENABLE_API_END_POINTS
            PFFAuthConfig.enableFormEndPoints = PWebAppConfig.ENABLE_FORM_END_POINTS

            PFFAuthConfig.loginViewName = PWebAppConfig.LOGIN_VIEW_NAME
            PFFAuthConfig.formUrlPrefix = PWebAppConfig.FORM_URL_PREFIX
            PFFAuthConfig.apiURLStartWith = PWebAppConfig.API_URL_START_WITH
            PFFAuthConfig.apiUrlPrefix = PWebAppConfig.API_URL_PREFIX
            PFFAuthConfig.successRedirect = PWebAppConfig.SUCCESS_REDIRECT

            PFFAuthConfig.loginURL = PWebAppConfig.LOGIN_URL
            PFFAuthConfig.resetPasswordURL = PWebAppConfig.RESET_PASSWORD_URL
            PFFAuthConfig.forgotPasswordURL = PWebAppConfig.FORGOT_PASSWORD_URL
            PFFAuthConfig.renewTokenURL = PWebAppConfig.RENEW_TOKEN_URL
            PFFAuthConfig.logoutURL = PWebAppConfig.LOGOUT_URL

            PFFAuthConfig.emailFormAppBaseURL = PWebAppConfig.AUTH_EMAIL_FORM_APP_BASE_URL
            PFFAuthConfig.emailRestAppBaseURL = PWebAppConfig.AUTH_EMAIL_REST_APP_BASE_URL
            PFFAuthConfig.emailTemplatePath = PWebAppConfig.AUTH_EMAIL_TEMPLATE_PATH
            PFFAuthConfig.emailConfig = self._email_config

            pf_flask_auth.init_app(self._pweb_app)

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
                        list_of_module = modules.get_module_list()
                        for module in list_of_module:
                            if issubclass(module, PWebAppRegistry):
                                instance = module()
                                instance.register_model(pweb_db)

                        for module in list_of_module:
                            if issubclass(module, PWebAppRegistry):
                                instance = module()
                                instance.register_controller(self._pweb_app)
                                instance.run_on_start(self._pweb_app)
