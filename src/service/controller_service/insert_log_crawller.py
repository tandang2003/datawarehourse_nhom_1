from src.config.procedure import insert_new_log_crawler
from src.service.controller_service.database_controller import Controller


class InsertLogCrawller(Controller):
    def __init__(self):
        super().__init__()

    def insert_log_crawller(self):
        return self.call_controller_procedure(insert_new_log_crawler,())