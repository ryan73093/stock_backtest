import os
from stock_backtest.setting import REPORT_DIR


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def create_dir():
        os.makedirs(REPORT_DIR, exist_ok=True)
