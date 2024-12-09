from src.service.controller_service.load_data_warehouse_controller import LoadDataWarehouseController

def main():
    """
    Hàm chính để thực thi workflow load dữ liệu từ staging vào warehouse.
    """
    print("=== Start Data Loading Workflow ===")
    loader = LoadDataWarehouseController()

    try:
        # Thực thi workflow
        loader.execute_procedure_sequence_loadStagingToWareHouse()
    except Exception as e:
        print(f"Error in workflow execution: {e}")
    finally:
        print("=== End Data Loading Workflow ===")

if __name__ == "__main__":
    main()
