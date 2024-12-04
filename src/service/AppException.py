import traceback
import logging
from enum import Enum

from src.service.notification_service.email import sent_mail, EmailCategory


class LEVEL(Enum):
    FILE_ERROR = 1
    STAGING_ERROR = 2
    WAREHOUSE_ERROR = 3
    DATAMART_ERROR = 4
    FILE_PENDING = 5
    STAGING_PENDING = 6
    WAREHOUSE_PENDING = 7
    DATAMART_PENDING = 8


# Các level lỗi để lưu log
LEVEL_ERROR = [LEVEL.FILE_ERROR, LEVEL.STAGING_ERROR, LEVEL.WAREHOUSE_ERROR, LEVEL.DATAMART_ERROR]


class AppException(Exception):
    def __init__(self, level: LEVEL = LEVEL.FILE_ERROR, message: str = None, file_name=None):
        self._message = message
        self._level = level
        self._file_name = file_name

    # 15
    def handle_exception(self):
        # 15.1 Kiểm tra level là thuộc level error
        if self._level in LEVEL_ERROR:
            self._handle_save_error_log()

        # 15.2 Kiểm tra message != None
        if self._message:
            # 15.2.1 Gọi hàm sent mail
            self._handle_sent_email()

    def _handle_save_error_log(self):
        stack_trace = traceback.format_exc()
        # 15.1.1 Cấu hình logging
        logging.basicConfig(
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),  # Output logs to console
                logging.FileHandler(f"{self._file_name}.log")  # Output logs to a file
            ]
        )
        # In lỗi ra console
        logging.error(f"{self._message}\nStack trace:\n{stack_trace}")

        # 15.1.2 lưu stack trace vào file
        logging.error(f"Error log saved {self._file_name}", exc_info=True)

    def _handle_sent_email(self):
        sent_mail(f"""
                            Level: {self._level.name}
                            Message: {self._message}        
                            File name: {self._file_name}
                            """, EmailCategory.ERROR)

    @property
    def file_error(self):
        return self._file_name

    @file_error.setter
    def file_error(self, file_name):
        self._file_name = file_name


