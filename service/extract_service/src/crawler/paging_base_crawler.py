from abc import abstractmethod

from service.extract_service.src.crawler.base_crawler import BaseCrawler
from service.extract_service.src.util.validation_util import check_url_valid


class PagingBase(BaseCrawler):

    def __init__(self, limit_page):
        super().__init__()
        self._current_page = 1
        self._limit_page = limit_page
        # # Chứa danh sách url item
        self._list_url = []
        # Chứa danh sách item đã cào được
        self._list_item = []

    def handle(self):
        super().setup_driver(headless=True)
        self.before_run()

        for (page) in range(1, self._limit_page):
            list_url = self.crawl_page(page)
            list_item_each_page = []
            for (url) in list_url:
                try:
                    if not check_url_valid(url):
                        raise NameError
                    item_crawled = self.crawl_item(url)
                    self._list_item.append(item_crawled)
                    self.after_run_each_item(item_crawled)
                except NameError:
                    self.handle_error_item(NameError)
            self.after_run_each_page(list_item_each_page)
            list_item_each_page.clear()
            self._current_page += 1

        self.after_run()

    @abstractmethod
    def crawl_item(self, url):
        pass

    @abstractmethod
    def crawl_page(self, page):
        pass

    def before_run(self):
        pass

    def after_run(self):
        pass

    def after_run_each_page(self, list_item):
        pass

    def after_run_each_item(self, item):
        pass

    def handle_error_item(self, error):
        pass
