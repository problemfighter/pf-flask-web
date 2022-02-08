from pf_flask_auth.common.pffa_auth_interceptor_abc import AuthInterceptOnVerifyABC, AuthInterceptAPILoginTokenABC, AuthInterceptRenewTokenABC, AuthInterceptOnAclABC
from pf_flask_auth.common.pffa_model_dto_conf import PFFAModelDTOConf
from pf_flask_auth.data.pffa_form_auth_data import FormAuthData
from pf_flask_rest_com.data.pffrc_request_info import PFFRCRequestInfo

Operator = PFFAModelDTOConf.OperatorModel


class AuthInterceptOnVerify(AuthInterceptOnVerifyABC):
    def process(self, operator: Operator, operator_service, is_api: bool) -> Operator:
        pass


class AuthInterceptAPILoginToken(AuthInterceptAPILoginTokenABC):
    def process(self, response_map: dict, operator: Operator, operator_api_service) -> dict:
        pass


class AuthInterceptRenewToken(AuthInterceptRenewTokenABC):
    def process(self, response_map: dict, requested_jwt_payload: dict, operator_api_service) -> dict:
        pass


class AuthInterceptOnAcl(AuthInterceptOnAclABC):
    def process(self, url_info: PFFRCRequestInfo, payload: dict = None, form_auth_data: FormAuthData = None, is_api: bool = False):
        pass
