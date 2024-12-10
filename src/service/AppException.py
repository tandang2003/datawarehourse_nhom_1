import logging
import traceback
from enum import Enum

from selenium.common import WebDriverException

from src.service.notification_service.email import EmailTemplate, LABEL


class STATUS(Enum):
    FILE_ERROR = "001"
    FILE_PENDING = "002"
    STAGING_ERROR = "003"
    STAGING_PENDING = "004"
    WAREHOUSE_ERROR = "005"
    WAREHOUSE_PENDING = "006"
    DATAMART_ERROR = "007"
    DATAMART_PENDING = "008"


# Các status lỗi để lưu log
STATUS_ERROR = [STATUS.FILE_ERROR, STATUS.STAGING_ERROR, STATUS.WAREHOUSE_ERROR, STATUS.DATAMART_ERROR]


class AppException(Exception):
    def __init__(self, status=None, message: str = None, file_name=None):
        self._message = message
        self._status = status
        self._file_name = file_name

    # 15
    def handle_exception(self):
        # 15.1 Kiểm tra level là thuộc level error
        if self._status is not None and self._status in STATUS_ERROR:
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
        email_template = EmailTemplate(subject="Test",
                                       status=self._status.name,
                                       code=self._status.value,
                                       message=self._message,
                                       file_log=self._file_name,
                                       label=LABEL.ERROR)
        email_template.sent_mail()

    @property
    def file_error(self):
        return self._file_name

    @file_error.setter
    def file_error(self, file_name):
        self._file_name = file_name
