import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

# Data config
# Get the root directory dynamically

ROOT_DIR = Path(__file__).parent.parent.parent
FOLDER_DATA = os.path.join(ROOT_DIR, "data")

PATH_ENV = os.path.join(ROOT_DIR, ".env")

load_dotenv(dotenv_path=PATH_ENV)

config = dotenv_values(PATH_ENV)

SOURCE_A_BASE = os.getenv("SOURCE_A_BASE")
SOURCE_A_1 = os.getenv("SOURCE_A_1")
SOURCE_A_2 = os.getenv("SOURCE_A_2")
SOURCE_B_BASE = os.getenv("SOURCE_B_BASE")
SOURCE_B_1 = os.getenv("SOURCE_B_1")
SOURCE_B_2 = os.getenv("SOURCE_B_2")
SOURCE_B_3 = os.getenv("SOURCE_B_3")
LIMIT_ITEM = int(os.getenv("LIMIT_ITEM"))
LIMIT_PAGE = int(os.getenv("LIMIT_PAGE"))

CONTROLLER_DB_NAME = os.getenv("CONTROLLER_DB_NAME")
CONTROLLER_DB_HOST = os.getenv("CONTROLLER_DB_HOST")
CONTROLLER_DB_PORT = int(os.getenv("CONTROLLER_DB_PORT"))
CONTROLLER_DB_USER = os.getenv("CONTROLLER_DB_USER")
CONTROLLER_DB_PASS = os.getenv("CONTROLLER_DB_PASS")
CONTROLLER_DB_POOL_SIZE = int(os.getenv("CONTROLLER_DB_POOL_SIZE"))
CONTROLLER_DB_POOL_NAME = os.getenv("CONTROLLER_DB_POOL_NAME")
