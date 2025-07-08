import logging
import os
from datetime import datetime

class Custom_Logger:
    def __init__(self, log_dir: str = "logs", log_file: str = None, logger_name: str = "CustomLogger"):
        """
        A production-grade custom logger to log messages to both file and console.
        Useful for ML pipelines, Streamlit, Flask apps, or any Python backend.
        """
        os.makedirs(log_dir, exist_ok=True)

        # Create timestamped log file if not provided
        if not log_file:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file = os.path.join(log_dir, f"log_{now}.log")
        else:
            log_file = os.path.join(log_dir, log_file)

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False  # Avoid duplicate logging in notebooks/apps

        if not self.logger.handlers:
            # File Handler
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s] → %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_formatter)

            # Console Handler
            stream_handler = logging.StreamHandler()
            stream_formatter = logging.Formatter("[%(levelname)s] → %(message)s")
            stream_handler.setFormatter(stream_formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger


# ✅ Example usage directly in the same Python file
if __name__ == "__main__":
    log = Custom_Logger().get_logger()

    log.debug("🔍 Debug info for development")
    log.info("✅ Model training started")
    log.warning("⚠️ Null values detected")
    try:
        x = 1 / 0  # Simulated error
    except Exception as e:
        log.error(f"❌ Exception occurred: {e}")
    log.critical("🔥 Critical failure in pipeline")
