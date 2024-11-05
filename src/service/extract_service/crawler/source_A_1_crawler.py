from datetime import datetime

from selenium.common import NoSuchElementException

from src.config.setting import SOURCE_A_1, SOURCE_A_BASE
from src.service.extract_service.crawler.config_crawler import config_crawler_source_A_1
from src.service.extract_service.crawler.paging_base_crawler import PagingBase
from src.util.file_util import write_json_to_csv


class SourceA1Crawler(PagingBase):
    _base_url = SOURCE_A_1
    _domain = SOURCE_A_BASE

    def crawl_page(self, page):
        url_page = f"{self._base_url}/p{page}"
        print(f"Visiting page: {url_page}")
        self.get_url(url_page)

        # Wait for 5 seconds
        self.wait(5)
        driver = self.driver.page_source
        self.clean_html(driver)

        estate_list = self.soup.select(".js__card")
        list_url = []
        for (estate) in estate_list:
            link = estate.select_one(".js__product-link-for-product-id").get("href")
            if link.startswith("https://"):
                continue
            else:
                list_url.append(f"{self._domain}{str(link)}")
        return list_url

    def crawl_item(self, url):
        super().crawl_item(url)
        result = {}

        for field_name, properties in config_crawler_source_A_1.items():
            print(f"Field Name: {field_name}")  # Print the name of the field
            print(f"Properties: {properties}")  # Print the properties of the field
            result[field_name] = self.find_element_by_config(properties)

        return result

    def after_run(self):
        data = self._list_item
        current_date = datetime.now().strftime("%Y_%m_%d__%H_%M")
        print(f"data: {data}")
        filename = f"source_1_{current_date}.csv"
        write_json_to_csv(filename, data)
        print(f"Data has been saved to {filename}")

    def handle_error_item(self, error):
        super().handle_error_item(error)

    @property
    def base_url(self):
        return self._base_url

    def find_elements_with_xpath(self, xpath):
        try:
            # Attempt to find elements using the provided XPath
            elements = self.etree.xpath(xpath)

            if not elements:
                print("No elements found with the specified XPath.")

            return elements  # Return found elements (can be an empty list if none found)

        except NoSuchElementException:
            print("Element not found using the provided XPath.")
            return []  # Return an empty list on exception

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []  # Return an empty list on other exceptions

    def find_element_by_config(self, field_properties):
        print(field_properties)
        method = field_properties.get("method", None)
        selector = field_properties.get("selector", None)
        attribute = field_properties.get("attribute", None)
        quantity = field_properties.get("quantity", 0)
        xpath = self.find_elements_with_xpath(selector)

        if quantity is None:
            return list(map(lambda img: img.get(attribute), xpath)) if xpath else None
        quantity -= 1
        if method == "time":
            return datetime.now().strftime("%d/%m/%Y")
        if method == "url":
            return self.driver.current_url
        if method == "description":
            return ''.join(xpath[quantity].itertext()).strip() if xpath else None
        if method == "get_attribute":
            return xpath[quantity].get(attribute) if xpath else None
        if method == "text":
            return xpath[quantity].text.strip() if xpath else None
        return None
