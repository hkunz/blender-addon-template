import logging
import re

class AnsiFilter(logging.Filter):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

    def filter(self, record):
        record.msg = self.ansi_escape.sub('', str(record.msg))
        return True

def configure_logging(enable=True):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if enable else logging.CRITICAL)
    
    if logger.hasHandlers():
        return

    stream_handler = logging.StreamHandler()  # Console handler

    file_handler = logging.FileHandler('app.log', mode='w')  # overwrite instead of append
    file_handler.addFilter(AnsiFilter())

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
