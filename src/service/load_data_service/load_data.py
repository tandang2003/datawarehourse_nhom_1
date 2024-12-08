import logging
from src.service.controller_service.crawl_controller import CrawlController

class LoadDataWarehouseService:
    def __init__(self):
        # Khởi tạo CrawlController để sử dụng hàm call_procedure
        self.crawl_controller = CrawlController()
        self.logger = logging.getLogger("LoadDataWarehouseService")

    def load_data_from_staging_to_warehouse(self):
        """
        Hàm thực hiện load dữ liệu từ Staging vào Warehouse.
        """
        self.logger.info("Bắt đầu load dữ liệu từ Staging vào Warehouse...")

        try:
            # Gọi stored procedure 'load_data_from_staging_to_warehouse'
            result = self.crawl_controller.call_staging_procedure('load_data_from_staging_to_warehouse', ())

            # Log kết quả trả về
            if result:
                self.logger.info(f"Load dữ liệu thành công: {result}")
            else:
                self.logger.warning("Load dữ liệu hoàn tất nhưng không có kết quả trả về.")
        except Exception as e:
            # Log lỗi nếu xảy ra
            self.logger.error(f"Lỗi khi load dữ liệu từ Staging vào Warehouse: {e}")
