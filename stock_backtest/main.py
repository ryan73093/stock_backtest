# %%
import pandas as pd
import numpy as np
import datetime
import time
import random
import pymysql
import matplotlib.pyplot as plt
import math
import os

# %%

host = os.getenv('sql_host')
port = 3306
user = os.getenv('sql_user')
passwd = os.getenv('sql_passwd')
db = 'stock'
conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
df_db = pd.read_sql('SELECT * FROM stock_everyday_new', con=conn)
df_db.head()
df = df_db.copy()

INPUT = {
    'METHOD': 'breakponit',
    'START_DATE': '2020-01-01',
    'END_DATE': '2020-12-01',
    'EXPORT_METHOD': 'jpg',
    'STOCK_CODE': '2330'

}


def main():
    steps = [
        Preflight(),
        ReadData(),
        CleanData(),
        AnalysisMethodSelect(),
        CalculateRevenue(),
        ExportReport(),
        PostFlight()

    ]
