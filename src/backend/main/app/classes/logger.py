import logging
from logging.handlers import RotatingFileHandler
import os

class Logger:
    def __init__(
        self,
        max_bytes=2000000,
        log_dir='logs',
        log_filename='app.log',
        formatter='%(asctime)s - %(levelname)s - %(message)s'
    ):
        # Ensure the log directory exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Initialize logger
        self._logger = logging.getLogger('app')

        # Verifica se o logger já tem handlers configurados
        if not self._logger.hasHandlers():  # Só adiciona handler se não houver nenhum
            self._logger.setLevel(logging.DEBUG)

            # Set up the log file handler
            log_path = os.path.join(log_dir, log_filename)
            file_handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=5)
            file_handler.setLevel(logging.INFO)

            # Set up the formatter
            file_handler.setFormatter(logging.Formatter(formatter))

            # Add handler to logger
            self._logger.addHandler(file_handler)
