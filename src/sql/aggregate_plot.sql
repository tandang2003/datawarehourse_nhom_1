-- Sử dụng cơ sở dữ liệu cần thiết
USE <tên_database>;

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
