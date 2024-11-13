from src.config.procedure import get_log_crawler
from src.service.controller_service.database_controller import Controller
from src.service.extract_service.crawler.paging_base_crawler import PagingBase


class CrawlController(Controller):
    def __init__(self):
        super().__init__()

    def get_config(self):
        data = self.call_controller_procedure(get_log_crawler, ())
        crawl = PagingBase(limit_page=data['limit_page'], format_file=data['format_file'], extension=data['extension'],
                           prefix=data['prefix'], dir_path=data['dir_path'], purpose=data['purpose'],
                           base_url=data['base_url'], source_page=data['source_page'],
                           paging_pattern=data['paging_pattern'], scenario=data['scenario'])
        result = crawl.handle()

        self.call_controller_procedure('insert_log_crawler', (data['id'],), result['file'], result['error_file_name'],
                                       result['count_row'], result['status'])


if __name__ == '__main__':
    c = CrawlController()
    c.get_config()
