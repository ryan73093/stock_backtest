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

from stock_backtest.utils import Utils
from stock_backtest.pipeline.pipeline import Pipeline
from stock_backtest.pipeline.steps.preflight import Preflight
from stock_backtest.pipeline.steps.read_data import ReadData
from stock_backtest.pipeline.steps.data_integrate import DataIntegrate
from stock_backtest.pipeline.steps.analysis import Analysis

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_row', None)
help(pd.set_option)
inputs = {
    'METHOD': 'breakpoint',
    'START_DATE': '2020-01-01',
    'END_DATE': '2021-04-30',
    'EXPORT_METHOD': 'jpg',
    'STOCK_CODE': '2603'
}


def main():
    steps = [
        Preflight(),
        ReadData(),
        DataIntegrate(),
        Analysis(),
        # ExportReport(),
        # PostFlight()

    ]
    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
