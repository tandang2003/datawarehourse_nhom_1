from src.config.database import MySQLCRUD
from src.config.setting import CONTROLLER_DB_PORT, CONTROLLER_DB_HOST, CONTROLLER_DB_NAME, CONTROLLER_DB_USER, \
    CONTROLLER_DB_PASS, CONTROLLER_DB_POOL_NAME, CONTROLLER_DB_POOL_SIZE


class Controller:
    __connector: MySQLCRUD = None

    def __init__(self):
        self.__connector = MySQLCRUD(
            host=CONTROLLER_DB_HOST,
            port=CONTROLLER_DB_PORT,
            database=CONTROLLER_DB_NAME,
            user=CONTROLLER_DB_USER,
            password=CONTROLLER_DB_PASS,
            pool_name=CONTROLLER_DB_POOL_NAME,
            pool_size=CONTROLLER_DB_POOL_SIZE
        )

        print(f"Connection pool created with pool size: {CONTROLLER_DB_POOL_SIZE}")

    def call_controller_procedure(self, procedure_name, args):
        connection = self.__connector.get_controller_connection()
        result = self.__connector.call_procedure(procedure_name, connection, args)
        # connection.close()
        return result

    def call_staging_procedure(self, procedure_name, args):
        connection = self.__connector.get_staging_connection()
        result = self.__connector.call_procedure(procedure_name, connection, args)
        # connection.close()
        return result

    def call_warehouse_procedure(self, procedure_name, args, header):
        connection = self.__connector.get_warehouse_connection()
        result = self.__connector.call_procedure(procedure_name, connection, args)
        # connection.close()
        return result
