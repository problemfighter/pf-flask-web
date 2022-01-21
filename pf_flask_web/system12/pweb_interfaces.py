from abc import abstractmethod, ABC


class PWebRegisterModule(ABC):

    @abstractmethod
    def register_model_controller(self, pweb_app):
        pass

    @abstractmethod
    def run_on_start(self, pweb_app):
        pass


class PWebAppRegistry(ABC):

    @abstractmethod
    def register_model(self):
        pass

    @abstractmethod
    def register_controller(self, pweb_app):
        pass

    @abstractmethod
    def run_on_start(self, pweb_app):
        pass
