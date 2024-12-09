import json
import logging
import os.path
import re
from datetime import datetime

from selenium.common import WebDriverException, NoSuchElementException

from src.service.AppException import STATUS, AppException
from src.service.extract_service.crawler.base_crawler import BaseCrawler
from src.service.notification_service.email import EmailTemplate, LABEL
from src.util.file_util import write_json_to_csv
from src.util.validation_util import check_url_valid


class PagingBase(BaseCrawler):

    def __init__(self,
                 limit_page,
                 file_format,
                 extension,
                 prefix,
                 data_dir_path,
                 error_dir_path,
                 purpose,
                 base_url,
                 source_page,
                 paging_pattern,
                 scenario,
                 navigate_scenario):
        super().__init__()
        self._limit_page = limit_page
        self._file_format = file_format
        self._extension = extension
        self._prefix = prefix
        self._data_dir_path = data_dir_path
        self._error_dir_path = error_dir_path
        self._purpose = purpose
        self._base_url = base_url
        self._source_page = source_page
        self._paging_pattern = paging_pattern
        self._scenario = json.loads(scenario)
        self._navigate_scenario = json.loads(navigate_scenario)
        # Chứa danh sách url item
        self._list_url = []
        # Chứa danh sách item đã cào được
        self._list_item = []

    # 7
    def handle(self) -> dict:
        # 7.1 Thực hiện tạo cấu hình crawler(selenium) bằng hàm setup_driver (8)
        super().setup_driver(headless=True)
        try:
            for (page) in range(1, 1 + self._limit_page):
                # 7.2. Thực hiện gọi hàm crawl_page (12) để lấy danh sách các url item trong trang
                list_url = self.crawl_page(page)
                # 7.3. Lấy 1 url item từ trong danh sách các item có trong trang
                for (url) in list_url:
                    # 7.4 Kiểm tra url có hợp lệ không
                    if not check_url_valid(url):
                        # 7.4.1 Không hợp lệ
                        break
                    # 7.4.2 Hợp lệ
                    # 7.5.thực hiện gọi hàm crawl_item để lấy các thông tin của item
                    item_crawled = self.crawl_item(url, self._scenario)
                    print(item_crawled)
                    # 7.6.Thêm các thông tin lấy được vào danh sách
                    self._list_item.append(item_crawled)
            logging.info(self._list_item)
            # 7.7 gọi hàm handle_success() đễ xử lý thành công
            return self.handle_success()
        except AppException | WebDriverException as e:
            # 7.8 Gọi hàm handle_exception() để xử lý lỗi
            return self.handle_exception(e)

    # 13
    def crawl_item(self, url, scenario):
        try:
            # 13.1 gọi request đến url chi tiết bất động sản
            self.get_url(url)

            logging.info(f"Visiting item: {url}")

            self.wait(10)
            current_url = self.driver.current_url

            # 13.2
            if current_url != url:
                # 13.2.1 no -> trang bị chuyển hướng
                return None
            # 13.2.2 hợp lệ
            driver = self.driver.page_source

            # Xóa các thẻ không cần thiết
            self.clean_html(driver)
            result = {}

            # 13.4 Loop qua các thuộc tính trong scenario
            for field_name, properties in scenario.items():
                # 13.5 gọi hàm find_element_by_config (9)
                result[field_name] = self.find_element_by_config(properties)
            # 13.6 Trả về dữ liệu đã trích xuất
            return result
        except WebDriverException as e:
            return None

    # 12
    def crawl_page(self, page):
        # 12.1 tạo url để navigate đến trang danh sách bất động sản
        url_page = f"{self._base_url}/{self._source_page}{self._paging_pattern}{page}"
        logging.info(f"Visiting page: {url_page}")

        # 12.2 Lấy HTML từ url
        self.get_url(url_page)
        self.wait(5)
        driver = self.driver.page_source

        # 12.3 Lọc các tag không sử dụng
        self.clean_html(driver)

        # 12.4 Lấy danh sách các url đến trang chi tiết
        estate_list = self.soup.select(self._navigate_scenario["list"])

        # 12.5 Kiểm tra list_url != None
        if len(estate_list) == 0:
            # 12.6 Ném ra ngoại lệ AppException => Crawl page không thành công
            raise AppException(STATUS.FILE_ERROR, "No data found")

        # 12.6 Tạo result = [] chứa các url đến trang chi tiết
        result = []

        # 12.7 Lấy ra từng url trong list_url
        for (estate) in estate_list:
            link = estate.select_one(self._navigate_scenario["item"]).get("href")
            # 12.8 kiểm tra url hợp lệ
            if link.startswith("https://"):
                # 12.8.1 Thêm list_url
                continue
            else:
                # 12.8.2 Thêm list_url
                result.append(f"{self._base_url}{str(link)}")
        return result

    def before_run(self):
        pass

    # 10
    def handle_success(self):
        data = self._list_item
        # 10.1 lấy ra thời gian hiện tại
        current_date = datetime.now().strftime(self._file_format)
        # 10.2 tạo tên file
        filename = f"{self._prefix}{current_date}.{self._extension}"
        # 10.3  Tạo đường dẫn đến file lưu dữ liệu, từ đường dẫn thư mục và tên file được tạo
        path = os.path.join(self._data_dir_path, filename)
        # 10.4 lưu dữ liệu vào file sử dụng hàm write_json_to_csv
        write_json_to_csv(path, data)
        logging.info(f"Data has been saved to {path}")

        # 10.5 Gửi email thông báo
        email_template = EmailTemplate(subject="Sent data to warehouse",
                                       status=STATUS.STAGING_PENDING.name,
                                       code=STATUS.STAGING_PENDING.value,
                                       message="Success",
                                       file_log=None,
                                       label=LABEL.INFO)
        email_template.sent_mail()

        # 10.6 trả về đường dẫn đến file, số lượng dòng thu thập được,
        # trạng thái "STAGING_PENDING" và đường dẫn file lỗi là None
        return {
            'file': path,
            'count_row': len(data),
            'status': 'STAGING_PENDING',
            'error_file_name': None
        }

    # 11 Xử lý ngoại lệ
    def handle_exception(self, exception: AppException):
        # 11.1 Tạo file name error
        filename = f"{self._prefix}{self._file_format}.log"
        path = os.path.join(self._error_dir_path, filename)
        # 11.2 cài đặt file name error vào exception
        exception.file_error = filename
        # 11.3 gọi hàm handler_exception trong exception (15)
        exception.handle_exception()
        # 11.4 Trả về giá trị gồm file, error file name, count row, status
        return {
            'file': None,
            'error_file_name': path,
            'count_row': 0,
            'status': 'STAGING_ERROR'
        }

    def find_element_by_config(self, field_properties):
        # print(field_properties)
        # 9.1 Khởi tạo các biến, trích xuất config field vào các biến
        method = field_properties.get("method", None)
        selector = field_properties.get("selector", None)
        attribute = field_properties.get("attribute", None)
        quantity = field_properties.get("quantity", 1)
        regex = field_properties.get("regex", None)
        xpath = self.find_elements_with_xpath(selector)

        try:
            # 9.2 regex != None
            if regex:
                # 9.2.1 gọi hàm find_element_by_regex (14)
                return self.find_element_by_regex(xpath, regex)
            # 9.3 quantity != None
            if quantity is None:
                # 9.3.1 trả về danh sách json ảnh
                return list(map(lambda img: img.get(attribute), xpath)) if xpath else None
            quantity -= 1
            # 9.4 method == time
            if method == "time":
                # 9.4.1 trả về thời gian hiện tại
                return datetime.now().strftime("%d/%m/%Y")
                # 9.5 method = url
            if method == "url":
                # 9.5.1 trả về url hiện tại của trang
                return self.driver.current_url
            # 9.6 method = description
            if method == "description":
                # 9.6.1 trả về text content
                return ''.join(xpath[quantity].itertext()).strip() if xpath else None
            # 9.7 method = get_attribute
            if method == "get_attribute":
                # 9.7.1 trích xuất attribute từ thẻ
                return xpath[quantity].get(attribute) if xpath else None
            # 9.8 method = text
            if method == "text":
                # 9.8.1 lấy ra text của thẻ
                return xpath[quantity].text if xpath else None
            # 9.8 trả về None
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def find_elements_with_xpath(self, xpath):
        try:
            elements = self.etree.xpath(xpath)

            if not elements:
                print("No elements found with the specified XPath.")
            return elements

        except NoSuchElementException:
            print("Element not found using the provided XPath.")
            return []

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    def find_element_by_regex(self, xpath, regex_pattern):
        # 14.1 Biến đổi dấu (\\ -> \)
        # 14.2 Tạo regex xpath từ regex pattern
        id_pattern = fr"{regex_pattern}".replace("\\\\", "\\")
        # 14.3 Trích xuất text từ xpath
        text = ''.join(xpath[0].itertext())
        # 14.4 Áp dụng regex trong text
        match = re.search(id_pattern, text)
        if match:
            return match.group(1)
        return None

# if __name__ == '__main__':
#     from lxml import html
#
#     # The provided HTML
#     html_content = """
#    <div class="sc-6orc5o-15 jiDXp"><h1>Bán nhà 100m2 Nguyễn Trãi, Q.1 chỉ 23,12 tỷ</h1><div class="sc-6orc5o-16 jGIyZP"><div class="price">23,12 tỷ</div></div><div class="address"><span class="sc-1vo1n72-6 bZuuMO"></span>212/12, Đường Nguyễn Trãi, Phường Nguyễn Cư Trinh, Quận 1, TP.HCM</div><div class="date"><span class="sc-1vo1n72-7 fGnMSX"></span>Ngày đăng: <!-- -->Hôm nay<!-- --> - Mã tin: <!-- -->6125271225</div></div>
#     """
#
#     # Parse the HTML string
#     tree = html.fromstring(html_content)
#
#     # Corrected XPath to select the div with class "date"
#     xpath = tree.xpath("//*[contains(@class, 'sc-6orc5o-15 jiDXp')]//*[@class='date']")
#
#     # Extract and print the text content
#     if xpath:
#         print(xpath[0].text_content().strip())
#     else:
#         print("No matching element found.")
