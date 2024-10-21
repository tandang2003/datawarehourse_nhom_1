import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType


class BaseCrawler:
    def __init__(self):
        self.driver: webdriver
        self.soup: BeautifulSoup

    def setup_driver(self, headless=False, disable_resource=False):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")
        chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--log-level=3")
        if headless:
            chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
        service = Service(ChromeDriverManager().install())
        if disable_resource:
            chrome_options.add_argument("--blink-settings=imagesEnabled=false")
            prefs = {
                "profile.managed_default_content_settings.images": 2,  # Disable images
                "profile.managed_default_content_settings.stylesheets": 2  # Disable CSS
            }
            chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def get_url(self, url):
        if self.driver is None:
            raise Exception("Driver not initialized. Call setup_driver() first.")
        self.driver.get(url)

    def wait(self, seconds):
        time.sleep(seconds)

    def filter_script(self, page_source):
        self.soup = BeautifulSoup(page_source, "html.parser")
        for script in self.soup(["script", "style", "link", "meta", "iframe"]):
            script.decompose()

    def close(self):
        if self.driver:
            self.driver.quit()
