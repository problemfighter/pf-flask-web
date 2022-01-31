from pf_flask_web.system12.pweb_interfaces import PWebAppRegistry


class ModuleRegistry(PWebAppRegistry):

    def run_on_start(self, pweb_app):
        pass

    def register_model(self, pweb_db):
        pass

    def register_controller(self, pweb_app):
        pass


module_registry = ModuleRegistry()
