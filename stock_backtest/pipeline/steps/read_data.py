import pymysql
import pandas as pd
import matplotlib as plt
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
        try:
            if inputs['STOCK_CODE'] != '*':
                df = pd.DataFrame()
                for i in inputs['STOCK_CODE']:
                    df_ = pd.read_sql(
                        f"SELECT * FROM {SQL_TABLE} "
                        f"WHERE DATE BETWEEN '{inputs['START_DATE']}' and '{inputs['END_DATE']}' "
                        f"AND SECURITY_CODE = {i}",
                        con=conn)
                    df = pd.concat([df, df_], axis=0)

            else:
                df = pd.read_sql(
                    f"SELECT * FROM {SQL_TABLE} "
                    f"WHERE DATE BETWEEN '{inputs['START_DATE']}' and '{inputs['END_DATE']}'",
                    con=conn)

        except Exception as e:
            print(e)
            pass

        data = df
        return data
