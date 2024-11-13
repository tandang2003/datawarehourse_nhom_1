import json

config_crawler_source_A_1 = json.loads(""" 
{
  "src": {"method": "url"},
  "subject": {
    "method": "text",
    "quantity": 1,
    "selector": "//*[contains(@class, 'pr-title')]"
  },
  "area": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 'js__pr-short-info-item')]/*[text()='Diện tích']/following-sibling::*[1]"
  },
  "address": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 'js__pr-address')]"
  },
  "price": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 'js__pr-short-info-item')]/*[text()='Mức giá']/following-sibling::*[1]"
  },
  "description": {
    "method"  : "description"                                ,
    "selector": "//*[contains(@class, 're__detail-content')]"
  },
  "images": {
    "quantity" : null                                       ,
    "method"   : "get_attribute"                            ,
    "attribute": "src"                                      ,
    "selector" : "//*[contains(@class, 'slick-track')]//img"
  },
  "natural_id": {
    "quantity": 1,
    "attribute": "prid",
    "method": "get_attribute",
    "selector": "//*[@id='product-detail-web']"
  },
  "orientation": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 're__pr-specs-content-item')]/*[text()='Hướng nhà']/following-sibling::*[1]"
  },
  "bedroom": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 're__pr-specs-content-item')]/*[text()='Số phòng ngủ']/following-sibling::*[1]"
  },
  "bathroom": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 're__pr-specs-content-item')]/*[text()='Số toilet']/following-sibling::*[1]"
  },
  "legal": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 're__pr-specs-content-item')]/*[text()='Pháp lý']/following-sibling::*[1]"
  },
  "email": {
    "quantity": 1,
    "method": "get_attribute",
    "selector": "//*[@id='email']",
    "attribute": "data-email"
  },
  "full_name": {
    "quantity": 1,
    "attribute": "title",
    "method": "get_attribute",
    "selector": "(//*[contains(@class, 'js_contact-name')])[1]"
  },
  "avatar": {
    "quantity": 1,
    "attribute": "src",
    "method": "get_attribute",
    "selector": "//*[contains(@class, 'js__agent-contact-avatar')]"
  },
  "start_date": {
    "method": "text",
    "quantity": 1,
    "selector": "//*[contains(@class, 'js__pr-config-item')]/*[text()='Ngày đăng']/following-sibling::*[1]"
  },
  "end_date": {
    "method": "text",
    "quantity": 1,
    "selector": "//*[contains(@class, 'js__pr-config-item')]/*[text()='Ngày hết hạn']/following-sibling::*[1]"
  },
  "create_at": {"method": "time"}
}
""")

config_crawler_source_B = json.loads("""{
  "src": {"method": "url"},
  "subject": {
    "method": "text",
    "quantity": 1,
    "selector": "//*[contains(@class, 'sc-6orc5o-15 jiDXp')]/h1"
  },
  "area": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[(text()='Diện tích đất')]/following-sibling::*[1]"
  },
  "address": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 'sc-6orc5o-15 jiDXp')]/div[contains(@class, 'address')]"
  },
  "price": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 'sc-6orc5o-15 jiDXp')]//*[@class='price']"
  },
  "description": {
    "method": "description",
    "selector": "//*[contains(@class, 'sc-6orc5o-18 gdAVnx')]"
  },
  "images": {
    "quantity": null,
    "method": "get_attribute",
    "attribute": "src",
    "selector": "//*[contains(@class, 'sc-6orc5o-3 ljaVcC')]//img"
  },
  "natural_id": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 'sc-6orc5o-15 jiDXp')]//*[@class='date']"
  },
  "floors": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[(text()='Tổng số tầng')]/following-sibling::*[1]"
  },
  "orientation": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[(text()='Hướng cửa chính')]/following-sibling::*[1]"
  },
  "bedroom": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[(text()='Số phòng ngủ')]/following-sibling::*[1]"
  },
  "bathroom": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[(text()='Số phòng vệ sinh')]/following-sibling::*[1]"
  },
  "legal": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[(text()='Giấy tờ pháp lý')]/following-sibling::*[1]"
  },
  "full_name": {
    "quantity": 1,
    "method": "text",
    "selector": "//span[contains(@class, 'title')]"
  },
  "phone": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 'sc-lohvv8-15 fyGvhT')]"
  },
  "create_at": {"method": "time"}
}""")
