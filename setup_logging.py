import logging
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.handlers.TimedRotatingFileHandler('my_app.log', when="M", interval=1, backupCount=10)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler2 = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(handler2)


def call_log(func):
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"Starting function {func.__name__}")
            result = func(*args, **kwargs)
            logger.info(f"Ending function {func.__name__}")
            return result
        except Exception as e:
            logger.info(f"Exception {e} was caught in function {func.__name__}")
    return wrapper
