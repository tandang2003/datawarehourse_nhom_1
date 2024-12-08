-- Sử dụng cơ sở dữ liệu cần thiết
USE <tên_database>;

-- 1. Sao chép dữ liệu từ agrregate_address vào agrregate_address_temp
INSERT INTO agrregate_address_temp (districts_sk, districts_name, province_sk, province_name, average_district)
SELECT districts_sk, districts_name, province_sk, province_name, average_district
FROM agrregate_address;

-- 2. Đổi tên bảng chính thành bảng tạm
RENAME TABLE agrregate_address TO agrregate_address_old;

-- 3. Đổi tên bảng tạm thành bảng chính
RENAME TABLE agrregate_address_temp TO agrregate_address;

-- 4. Đổi tên bảng cũ thành bảng tạm
RENAME TABLE agrregate_address_old TO agrregate_address_temp;
