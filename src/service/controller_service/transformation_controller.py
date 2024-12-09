from src.config.procedure import get_log_transform, insert_log_transform
from src.service.controller_service.database_controller import Controller
from src.service.transformation_service.transformation_service import Transformation


class TransformationController(Controller):
    def __init__(self):
        super().__init__()

    def get_config(self):
        # 16.2 Gọi hàm call_procedure (4.1) để lấy cấu hình cho transform
        data = self.call_controller_procedure(get_log_transform, ())

        # 16.3 kiểm tra các thông số cấu hình lấy về data != None
        if data is None:
            # 6.3.1 Không lấy được cấu hình
            return

        # 16.3.2 Lấy được cấu hình
        # 16.4 Khởi tạo đối tượng Transformation với các thông số lấy về từ database
        transformation = Transformation(source_name=data['source_name'],
                                        file_format=data['file_format'],
                                        prefix=data['prefix'],
                                        error_dir_path=data['error_dir_path'],
                                        controller=self)

        # 16.5. Gọi PagingBase.handle() (17) để tiến hành transform data
        result = transformation.handle()

        # 16.6 Gọi hàm call_procedure (4.2) để thực hiện procedure insert_log_transform
        self.call_controller_procedure(insert_log_transform, (
            data['id'],
            result['count_row'],
            result['error_file_name'],
            result['status']))


if __name__ == '__main__':
    c = TransformationController()
    c.get_config()
