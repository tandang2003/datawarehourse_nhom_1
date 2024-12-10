from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from src.config.setting import SERVER_HOST, SERVER_PORT
from src.service.controller_service.crawl_controller import CrawlController
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import uvicorn

from src.service.controller_service.transformation_controller import TransformationController
from src.service.transformation_service.transformation_service import Transformation

app = FastAPI()
scheduler = BackgroundScheduler()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
crawl_controller = CrawlController()
transformation_controller = TransformationController()


def crawl_data():
    # 6. Crawl_Data:
    # 6.1. sử hàm getConfig của crawlController đã tạo trước đó
    crawl_controller.get_config()


def insert_new_log_crawler_daily():
    crawl_controller.call_controller_procedure('insert_new_log_crawler_daily', ())

# HÀm này dùng để load data từ file vào staging
# Hiện thực code ở thư mục src/service/load_data_service
def load_data_from_file_to_staging():
    # Lấy cấu từ controller
    # crawl_controller.call_staging_procedure('load_data_from_file_to_staging', ())
    pass

# Hàm này dùng để transform data và load data vào warehouse
# Hiện thực code ở thư mục src/service/transform_service
def transforms_data():
    # Lấy cấu từ controller
    transformation_controller.get_config()
    pass

# Hàm này dùng để load data từ staging vào warehouse
# Hiện thực code ở thư mục src/service/load_data_warehourse_service
def load_data_from_staging_to_warehouse():
    # Lấy cấu từ controller
    # crawl_controller.call_staging_procedure('load_data_from_staging_to_warehouse', ())
    pass

# Hàm này dùng để load data từ warehouse vào data mart
# Hiện thực code ở thư mục src/service/aggerate_service
def load_data_from_warehouse_to_data_mart():
    # Lấy cấu từ controller
    # crawl_controller.call_staging_procedure('load_data_from_warehouse_to_data_mart', ())
    pass


@app.on_event("startup")
def startup_event():
    scheduler.start()
    scheduler.add_job(insert_new_log_crawler_daily,
                      CronTrigger(hour=8, minute=0),
                      id='insert_new_log_crawler_daily', replace_existing=True)
    scheduler.add_job(crawl_data, IntervalTrigger(minutes=2),
                      id='crawl_data', replace_existing=True)
    scheduler.add_job(load_data_from_file_to_staging, IntervalTrigger(minutes=20),
                      id='load_data_from_file_to_staging', replace_existing=True)
    scheduler.add_job(transforms_data, IntervalTrigger(minutes=20),
                      id='transforms_data', replace_existing=True)
    scheduler.add_job(load_data_from_warehouse_to_data_mart, IntervalTrigger(minutes=20),
                      id='load_data_from_warehouse_to_data_mart', replace_existing=True)


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()


if __name__ == '__main__':
    uvicorn.run(
        "src.main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=True
    )