import sys
import traceback
from networksecurity.logger import Custom_Logger  # adjust the path as per your project structure

log = Custom_Logger().get_logger()

class CustomException(Exception):
    """
    Custom exception class for detailed error handling in production ML pipelines.
    Captures filename, line number, traceback, and logs it using a custom logger.
    """

    def __init__(self, error_message: str, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self._get_detailed_error_message(error_message, error_detail)
        log.error(self.error_message)  # Automatically log the error when raised

    def _get_detailed_error_message(self, error_message: str, error_detail: sys) -> str:
        """
        Returns detailed error message including:
        - Error description
        - File name
        - Line number
        - Exception type
        """
        exc_type, exc_obj, tb = error_detail.exc_info()
        if tb:
            last_trace = traceback.extract_tb(tb)[-1]
            file_name = last_trace.filename
            line_number = last_trace.lineno
            return (
                f"\n🛑 Exception Occurred:\n"
                f"🔤 Message    : {error_message}\n"
                f"📄 File       : {file_name}\n"
                f"🔢 Line       : {line_number}\n"
                f"📌 Trace Type : {exc_type.__name__}"
            )
        else:
            return f"Error occurred, but traceback is missing: {error_message}"

    def __str__(self):
        return self.error_message
