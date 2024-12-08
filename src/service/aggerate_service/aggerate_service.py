import logging
from src.service.controller_service.crawl_controller import CrawlController

class AggregateService:
    def __init__(self):
        # Khởi tạo CrawlController để sử dụng hàm call_procedure
        self.crawl_controller = CrawlController()
        self.logger = logging.getLogger("AggregateService")

    def load_data_from_warehouse_to_data_mart(self):
        """
        Hàm thực hiện load dữ liệu từ Warehouse vào Data Mart.
        """
        self.logger.info("Bắt đầu load dữ liệu từ Warehouse vào Data Mart...")

        try:
            # Gọi stored procedure 'load_data_from_warehouse_to_data_mart'
            result = self.crawl_controller.call_warehouse_procedure('load_data_from_warehouse_to_data_mart', ())

            # Log kết quả trả về
            if result:
                self.logger.info(f"Load dữ liệu thành công: {result}")
            else:
                self.logger.warning("Load dữ liệu hoàn tất nhưng không có kết quả trả về.")
        except Exception as e:
            # Log lỗi nếu xảy ra
            self.logger.error(f"Lỗi khi load dữ liệu từ Warehouse vào Data Mart: {e}")
