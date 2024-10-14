from datetime import datetime

from service.extract_service.src.config.setting import LIMIT_PAGE
from service.extract_service.src.crawler.source_A_1_crawler import SourceA1Crawler
from service.extract_service.src.crawler.source_B_1_crawler import SourceB1Crawler
from service.extract_service.src.util.file_util import write_json_to_csv


def run_crawlers():
    run_crawler_source_B_1()
    # Initialize Source1Crawler
    # source1_crawler = Source1Crawler()
    # source1_crawler.setup_driver(headless=True)  # Headless browser option
    # # source1_crawler.setJwt()
    # data = source1_crawler.crawl()
    # # current_date = datetime.now().strftime("%H_%M__%d_%m_%Y")
    # # filename = f"source_1_{current_date}.csv"
    # # write_json_to_csv(filename, data)


def run_crawler_source_A_1():
    source1_crawler = SourceA1Crawler(LIMIT_PAGE)
    print(f"Started crawl at: {source1_crawler.base_url}")
    source1_crawler.handle()
def run_crawler_source_B_1():
    source1_crawler = SourceB1Crawler(LIMIT_PAGE)
    print(f"Started crawl at: {source1_crawler.base_url}")
    source1_crawler.handle()

if __name__ == "__main__":
    print("Running crawlers...")
    run_crawlers()