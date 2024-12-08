import logging
from src.service.controller_service.crawl_controller import CrawlController

class TransformService:
    def __init__(self):
        # Khởi tạo CrawlController để sử dụng hàm call_staging_procedure
        self.crawl_controller = CrawlController()
        self.logger = logging.getLogger("TransformService")

    def transforms_data(self):
        """
        Hàm thực hiện transform dữ liệu từ Staging sang cấu trúc chuẩn.
        """
        self.logger.info("Bắt đầu transform dữ liệu từ Staging...")

        try:
            # Gọi stored procedure 'transforms_data' trên Staging Database
            result = self.crawl_controller.call_staging_procedure('transforms_data', ())

            # Log kết quả trả về (nếu cần)
            if result:
                self.logger.info(f"Transform thành công: {result}")
            else:
                self.logger.warning("Transform hoàn tất nhưng không có kết quả trả về.")
        except Exception as e:
            # Log lỗi nếu có
            self.logger.error(f"Lỗi khi transform dữ liệu: {e}")
