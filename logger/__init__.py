import os
import logging

levels = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}

logger_name = "FOLDER-SYNC"

class Logger:
    
    def __init__(self, log_path, debug=False):
        try:
            log_level = levels.get("INFO" if not debug else "DEBUG", logging.DEBUG)

            logger = logging.getLogger(logger_name)
            logger.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            handler = logging.StreamHandler()
            handler.setLevel(log_level)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            if not os.path.isdir(f'{log_path}'):
                try:
                    path = os.getcwd()
                    os.mkdir(f'{log_path}')
                except OSError as e:
                    print(f"Creation of the directory {log_path} failed {e}")

            handler = logging.FileHandler(f"{log_path}/{logger_name}.log")

            handler.setLevel(log_level)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        except Exception as e:
            raise RuntimeError(f"Error initializing logger: {str(e)}")

    @staticmethod
    def debug(msg: str, name=logger_name) -> None:
        logger = logging.getLogger(name)
        logger.debug(msg)
    
    @staticmethod
    def info(msg: str, name=logger_name) -> None:
        logger = logging.getLogger(name)
        logger.info(msg)

    @staticmethod
    def warning(msg: str, name=logger_name) -> None:
        logger = logging.getLogger(name)
        logger.warning(msg)

    @staticmethod
    def error(msg: str, name=logger_name) -> None:
        logger = logging.getLogger(name)
        logger.error(msg)
