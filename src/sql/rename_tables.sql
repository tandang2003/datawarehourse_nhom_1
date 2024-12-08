-- Sử dụng cơ sở dữ liệu cần thiết
USE <tên_database>;

-- Đổi tên các bảng aggregate_address
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


-- Đổi tên các bảng aggregate_plot
-- 1. Sao chép dữ liệu từ agrregate_plot vào agrregate_plot_temp
INSERT INTO agrregate_plot_temp (area, price, count)
SELECT area, price, count
FROM agrregate_plot;

-- 2. Đổi tên bảng chính thành bảng tạm
RENAME TABLE agrregate_plot TO agrregate_plot_old;

-- 3. Đổi tên bảng tạm thành bảng chính
RENAME TABLE agrregate_plot_temp TO agrregate_plot;

-- 4. Đổi tên bảng cũ thành bảng tạm
RENAME TABLE agrregate_plot_old TO agrregate_plot_temp;
