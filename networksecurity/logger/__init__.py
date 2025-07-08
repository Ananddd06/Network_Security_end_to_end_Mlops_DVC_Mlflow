import logging
import os
from datetime import datetime

class Custom_Logger:
    def __init__(self, log_dir: str = "logs", log_file: str = None):
        os.makedirs(log_dir, exist_ok=True)

        if not log_file:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file = f"{log_dir}/log_{now}.log"
        else:
            log_file = os.path.join(log_dir, log_file)

        self.logger = logging.getLogger("CustomLogger")
        self.logger.setLevel(logging.DEBUG)

        # Avoid duplicate handlers in Jupyter/Streamlit runs
        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_file)
            stream_handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] → %(message)s", 
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger
