import json

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
                database=database
            )
            print(f"Connection pool created with pool size: {pool_size}")
        except Error as e:
            print(f"Error creating connection pool: {e}")
            self.pool = None

    def get_controller_connection(self):
        """Get a connection from the pool."""
        try:
            connection = self.__controller_pool.get_connection()
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Failed to get connection from pool: {e}")
            return None

    def get_staging_connection(self) -> mysql.connector.connection.MySQLConnection:
        """Get a connection from the pool."""
        if self.__staging_pool is None:
            self.__staging_establish_pool()
        try:
            connection = self.__staging_pool.get_connection()
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Failed to get connection from pool: {e}")
            return None

    def __staging_establish_pool(self):
        controller_connection: mysql.connector.connection.MySQLConnection = self.__controller_pool.get_connection()
        cursor = controller_connection.cursor(dictionary=True)
        cursor.callproc(procedure_get_database_config, ("staging",))
        for result in cursor.stored_results():
            for row in result.fetchall():
                self.__staging_pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=CONTROLLER_DB_POOL_NAME,
                    pool_size=CONTROLLER_DB_POOL_SIZE,
                    pool_reset_session=True,  # Resets session on each connection reuse
                    host=row["host"],
                    port=row["port"],
                    user=row["username"],
                    password=row["password"],
                    database=row["name"]
                )
                print(f"Connection pool created with staging pool size: {CONTROLLER_DB_POOL_SIZE}")
        cursor.close()

    def get_warehouse_connection(self):
        """Get a connection from the pool."""
        if self.__warehouse_pool is None:
            self.__warehouse_establish_pool()
        try:
            connection = self.__warehouse_pool.get_connection()
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Failed to get connection from pool: {e}")
            return None

    def __warehouse_establish_pool(self):
        controller_connection: mysql.connector.connection.MySQLConnection = self.__controller_pool.get_connection()
        cursor = controller_connection.cursor(dictionary=True)
        cursor.callproc(procedure_get_database_config, ("warehouse",))
        for result in cursor.stored_results():
            for row in result.fetchall():
                self.__warehouse_pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=CONTROLLER_DB_POOL_NAME,
                    pool_size=CONTROLLER_DB_POOL_SIZE,
                    pool_reset_session=True,  # Resets session on each connection reuse
                    host=row["host"],
                    port=row["port"],
                    user=row["username"],
                    password=row["password"],
                    database=row["name"]
                )
                print(f"Connection pool created with warehouse pool size: {CONTROLLER_DB_POOL_SIZE}")
        cursor.close()

    def call_procedure(self, procedure_name: str, connection: mysql.connector.connection.MySQLConnection, args=()):
        """Call a stored procedure."""
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc(procedure_name, args)
            # Fetch the results if the procedure returns data
            results = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    results.append(row)
            print(f"Procedure '{procedure_name}' called successfully.")
            return len(results) > 1 and results or results[0] if results else None
        except Error as e:
            print(f"Failed to call procedure '{procedure_name}': {e}")
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
    controller_connector.get_staging_connection()
    controller_connector.get_warehouse_connection()
staging_connector = None
warehouse_connector = None
