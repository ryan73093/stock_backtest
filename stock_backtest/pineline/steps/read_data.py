import pymysql
import pandas as pd
from .step import Step
from stock_backtest.setting import SQL_HOST
from stock_backtest.setting import SQL_PORT
from stock_backtest.setting import SQL_USER
from stock_backtest.setting import SQL_PASSWORD
from stock_backtest.setting import SQL_DB


class ReadData(Step):
    def process(self, data, inputs, utils):
        conn = pymysql.connect(host=SQL_HOST,
                               port=SQL_PORT,
                               user=SQL_USER,
                               passwd=SQL_PASSWORD,
                               db=SQL_DB)

        return pd.read_sql('SELECT * FROM stock_everyday_new WHERE DATE > 2020-01-01',
                           con=conn)
