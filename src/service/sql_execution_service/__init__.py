import mysql.connector
from src.config.database import get_db_connection

class SqlExecutionService:
    def __init__(self):
        self.connection = get_db_connection()  # Hàm này lấy connection từ file config
        self.cursor = self.connection.cursor()

    def execute_sql_from_file(self, sql_file_path):
        with open(sql_file_path, 'r') as sql_file:
            sql_queries = sql_file.read()
        self.cursor.execute(sql_queries)
        self.connection.commit()

    def execute_aggregate_address_procedure(self):
        self.execute_sql_from_file('src/sql/aggregate_address.sql')

    def execute_aggregate_plot_procedure(self):
        self.execute_sql_from_file('src/sql/aggregate_plot.sql')

    def execute_rename_tables_procedure(self):
        self.execute_sql_from_file('src/sql/rename_tables.sql')
