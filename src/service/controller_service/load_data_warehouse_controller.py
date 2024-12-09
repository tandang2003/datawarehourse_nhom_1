from src.service.controller_service.database_controller import Controller
from src.config.procedure import *


class LoadDataWarehouseController:
    #1 gọi đến controller để lấy thông tin và gọi đến các kết nối db controller, db staging, db warehouse
    def __init__(self):
        self.controller = Controller()


    def execute_procedure_sequence_loadStagingToWareHouse(self):
        """Chạy lần lượt các procedure theo thứ tự."""
        #2 tao mot danh sach procedure để xử lý tuần tự
        procedures = [
            "CreateTable_temp_estate_update",
            "InsertSource1IntoTempEstateUpdate",
            "InsertSource2IntoTempEstateUpdate",
            "UpdateExpiredStatus",
            "InsertIntoFactEstate",
            "InsertNewRecordsIntoWarehouse"
        ]

        for procedure in procedures:
            try:
                print(f"Executing procedure: {procedure}...")
                #3 gọi hàm call_staging_procedure để chạy tuần tự với từng procedure tương ứng
                result = self.controller.call_staging_procedure(procedure, ())
                #6 in ra kết quả với mỗi lần chạy
                if result is None:
                    print(f"No result returned from procedure: {procedure}.")
                else:
                    print(f"Procedure {procedure} executed successfully.")
            # 7 Kiem tra loi
            except Exception as e:
                #8 in ra lỗi tuuowng ứng
                print(f"Error executing procedure {procedure}: {e}")
                break  # Dừng lại nếu xảy ra lỗi


