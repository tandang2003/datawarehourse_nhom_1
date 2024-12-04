import re
def find_element_by_regex( text, regex_pattern):
    # 14.1 Biến đổi dấu (\\ -> \)
    # 14.2 Tạo regex xpath từ regex pattern
    id_pattern = fr"{regex_pattern}".replace("\\\\", "\\")
    # 14.3 Trích xuất text từ xpath
    # 14.4 Áp dụng regex trong text
    match = re.search(id_pattern, text)
    if match:
        return match.group(1)
    return None

if __name__ == '__main__':
    html = """
    <div class="date"><span class="sc-1vo1n72-7 fGnMSX"></span>Ngày đăng: <!-- -->Hôm nay<!-- --> - Mã tin: <!-- -->69546466</div>
    """
    print(find_element_by_regex("Ngày đăng: Hôm nay - Mã tin: 68936795", "Mã tin:\\s*(\\d+)"))