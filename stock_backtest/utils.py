import os
from stock_backtest.setting import REPORT_DIR
from stock_backtest.setting import PICTURE_DIR

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def create_dir():
        os.makedirs(REPORT_DIR, exist_ok=True)
        os.makedirs(PICTURE_DIR, exist_ok=True)

    @staticmethod
    def average_price(df):
        df['DAY_MEAN5'] = df['CLOSING_PRICE'].rolling(5).mean()
        df['DAY_MEAN20'] = df['CLOSING_PRICE'].rolling(20).mean()
        df['DAY_MEAN60'] = df['CLOSING_PRICE'].rolling(60).mean()
        df['DAY_MEAN120'] = df['CLOSING_PRICE'].rolling(120).mean()
        df['DAY_MEAN240'] = df['CLOSING_PRICE'].rolling(240).mean()
        df['RISE'] = (((df['CLOSING_PRICE'].shift(1) / df['CLOSING_PRICE']) - 1) * -100).round(4)
        df.loc[(df['RISE'] > 9.5) & (df['RISE'] < 11), 'LIMIT_UP'] = 1
        return df




