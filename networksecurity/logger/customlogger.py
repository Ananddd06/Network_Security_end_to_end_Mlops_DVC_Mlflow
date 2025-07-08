import os
import logging
from datetime import datetime

class Custom_Logger:
    def get_logger(self):
        # Get the absolute path to the project root (where app.py is located)
        project_root = os.path.dirname(os.path.abspath(__file__))
        while not os.path.exists(os.path.join(project_root, "app.py")):
            parent = os.path.dirname(project_root)
            if parent == project_root:
                break  # Reached the filesystem root
            project_root = parent

        log_dir = os.path.join(project_root, "log")  # <-- use 'log' not 'logs'
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

        logger = logging.getLogger("CustomLogger")
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file)

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] → %(message)s')
        fh.setFormatter(formatter)
        
        if not logger.hasHandlers():
            logger.addHandler(fh)
        return logger


# ✅ Example usage directly in the same Python file
if __name__ == "__main__":
    log = Custom_Logger().get_logger()

    log.debug("🔍 Debug info for development")
    log.info("✅ Model training started")
    log.error("❌ Error encountered during model training")
    log.warning("⚠️ Null values detected")
    log.critical("🔥 Critical failure in pipeline")
