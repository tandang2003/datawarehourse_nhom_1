DROP USER 'estate_root'@'%';
CREATE USER 'estate_root'@'%' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON *.* TO 'estate_root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

SELECT @@global.time_zone, @@session.time_zone;