# File: datawarehourse_nhom_1-main/src/service/controller_service/datamart_controller.py

import mysql.connector
from mysql.connector import Error

class Controller:
    def __init__(self, db_config):
        # Khởi tạo kết nối với database
        self.connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        self.cursor = self.connection.cursor()

    def call_get_log_datamart(self):
        try:
            # Gọi thủ tục get_log_datamart
            self.cursor.callproc('get_log_datamart')

            # Kiểm tra kết quả trả về từ procedure
            for result in self.cursor.stored_results():
                print(result.fetchall())

        except Error as e:
            print(f"Error: {e}")

        finally:
            self.cursor.close()
            self.connection.close()

# Cấu hình DB
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'estate_controller'
}

# Khởi tạo Controller và gọi thủ tục
controller = Controller(db_config)
controller.call_get_log_datamart()
