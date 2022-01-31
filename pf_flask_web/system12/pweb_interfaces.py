from abc import abstractmethod, ABC


class PWebRegisterModule(ABC):

    @abstractmethod
    def get_module_list(self) -> list:
        pass


class PWebAppRegistry(ABC):

    @abstractmethod
    def register_model(self, pweb_db):
        pass

    @abstractmethod
    def register_controller(self, pweb_app):
        pass

    @abstractmethod
    def run_on_start(self, pweb_app):
        pass
