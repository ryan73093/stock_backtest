import pymysql
import pandas as pd
from .step import Step
from .step import StepException
from stock_backtest.setting import SQL_HOST
from stock_backtest.setting import SQL_PORT
from stock_backtest.setting import SQL_USER
from stock_backtest.setting import SQL_PASSWORD
from stock_backtest.setting import SQL_DB
from stock_backtest.setting import SQL_TABLE


class ReadData(Step):
    def process(self, data, inputs, utils):
        conn = pymysql.connect(host=SQL_HOST,
                               port=SQL_PORT,
                               user=SQL_USER,
                               passwd=SQL_PASSWORD,
                               db=SQL_DB)

        df = pd.read_sql(
            f"SELECT * FROM {SQL_TABLE} "
            f"WHERE DATE BETWEEN '{inputs['START_DATE']}' and '{inputs['END_DATE']}' "
            f"AND SECURITY_CODE = {inputs['STOCK_CODE']}",
            con=conn)

        data = df
        return data
