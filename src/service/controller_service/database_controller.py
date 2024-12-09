from src.config.database import MySQLCRUD
from src.config.setting import CONTROLLER_DB_PORT, CONTROLLER_DB_HOST, CONTROLLER_DB_NAME, CONTROLLER_DB_USER, \
    CONTROLLER_DB_PASS, CONTROLLER_DB_POOL_NAME, CONTROLLER_DB_POOL_SIZE


class Controller:
    __connector: MySQLCRUD = None

    def __init__(self):
        self.__connector = MySQLCRUD(
            host=CONTROLLER_DB_HOST,
            port=CONTROLLER_DB_PORT,
            database=CONTROLLER_DB_NAME,
            user=CONTROLLER_DB_USER,
            password=CONTROLLER_DB_PASS,
            pool_name=CONTROLLER_DB_POOL_NAME,
            pool_size=CONTROLLER_DB_POOL_SIZE
        )

        print(f"Connection pool created with pool size: {CONTROLLER_DB_POOL_SIZE}")

    def call_controller_procedure(self, procedure_name, args):
        # 1.Kiểm tra trong quá trình lấy connection có lỗi sảy ra không
        try:
            # 2. tạo connection controller bằng hàm get_controller_connection
            connection = self.__connector.get_controller_connection()
            # 3.sử dụng hàm call_procedure(3) với tên procedure, connection lấy được và các tham số cần thiết
            result = self.__connector.call_procedure(procedure_name, connection, args)
            # 4.trả về kết quả
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None
    def get_staging_connection(self):
        return self.__connector.get_staging_connection()
    def call_staging_procedure(self, procedure_name, args):
        # 1.Kiểm tra trong quá trình lấy connection có lỗi sảy ra không
        try:
            # 2. tạo connection staging bằng hàm get_controller_connection
            connection = self.__connector.get_staging_connection()
            # 3.sử dụng hàm call_procedure(3) với tên procedure, connection lấy được và các tham số cần thiết
            result = self.__connector.call_procedure(procedure_name, connection, args)
            # 4.trả về kết quả
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None

    def call_warehouse_procedure(self, procedure_name, args, header):
        # 1.Kiểm tra trong quá trình lấy connection có lỗi sảy ra không
        try:
            # 2. tạo connection warehouse bằng hàm get_controller_connection
            connection = self.__connector.get_warehouse_connection()
            # 3.sử dụng hàm call_procedure(3) với tên procedure, connection lấy được và các tham số cần thiết
            result = self.__connector.call_procedure(procedure_name, connection, args)
            # 4.trả về kết quả
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None
    def call_datamart_procedure(self, procedure_name, args, header):
        # 1.Kiểm tra trong quá trình lấy connection có lỗi sảy ra không
        try:
            # 2. tạo connection datamart bằng hàm get_controller_connection
            connection = self.__connector.get_datamart_connection()
            # 3.sử dụng hàm call_procedure(3) với tên procedure, connection lấy được và các tham số cần thiết
            result = self.__connector.call_procedure(procedure_name, connection, args)
            # 4.trả về kết quả
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None