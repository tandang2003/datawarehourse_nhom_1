use estate_controller;
DROP PROCEDURE IF EXISTS get_log_datamart;
CREATE PROCEDURE get_log_datamart()
BEGIN
#     1.1 tạo biến _id và _config_id để lưu lại log id và config id của log đó
    DECLARE _id INT DEFAULT 0;
DECLARE _config_id INT DEFAULT 0;
#     1.2 thực hiện kiểm tra trong log có tồn tại ít nhất 1 dòng là DATAMART_PROCESSING
IF !EXISTS(SELECT 'DATAMART_PROCESSING'
               FROM logs
               WHERE status = 'DATAMART_PROCESSING'
                 AND is_delete = 0
               LIMIT 1) THEN
SELECT logs.id, logs.config_id
#         1.4.1 không thay đổi giá trị 2 biến
#        1.4.2 thực hiện việc gán giá trị log.id và log.config_id vào biến _id, _config_id
INTO _id, _config_id
#         1.3 thực hiện join bảng logs và bảng config
FROM logs
         join configs on logs.config_id = configs.id
#         1.4 tìm kiếm 1 dòng log có status là DATAMART_PENDING hay DATAMART_ERROR chưa bị xóa của ngày hôm đó và của thông tin còn hoạt động
WHERE (logs.status = 'DATAMART_PENDING' OR logs.status = 'DATAMART_ERROR')
  AND is_delete = 0
  AND DATE(logs.create_at) = CURRENT_DATE
  And configs.active = 1
#     GROUP BY logs.id, logs.config_id
ORDER BY
    CASE
             WHEN logs.status = 'DATAMART_PENDING' THEN 1
             WHEN logs.status = 'DATAMART_ERROR' THEN 2
    END,
         logs.create_at ASC
LIMIT 1;
#         1.5 Kiểm tra nếu config_id lấy được khác không(tức tìm được dòng có trạng thái hợp lệ)
IF _config_id != 0 THEN
#             1.6 thiết lập trạng thái bị xóa cho dòng log đó
UPDATE logs
SET logs.is_delete = 1
WHERE logs.id = _id;
#               AND (logs.status = 'FILE_PENDING' OR logs.status = 'DATAMART_ERROR')
#               AND DATE(logs.create_at) = CURRENT_DATE;
# 1.7 thêm 1 dòng log mới có config_id, thời gian bắt đầu và thời giang tạo ngay lúc thêm và có trạng thái "DATAMART_PROCESSING"
INSERT INTO logs (config_id, time_start, time_end, file_name, error_file_name, count_row, status,
                  create_at)
VALUES (_config_id, NOW(), NULL, '', ' ', 0, 'DATAMART_PROCESSING', NOW());
END IF;
#         1.8 Trả về các thông tin cần thiết cho việc load của _config_id lấy được
SELECT configs.id,
       configs.email,
       configs.error_dir_path,
       configs.file_format,
       configs.prefix
FROM resources
         JOIN configs ON resources.id = configs.resource_id
         JOIN logs ON logs.config_id = configs.id

WHERE configs.id = _config_id
  AND logs.id = _id
  AND active = 1;
END IF;
END;
DeLIMITER ;
call get_log_staging()