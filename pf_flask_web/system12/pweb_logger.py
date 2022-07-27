import logging
from pf_flask_web.system12.pweb_app_config import PWebAppConfig


class PWebLogger:
    logMan = None

    @staticmethod
    def debug(message):
        PWebLogger.logMan.log(logging.DEBUG, message)

    @staticmethod
    def info(message):
        PWebLogger.logMan.log(logging.INFO, message)

    @staticmethod
    def warning(message):
        PWebLogger.logMan.log(logging.WARNING, message)

    @staticmethod
    def error(message):
        PWebLogger.logMan.log(logging.ERROR, message)

    @staticmethod
    def critical(message):
        PWebLogger.logMan.log(logging.CRITICAL, message)


class PWebLogMan:
    _config: PWebAppConfig

    def init(self, config: PWebAppConfig):
        self._config = config
        PWebLogger.logMan = self
        if not config.PWEB_LOG_ENABLE:
            return
        configuration = {
            "encoding": 'utf-8',
            "level": logging.DEBUG,
            "format": 'PWeb: %(levelname)s: %(message)s'
        }
        if config.PWEB_LOG_FILE:
            configuration["filename"] = config.PWEB_LOG_FILE
        logging.basicConfig(**configuration)

    def log(self, level, message):
        if self._config and self._config.PWEB_LOG_ENABLE:
            logging.log(level=level, msg=message)
