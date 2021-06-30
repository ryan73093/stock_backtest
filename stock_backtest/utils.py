import os
import math
import matplotlib.pyplot as plt
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
        df['LIMIT_UP'] = 0
        df.loc[(df['RISE'] > 9.5) & (df['RISE'] < 11), 'LIMIT_UP'] = 1
        df['YEAR'] = df['DATE'].apply(lambda x: x.split('-')[0])
        df['MONTH'] = df['DATE'].apply(lambda x: x.split('-')[1])
        return df

    @staticmethod
    def plt_figure_interval(df):
        plt.ticklabel_format(axis="y", style='plain')
        plt.grid(b=True, which='major', color='gray')
        plt.plot(df['DATE'], df['CLOSING_PRICE'])
        lst_xsticks = []
        lst_month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        lst_month_odd = ['01', '03', '05', '07', '09', '11']
        # interval
        for i in df['YEAR'].drop_duplicates():
            for k in lst_month:
                try:
                    df_tmp_interval = df[(df['YEAR'] == i) & (df['MONTH'] == k)]
                    lst_xsticks.append(df_tmp_interval.iloc[0]['DATE'])
                    lst_xsticks.append(df_tmp_interval.iloc[math.ceil(len(df_tmp_interval) / 2)]['DATE'])
                except IndexError:
                    continue
            for j in lst_month_odd:
                try:
                    df_tmp_interval = df[(df['YEAR'] == i) & (df['MONTH'] == j)]
                    plt.axvspan(xmin=df_tmp_interval.iloc[0]['DATE'],
                                xmax=df_tmp_interval.iloc[-1]['DATE'],
                                facecolor='grey', alpha=0.3)
                except IndexError:
                    continue
        plt.xticks(lst_xsticks, rotation=80)

