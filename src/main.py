from src.config.setting import LIMIT_PAGE
from src.service.extract_service.crawler.source_A_1_crawler import SourceA1Crawler
from src.service.extract_service.crawler.source_B_1_crawler import SourceB1Crawler


def run_crawlers():
    # run_crawler_source_A_1()
    run_crawler_source_B_1()


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
    # result = get_config()
    run_crawlers()
