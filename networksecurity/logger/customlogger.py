import os
import logging
from datetime import datetime

class Custom_Logger:
    def get_logger(self):
        # Start from current file and move up until we find 'app.py'
        current_path = os.path.abspath(__file__)
        project_root = current_path
        while not os.path.exists(os.path.join(project_root, "app.py")):
            parent = os.path.dirname(project_root)
            if parent == project_root:  # Reached filesystem root
                break
            project_root = parent

        # Create a global log folder just outside your main source folders
        log_dir = os.path.join(project_root, "log")
        os.makedirs(log_dir, exist_ok=True)

        # Create a unique log file with timestamp
        log_file = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

        logger = logging.getLogger("CustomLogger")
        logger.setLevel(logging.DEBUG)

        # Prevent duplicate handlers if logger is reused
        if not logger.hasHandlers():
            fh = logging.FileHandler(log_file)
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] → %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)

            # Optional: log to console as well
            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            logger.addHandler(sh)

        return logger
