import os

from src.config.procedure import transform_batdongsan_com_vn, transform_muaban_net, \
    load_staging_warehouse_batdongsan_com_vn, load_staging_warehouse_muaban_net
from src.service.AppException import AppException, STATUS
from src.service.controller_service.database_controller import Controller
from src.service.notification_service.email import EmailTemplate, LABEL


class Transformation:
    def __init__(self,
                 source_name,
                 controller: Controller,
                 prefix,
                 file_format,
                 error_dir_path):
        self._source = source_name
        self._controller = controller
        self._prefix = prefix
        self._file_format = file_format
        self._error_dir_path = error_dir_path

    def handle(self):
        # 17.1 Khởi tạo count_row để đếm số dòng transform
        count_row = 0
        try:
            # 17.2 Kiểm tra source == 'batdongsan.com.vn'
            if self._source == 'batdongsan.com.vn':
                # 17.2.1 gọi hàm call_controller_procedure (4.1)
                # để bắt đầu transform data từ
                # estate_staging.estate_daily_temp_batdongsan_com_vn
                # sang estate_staging.estate_daily_batdongsan_com_vn
                # param: procedure transform_batdongsan_com_vn
                result = self._controller.call_staging_procedure(transform_batdongsan_com_vn, ())

                # 17.2.3 Lấy ra giá trị row_count từ procedure trên set lại vào row_count
                count_row = result['count_row']

            # 17.3 Kiểm tra source == 'muaban.net/bat-dong-san'
            elif self._source == 'muaban.net/bat-dong-san':

                # 17.3.1 gọi hàm call_controller_procedure (4.1)
                # để bắt đầu transform data từ
                # estate_staging.estate_daily_temp_muaban_net
                # sang estate_staging.estate_daily_muaban_net
                # param: procedure transform_muabna_net
                result = self._controller.call_staging_procedure(transform_muaban_net, ())

                # 17.3.2 Lấy ra giá trị row_count từ procedure trên set lại vào row_count
                count_row = result['count_row']
            else:
                # Ném ra ngoại lệ để báo source không tồn tại
                raise AppException(message='Source not found')
            # 17.5 Gọi hàm handle_success
            return self.handle_success(count_row)
        except AppException as e:
            # 17.4 Gọi hàm handle_exception
            return self.handle_exception(e)

    # 18
    def handle_success(self, count_row):
        # 18.1 Khởi tạo email template
        email_template = EmailTemplate(subject="TRANSFORMATION SUCCESS",
                                       status=STATUS.STAGING_PENDING.name,
                                       code=STATUS.STAGING_PENDING.value,
                                       message="Success",
                                       file_log=None,
                                       label=LABEL.INFO)

        # 18.2 Tiến hành gửi mail
        email_template.sent_mail()

        # 18.3 Trả về giá trị để cập nhập trạng thái lên controller
        return {
            'file': None,
            'error_file_name': None,
            'count_row': count_row,
            'status': 'STAGING_SUCCESS -> WAREHOUSE_PENDING'
        }

    def handle_exception(self, exception: AppException):
        # 19.1 Tạo file name error
        filename = f"{self._prefix}{self._file_format}.log"
        path = os.path.join(self._error_dir_path, filename)
        # 19.2 cài đặt file name error vào exception
        exception.file_error = filename
        exception._status = STATUS.STAGING_ERROR
        # 19.3 gọi hàm handler_exception trong exception (15)
        exception.handle_exception("TRANSFORMATION ERROR")
        # 19.4 Trả về giá trị gồm file, error file name, count row, status
        return {
            'file': None,
            'error_file_name': path,
            'count_row': 0,
            'status': 'STAGING_ERROR'
        }