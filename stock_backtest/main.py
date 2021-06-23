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

inputs = {
    'METHOD': 'breakpoint',
    'START_DATE': '2020-01-01',
    'END_DATE': '2020-02-01',
    'EXPORT_METHOD': 'jpg',
    'STOCK_CODE': ['2330', '2323']
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
