import mysql.connector
from mysql.connector import Error

from src.config.procedure import procedure_get_database_config
from src.config.setting import CONTROLLER_DB_HOST, CONTROLLER_DB_PORT, CONTROLLER_DB_NAME, CONTROLLER_DB_USER, \
    CONTROLLER_DB_PASS, CONTROLLER_DB_POOL_NAME, CONTROLLER_DB_POOL_SIZE


class MySQLCRUD:
    __controller_pool: mysql.connector.pooling.MySQLConnectionPool = None
    __staging_pool: mysql.connector.pooling.MySQLConnectionPool = None
    __warehouse_pool: mysql.connector.pooling.MySQLConnectionPool = None
    __data_mart_pool: mysql.connector.pooling.MySQLConnectionPool = None

    def __init__(self, host, port, user, password, database, pool_name, pool_size=5):
        try:
            self.__controller_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                pool_reset_session=True,  # Resets session on each connection reuse
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                autocommit=True,
                allow_local_infile=True
            )
            print(f"Connection pool created with pool size: {pool_size}")
        except Error as e:
            print(f"Error creating connection pool: {e}")

    def get_controller_connection(self):
        # 1.2 Kiểm tra trong quá trình lấy connection có bị lỗi hay không
        try:
            # 1.1 Lấy connection controller từ controller_pool
            # 1.2.1 Không có lỗi sảy ra
            connection = self.__controller_pool.get_connection()
            # 1.3.1 trả connection nhận được từ pool
            return connection
        except Error as e:
            #1.2.2 Có bị lỗi
            #1.3.2 gửi lỗi phát sinh ra hàm sử dụng
            raise Exception(f"Failed to get connection from pool: {e}")
            # return None

    def get_staging_connection(self) -> mysql.connector.connection.MySQLConnection:
        # 1.Kiểm tra staging connection pool có được thiết lập chưa
        if self.__staging_pool is None:
            # 1.1.thực hiện tạo connection pool của staging (bằng hàm __staging_establish_pool)
            self.__staging_establish_pool()
        #     1.2Lấy connection từ staging_pool
        # 2.Kiểm tra trong quá trình lấy connection có lỗi sảy ra không
        try:
            connection = self.__staging_pool.get_connection()
            # 2.1 trả connection nhận được từ pool
            return connection
        except Error as e:
            # 2.2.gửi lỗi phát sinh ra hàm sử dụng
            raise Exception(f"Failed to get connection from pool: {e}")

    def __staging_establish_pool(self):
        # 1.Lấy connection của controller thông qua hàm get_controller_conection
        controller_connection: mysql.connector.connection.MySQLConnection = self.__controller_pool.get_connection()
        cursor = controller_connection.cursor(dictionary=True)
        # 2.Gọi tới procedure get_database_config lấy các thông tin connection cần thiết
        cursor.callproc(procedure_get_database_config, ("staging",))
        for rows in cursor.stored_results():
            for row in rows.fetchall():
                # 3.Tạo connection tới warehouse database với các thông tin trả về từ procedure
                self.__staging_pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=CONTROLLER_DB_POOL_NAME,
                    pool_size=CONTROLLER_DB_POOL_SIZE,
                    pool_reset_session=True,  # Resets session on each connection reuse
                    host=row["host"],
                    port=row["port"],
                    user=row["username"],
                    password=row["password"],
                    database=row["name"],
                    autocommit=True,
                    allow_local_infile=True

                )
        print(f"Connection pool created with staging pool size: {CONTROLLER_DB_POOL_SIZE}")
        cursor.close()

    def get_warehouse_connection(self):
        # 1.Kiểm tra warehouse connection pool có được thiết lập chưa
        if self.__warehouse_pool is None:
            # 1.1.thực hiện tạo connection pool của warehouse (bằng hàm __warehouse_establish_pool)
            self.__warehouse_establish_pool()
        #     1.2Lấy connection từ warehouse_pool
        # 2.Kiểm tra trong quá trình lấy connection có lỗi sảy ra không
        try:
            connection = self.__warehouse_pool.get_connection()
            # 2.1 trả  connection nhận được từ pool
            return connection
        except Error as e:
            # 2.2.gửi lỗi phát sinh ra hàm sử dụng
            raise Exception(f"Failed to get connection from pool: {e}")

    def __warehouse_establish_pool(self):
        # 1.Lấy connection của controller thông qua hàm get_controller_conection
        controller_connection: mysql.connector.connection.MySQLConnection = self.get_controller_connection();
        cursor = controller_connection.cursor(dictionary=True)
        # 2.Gọi tới procedure get_database_config lấy các thông tin connection cần thiết
        cursor.callproc("get_database_config", ("warehouse",))
        for result in cursor.stored_results():
            for row in result.fetchall():
                # 3.Tạo connection tới warehouse database với các thông tin trả về từ procedure
                self.__warehouse_pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=CONTROLLER_DB_POOL_NAME,
                    pool_size=CONTROLLER_DB_POOL_SIZE,
                    pool_reset_session=True,  # Resets session on each connection reuse
                    host=row["host"],
                    port=row["port"],
                    user=row["username"],
                    password=row["password"],
                    database=row["name"],
                    autocommit=True,
                    allow_local_infile=True
                )
                print(f"Connection pool created with warehouse pool size: {CONTROLLER_DB_POOL_SIZE}")
        cursor.close()

    def get_datamart_connection(self) -> mysql.connector.connection.MySQLConnection:
        # 1.Kiểm tra staging connection pool có được thiết lập chưa
        if self.__data_mart_pool is None:
            # 1.1.thực hiện tạo connection pool của staging (bằng hàm __staging_establish_pool)
            self.__data_mart_establish_pool()
        #     1.2Lấy connection từ staging_pool
        # 2.Kiểm tra trong quá trình lấy connection có lỗi sảy ra không
        try:
            connection = self.__data_mart_pool.get_connection()
            # 2.1 trả connection nhận được từ pool
            return connection
        except Error as e:
            return None
            # 2.2.gửi một email báo lỗi với email mặc định được lưu trên server
            # TODO send mail

    def call_procedure(self, procedure_name: str, connection: mysql.connector.connection.MySQLConnection, args=()):
        # 1 Kiển tra connection có được truyền vào hay không
        if connection is None:
            # 1.2 không được truyền
            return None
        # 1.1 Được truyền
        cursor = connection.cursor(dictionary=True)
        # 3. Kiểm tra trong quá trình gọi procedure có lỗi xảy ra không
        try:
            # 2 thực hiện gọi procedure với tên và tham số được nhận vào
            cursor.callproc(procedure_name, args)
            results = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    # 3.2 Lưu các kết quả nhận về vào 1 danh sách dictionary
                    results.append(row)
            print(f"Procedure '{procedure_name}' called successfully.")
            # 4 Kiểm tra trong dictionary trả về
            # dictionary bị rỗng
            # 4.1 trả về None
            # dictionary không rỗng
            #  4.2 Kiểm tra trong dictionary trả về
            # nếu dài hơn 1
            # 5.1 trả về dictionary
            # dictionary không rỗng
            # 5.2 trả về giá trị đầu tiên
            return len(results) > 1 and results or results[0] if results else None
        except Error as e:
            # 3.1 Gửi mail thông báo việc gọi procedure lỗi
            #  TODO send mail
            return None
        finally:
            cursor.close()
            connection.close()

    def execute_sql_file(self, file_path):
        """Execute SQL commands from a file."""
        connection = self.get_connection()
        if connection is None:
            return
        try:
            cursor = connection.cursor()
            with open(file_path, 'r') as file:
                sql_script = file.read()
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            connection.commit()
            print(f"SQL file '{file_path}' executed successfully.")
        except (Error, FileNotFoundError) as e:
            print(f"Failed to execute SQL file '{file_path}': {e}")
        finally:
            cursor.close()
            connection.close()

    def close_controller_pool(self):
        """Close the pool and all connections."""
        try:
            self.__controller_pool.close()
            print("Connection pool closed.")
        except Error as e:
            print(f"Error closing the connection pool: {e}")

    def __data_mart_establish_pool(self):
        # 1.Lấy connection của controller thông qua hàm get_controller_conection
        controller_connection: mysql.connector.connection.MySQLConnection = self.__controller_pool.get_connection()
        cursor = controller_connection.cursor(dictionary=True)
        # 2.Gọi tới procedure get_database_config lấy các thông tin connection cần thiết
        cursor.callproc(procedure_get_database_config, ("datamart",))
        for rows in cursor.stored_results():
            for row in rows.fetchall():
                # 3.Tạo connection tới warehouse database với các thông tin trả về từ procedure
                self.__data_mart_pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=CONTROLLER_DB_POOL_NAME,
                    pool_size=CONTROLLER_DB_POOL_SIZE,
                    pool_reset_session=True,  # Resets session on each connection reuse
                    host=row["host"],
                    port=row["port"],
                    user=row["username"],
                    password=row["password"],
                    database=row["name"],
                    autocommit=True,
                    allow_local_infile=True

                )
        print(f"Connection pool created with staging pool size: {CONTROLLER_DB_POOL_SIZE}")
        cursor.close()


if __name__ == '__main__':
    controller_connector = MySQLCRUD(
        host=CONTROLLER_DB_HOST,
        port=CONTROLLER_DB_PORT,
        database=CONTROLLER_DB_NAME,
        user=CONTROLLER_DB_USER,
        password=CONTROLLER_DB_PASS,
        pool_name=CONTROLLER_DB_POOL_NAME,
        pool_size=CONTROLLER_DB_POOL_SIZE
    )
    controller_connector.get_datamart_connection()
staging_connector = None
warehouse_connector = None
