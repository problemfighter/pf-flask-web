from typing import Optional
from flask import render_template, send_from_directory
from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.pf_flask_auth import pf_flask_auth
from pf_flask_mail.common.pffm_config import PFFMConfig
from pf_flask_rest.pf_flask_rest import pf_flask_rest
from pf_flask_swagger.common.pf_flask_swagger_config import PFFlaskSwaggerConfig
from pf_flask_swagger.flask.pf_flask_swagger import pf_flask_swagger
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
        self.init_static_resource_mapping()
        self._init_db()
        self._init_rest_engine()
        self._init_swagger_doc()
        self._init_auth_system()

    def _init_swagger_doc(self):
        PFFlaskSwaggerConfig.enable_pf_api_convention = True
        PFFlaskSwaggerConfig.enable_swagger_view_page = self._config.ENABLE_SWAGGER_VIEW_PAGE
        PFFlaskSwaggerConfig.enable_swagger_page_auth = self._config.ENABLE_SWAGGER_PAGE_AUTH
        PFFlaskSwaggerConfig.swagger_page_auth_user = self._config.SWAGGER_PAGE_AUTH_USER
        PFFlaskSwaggerConfig.swagger_page_auth_password = self._config.SWAGGER_PAGE_AUTH_PASSWORD

        swagger_title = self._config.SWAGGER_TITLE
        if not swagger_title:
            swagger_title = self._config.APP_NAME
        PFFlaskSwaggerConfig.title = swagger_title

        PFFlaskSwaggerConfig.version = self._config.SWAGGER_VERSION
        PFFlaskSwaggerConfig.enable_jwt_auth_global = self._config.SWAGGER_ENABLE_JWT_AUTH_GLOBAL

        if not isinstance(self._config.SKIP_URL_LIST, list):
            self._config.SKIP_URL_LIST = []
        self._config.SKIP_URL_LIST.append(PFFlaskSwaggerConfig.swagger_json_definition_url)
        self._config.SKIP_URL_LIST.append(PFFlaskSwaggerConfig.swagger_ui_url)

        if not isinstance(self._config.SKIP_START_WITH_URL_LIST, list):
            self._config.SKIP_START_WITH_URL_LIST = []
        self._config.SKIP_START_WITH_URL_LIST.append("/" + PFFlaskSwaggerConfig.swagger_static_folder)

        pf_flask_swagger.init_app(self._pweb_app)

    def _init_db(self):
        pweb_db.init_app(self._pweb_app)

    def _init_rest_engine(self):
        pf_flask_rest.init_app(self._pweb_app)

    def _init_email(self):
        self._email_config = PFFMConfig()
        PFFMConfig.smtpServer = self._email_config.smtpServer = self._config.EMAIL_SMTP_SERVER
        PFFMConfig.smtpSenderEmail = self._email_config.smtpSenderEmail = self._config.EMAIL_SMTP_SENDER_EMAIL
        PFFMConfig.smtpUser = self._email_config.smtpUser = self._config.EMAIL_SMTP_USER
        PFFMConfig.smtpPassword = self._email_config.smtpPassword = self._config.EMAIL_SMTP_PASSWORD
        PFFMConfig.smtpPort = self._email_config.smtpPort = self._config.EMAIL_SMTP_PORT
        PFFMConfig.smtpEncryption = self._email_config.smtpEncryption = self._config.EMAIL_SMTP_ENCRYPTION

    def _init_auth_system(self):
        if self._config.ENABLE_AUTH_SYSTEM:
            PFFAuthConfig.loginIdentifier = self._config.LOGIN_IDENTIFIER
            PFFAuthConfig.jwtSecret = self._config.JWT_SECRET
            PFFAuthConfig.jwtRefreshTokenValidityMin = self._config.JWT_REFRESH_TOKEN_VALIDITY_MIN
            PFFAuthConfig.jwtAccessTokenValidityMin = self._config.JWT_ACCESS_TOKEN_VALIDITY_MIN
            PFFAuthConfig.resetPasswordTokenValidMin = self._config.RESET_PASSWORD_TOKEN_VALID_MIN
            PFFAuthConfig.isStringImportSilent = self._config.STRING_IMPORT_SILENT
            PFFAuthConfig.operatorAdditionalFields = self._config.CUSTOM_OPERATOR_ADDITIONAL_FIELDS

            if self._config.SKIP_URL_LIST:
                PFFAuthConfig.skipUrlList.extend(self._config.SKIP_URL_LIST)

            if self._config.SKIP_START_WITH_URL_LIST:
                PFFAuthConfig.skipStartWithUrlList.extend(self._config.SKIP_START_WITH_URL_LIST)

            PFFAuthConfig.enableAPIAuth = self._config.ENABLE_API_AUTH
            PFFAuthConfig.enableSessionAuth = self._config.ENABLE_SESSION_AUTH
            PFFAuthConfig.enableAPIEndPoints = self._config.ENABLE_API_END_POINTS
            PFFAuthConfig.enableFormEndPoints = self._config.ENABLE_FORM_END_POINTS

            PFFAuthConfig.isCreateDefaultModel = self._config.ENABLE_DEFAULT_AUTH_MODEL
            PFFAuthConfig.customOperatorModel = self._config.CUSTOM_OPERATOR_MODEL
            PFFAuthConfig.customOperatorTokenModel = self._config.CUSTOM_OPERATOR_TOKEN_MODEL
            PFFAuthConfig.customOperatorDTO = self._config.CUSTOM_OPERATOR_DTO
            PFFAuthConfig.enablePFAPIConvention = True

            # ABC
            PFFAuthConfig.authInterceptOnVerifyABC = self._config.AUTH_INTERCEPT_ON_VERIFY
            PFFAuthConfig.authInterceptAPILoginTokenABC = self._config.AUTH_INTERCEPT_API_LOGIN_TOKEN
            PFFAuthConfig.authInterceptRenewTokenABC = self._config.AUTH_INTERCEPT_RENEW_TOKEN
            PFFAuthConfig.authInterceptOnAclABC = self._config.AUTH_INTERCEPT_ON_ACL

            login_view_name = self._config.LOGIN_VIEW_NAME
            if not login_view_name:
                login_view_name = self._config.APP_NAME
            PFFAuthConfig.loginViewName = login_view_name

            PFFAuthConfig.formUrlPrefix = self._config.FORM_URL_PREFIX
            PFFAuthConfig.apiURLStartWith = self._config.API_URL_START_WITH
            PFFAuthConfig.apiUrlPrefix = self._config.API_URL_PREFIX
            PFFAuthConfig.successRedirect = self._config.SUCCESS_REDIRECT

            PFFAuthConfig.emailFormAppBaseURL = self._config.AUTH_EMAIL_FORM_APP_BASE_URL
            PFFAuthConfig.emailRestAppBaseURL = self._config.AUTH_EMAIL_REST_APP_BASE_URL
            PFFAuthConfig.emailTemplatePath = self._config.AUTH_EMAIL_TEMPLATE_PATH
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
                        if not list_of_module:
                            return
                        for module in list_of_module:
                            if issubclass(module, PWebAppRegistry):
                                instance = module()
                                instance.register_model(pweb_db)

                        for module in list_of_module:
                            if issubclass(module, PWebAppRegistry):
                                instance = module()
                                instance.register_controller(self._pweb_app)
                                instance.run_on_start(self._pweb_app)

    def init_static_resource_mapping(self):
        if self._config.UPLOADED_STATIC_RESOURCES_URL and self._config.UPLOADED_STATIC_RESOURCES_URL != "":
            self._config.SKIP_START_WITH_URL_LIST.append(self._config.UPLOADED_STATIC_RESOURCES_URL)
            url = self._config.UPLOADED_STATIC_RESOURCES_URL + "/<path:path>"
            self._pweb_app.add_url_rule(url, view_func=self.static_resource_endpoint)

    def static_resource_endpoint(self, path):
        return send_from_directory(self._config.UPLOADED_STATIC_RESOURCES, path)
