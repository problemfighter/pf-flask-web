from typing import Optional
from pf_flask_web.system12.pweb_interfaces import PWebAppRegistry, PWebRegisterModule
from pf_py_common.pf_exception import PFException
from pf_py_common.py_common import PyCommon


class PWebModuleOperation:

    def get_modules(self, module_registry_package, config) -> Optional[PWebRegisterModule]:
        app_config = PyCommon.import_from_string(module_registry_package, config.STRING_IMPORT_SILENT)
        if app_config:
            if not issubclass(app_config, PWebRegisterModule):
                raise PFException("Register Should be Implementation of PWebRegisterModule")
            return app_config()
        return None

    def run_module_cli_init(self, config, pweb_app):
        module_registry_packages = config.MODULE_REGISTRY_PACKAGE
        if module_registry_packages and isinstance(module_registry_packages, list):
            for module_registry_package in module_registry_packages:
                modules = self.get_modules(module_registry_package, config)
                if modules:
                    with pweb_app.app_context():
                        list_of_module = modules.get_module_list()
                        if not list_of_module:
                            return
                        for module in list_of_module:
                            if issubclass(module, PWebAppRegistry):
                                instance = module()
                                if hasattr(instance, "run_on_cli_init"):
                                    instance.run_on_cli_init(pweb_app)
