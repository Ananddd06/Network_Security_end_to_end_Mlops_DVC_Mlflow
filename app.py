from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.exception.exception import CustomException
import sys

def main():
    try:
        # addition of 2 numbers
        num1 = 10
        num2 = 20
        result = num1 + num2
        log = Custom_Logger().get_logger()
        log.info(f"Addition Result: {result}")
        # Simulating an error
        if result > 25:
            raise ValueError("Result exceeds 25, which is not allowed.")
    except Exception as e:
        log = Custom_Logger().get_logger()
        raise CustomException(str(e), sys)

if __name__ == "__main__":
    try:
        main()
    except CustomException as e:
        log = Custom_Logger().get_logger()
        log.error(f"An error occurred: {e}")
        print(e)  # For demonstration purposes, you can remove this in production code