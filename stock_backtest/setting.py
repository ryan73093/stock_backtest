import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
SQL_HOST = os.getenv('SQL_HOST')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

REPORT_DIR = 'reports'