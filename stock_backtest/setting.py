import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
SQL_HOST = os.getenv('SQL_HOST')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
SQL_PORT = 3306
SQL_DB = 'stock'


REPORT_DIR = 'reports'