from src.service.sql_execution_service import SqlExecutionService

class Controller:
    def __init__(self):
        self.sql_service = SqlExecutionService()

    def process_data(self):
        # Call procedure to aggregate address
        self.sql_service.execute_aggregate_address_procedure()

        # Call procedure to aggregate plot
        self.sql_service.execute_aggregate_plot_procedure()

        # Call procedure to rename tables
        self.sql_service.execute_rename_tables_procedure()
