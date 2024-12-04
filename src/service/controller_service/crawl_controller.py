from src.config.procedure import get_log_crawler
from src.service.controller_service.database_controller import Controller
from src.service.extract_service.crawler.base_crawler import BaseCrawler
from src.service.extract_service.crawler.paging_base_crawler import PagingBase


class CrawlController(Controller):
    def __init__(self):
        super().__init__()

    def get_config(self):
        # 6.2 Gọi hàm call_procedure (4.1) để lấy cấu hình cho crawler
        data = self.call_controller_procedure(get_log_crawler, ())

        # 6.3 Kiểm tra các thông ố lấy về data != None
        if data is None :
            # 6.3.1 Không lấy được cấu hình
            return

        # 6.3.2 Lấy được cấu hình
        # 6.4 Khởi tạo đối tượng PagingBase với các thông số lấy về từ database
        print(data)
        crawl = PagingBase(limit_page=data['limit_page'],
                           format_file=data['file_format'],
                           extension=data['file_extension'],
                           prefix=data['prefix'],
                           data_dir_path=data['data_dir_path'],
                           error_dir_path=data['error_dir_path'],
                           purpose=data['purpose'],
                           base_url=data['base_url'],
                           source_page=data['source_page'],
                           paging_pattern=data['paging_pattern'],
                           scenario=data['scenario'],
                           navigate_scenario=data['navigate_scenario'])

        # 6.5. Gọi PagingBase.handle() (2) để tiến hành crawl data
        result = crawl.handle()

        # 6.6 Gọi hàm call_procedure (4.2) để insert log crawler
        self.call_controller_procedure('insert_log_crawler', (
            data['id'],
            result['file'],
            result['error_file_name'],
            result['count_row'],
            result['status']))


if __name__ == '__main__':
    c = CrawlController()
    c.get_config()
