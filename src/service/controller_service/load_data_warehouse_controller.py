from src.service.controller_service.database_controller import Controller
from src.config.procedure import test_procedure

class LoadDataWarehouseController:
    def __init__(self):
        self.controller = Controller()

    def load_data_from_staging_to_warehouse(self):
        """Load data từ Staging DB vào Warehouse DB."""
        try:
            result = self.controller.call_staging_procedure(test_procedure, ())
            if result:
                print("Procedure result:", result)  # In ra kết quả trả về từ procedure
            else:
                print("No result returned from procedure.")
            print("Loaded data from staging to warehouse successfully.")
        except Exception as e:
            print(f"Error loading data from staging to warehouse: {e}")

# Hàm main để kiểm tra chức năng của LoadDataWarehouseController
if __name__ == "__main__":
    # Tạo đối tượng của LoadDataWarehouseController
    loader = LoadDataWarehouseController()

    # Gọi hàm load_data_from_staging_to_warehouse để kiểm tra
    loader.load_data_from_staging_to_warehouse()