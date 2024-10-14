from datetime import datetime
import re

from service.extract_service.src.config.setting import SOURCE_B_1, SOURCE_B_BASE, SOURCE_B_2, SOURCE_B_3
from service.extract_service.src.crawler.paging_base_crawler import PagingBase
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from bs4.element import ResultSet
from bs4.element import Tag


class SourceB1Crawler(PagingBase):
    _base_url = SOURCE_B_3
    _domain = SOURCE_B_BASE

    def crawl_page(self, page):
        url_page = f"{self._base_url}?page={page}"
        print(f"Visiting page: {url_page}")
        self.get_url(url_page)

        # Wait for 5 seconds
        self.wait(5)
        driver = self.driver.page_source
        self.filter_script(driver)

        estate_list = self.soup.select(".sc-q9qagu-4.iZrvBN")
        list_url = []
        for (estate) in estate_list:
            link = estate.select_one("a.title").get("href")
            list_url.append(f"{self._domain}{str(link)}")
        return list_url

    def crawl_item(self, url):
        try:
            self.get_url(url)
        except WebDriverException as e:
            return None
        print(f"Visiting item: {url}")

        self.wait(10)
        current_url = self.driver.current_url
        if current_url != url:
            return None

        # self._click_show_phone()
        driver = self.driver.page_source

        self.filter_script(driver)
        agent = self.__extract_user()

        create_and_id = self.soup.select_one(".sc-6orc5o-15.jiDXp div.date").get_text()
        title = self.soup.select_one(".sc-6orc5o-15.jiDXp h1").get_text(strip=True)
        address = self.soup.select_one(".sc-6orc5o-15.jiDXp div.address").get_text(strip=True)
        created_at = datetime.now().strftime("%H:%M %d:%m:%Y")
        natural_id = self._extract_post_id(create_and_id)
        description = self.soup.select_one("div.sc-6orc5o-18.gdAVnx").get_text(strip=True)

        result = {
            "Subject": title,
            "Address": address,
            "Description": description,
            "natural_id": natural_id,
            "created_at": created_at,
            "src": current_url,
            "agent": agent,
            "images": self.__extract_imgs()
        }
        print(result)

    def __extract_imgs(self):
        tag_img = self.soup.select(".sc-6orc5o-3.ljaVcC img")
        result = []
        for img in tag_img:
            result.append(img.get("data-src"))
        return result

    def base_url(self):
        return self._base_url

    def __extract_properties(self):
        properties = {}
        list_label_attribute: ResultSet = self.soup.select('ul.sc-6orc5o-24.jhtUTo li')

        for item in list_label_attribute:
            spans: ResultSet = item.select("span")
            properties[spans[0].get_text()] = spans[1].get_text()
        price = self.soup.select_one(".sc-6orc5o-15.jiDXp div.price").get_text(strip=True)
        properties["price"] = price

    def __extract_user(self):
        return {"phone": self.soup.select_one("span.sc-lohvv8-15.fyGvhT").get_text(strip=True),
                "avatar ": self.soup.select_one(".sc-lohvv8-2.ficBQz img").get("src"),
                "name": self.soup.select_one("span.title").get_text(strip=True)
                }

        # def _click_show_phone(self):
        #     self.driver.find_element(by=By.CLASS_NAME, value="show-phone").click()
        #     self.wait(3)
        #     self.driver.find_element(by=By.CLASS_NAME, value="sc-lohvv8-18 sc-lohvv8-19 kgVSjR iuojYw").click()
        #     self.wait(3)

    def _extract_created_at(self, text):
        created_at_pattern = r"Ngày đăng:\s*([^\-]+)"
        created_at_match = re.search(created_at_pattern, text)
        if created_at_match:
            return created_at_match.group(1).strip()
        return None

        # Function to extract the post ID
    def _extract_post_id(self, text):
        id_pattern = r"Mã tin:\s*(\d+)"
        id_match = re.search(id_pattern, text)
        if id_match:
            return id_match.group(1)
        return None

