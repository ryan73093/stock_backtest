import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
from .analysis_method import AnalysisMethod
from stock_backtest.setting import PICTURE_DIR

class BreakPoint(AnalysisMethod):
    def analysis_info(self, data, inputs, utils):
        print('break point analysis')
        pass
        return data

    def analysis(self, data, inputs, utils):
        # define break point
        lst_break = []
        data = data
        for i in range(len(data)):
            if data.iloc[i]['CLOSING_PRICE'] > data.iloc[:i]['CLOSING_PRICE'].max():
                lst_break.append(1)
            else:
                lst_break.append(0)
        data['BREAK'] = lst_break
        data['BREAK_PRICE'] = data['BREAK'] * data['CLOSING_PRICE']
        data['+10%'] = data['BREAK_PRICE'] * 1.1
        data['-3%'] = data['BREAK_PRICE'] * 0.97
        # define sold date and price
        lst_date = []
        lst_sold = []
        for k in range(len(data)):
            tmp_a = data.iloc[k]['BREAK_PRICE'] * 1.1
            tmp_b = data.iloc[k]['BREAK_PRICE'] * 0.97
            for i, j in zip(data.iloc[k:]['CLOSING_PRICE'], data.iloc[k:]['DATE']):
                if (i > tmp_a) | (i < tmp_b):
                    date = j
                    sold = i
                    break
                else:
                    date = 0
                    sold = 0
                    pass
            lst_date.append(date)
            lst_sold.append(sold)
        data['SOLD_DATE'] = lst_date
        data['SOLD_PRICE'] = lst_sold
        data['REVENUE'] = data['SOLD_PRICE'] - data['BREAK_PRICE']

        return data

    def revenue(self, data, inputs, utils):
        df = self.analysis(data, inputs, utils)
        df_ = df[(df['BREAK_PRICE'] != 0)
                 & (df['LIMIT_UP'] != 1)
                 & (df['SOLD_PRICE'] != 0)]
        df_['HOLD_TIME'] = pd.to_datetime(df_['SOLD_DATE']) - pd.to_datetime(df_['DATE'])
        # print(df_)
        dict_df = {
            'stock_code': df.iloc[0]['SECURITY_CODE'],
            'start_date': df.iloc[0]['DATE'],
            'end_date': df.iloc[-1]['DATE'],
            'final_price': df.iloc[-1]['CLOSING_PRICE'],
            'revenue': round(df_['REVENUE'].sum(), 2),
            'revenue(%)': round((df_['SOLD_PRICE'].sum()) / (df_['BREAK_PRICE'].sum())*100, 2),
            'amount in and out': round(df_['CLOSING_PRICE'].sum(), 2),
            'frequency in an out': len(df_),
            'hold_time_avg': df_['HOLD_TIME'].mean(),
            'hold_time_max': df_['HOLD_TIME'].max(),
            'hold_time_min': df_['HOLD_TIME'].min(),
        }
        df = pd.DataFrame(dict_df, index=[0])
        df = df.T.reset_index()
        df.columns = ['Item', 'Data']
        print(df)
        return df

    def plot_graph(self, data, inputs, utils):
        # line plot
        df = self.analysis(data, inputs, utils)
        plt.figure(figsize=(16, 10))
        plt_grid = plt.GridSpec(3, 5, wspace=0.2, hspace=0.1)

        
        # grid(1)
        plt.subplot(plt_grid[0:2, 0:3])  # all row, 0 column
        df_ = df[(df['BREAK_PRICE'] != 0)
                 & (df['LIMIT_UP'] != 1)
                 & (df['SOLD_PRICE'] != 0)]
        colors = ['b', 'darkorange', 'deepskyblue', 'darkorchid', 'saddlebrown', 'darkgreen', 'red', 'royalblue']
        labels = ['1days', '5days', '20days', '60days', '120days', '240days', 'breakpoint', 'revenue']
        plt.plot(df['DATE'], df['CLOSING_PRICE'], c=colors[0])
        utils.plt_figure_interval(df)
        plt.plot(df['DATE'], df['DAY_MEAN5'], c=colors[1])
        plt.plot(df['DATE'], df['DAY_MEAN20'], c=colors[2])
        plt.plot(df['DATE'], df['DAY_MEAN60'], c=colors[3])
        plt.plot(df['DATE'], df['DAY_MEAN120'], c=colors[4])
        plt.plot(df['DATE'], df['DAY_MEAN240'], c=colors[5])
        plt.scatter(df[df['BREAK'] == 1]['DATE'], df[df['BREAK'] == 1]['CLOSING_PRICE'], c=colors[6],
                    zorder=10, s=14)  # breakpoint
        plt.bar(df_['DATE'], df_['REVENUE'], color=colors[7])
        plt.xticks(color='w')
        plt.legend(handles=[mpatches.Patch(color=c, label=l) for c, l in zip(colors, labels)])


        # grid(2)
        plt.subplot(plt_grid[2, 0:3])  # 0 row, 1之後的所有column
        plt.bar(df['DATE'], df['TRADE_VOLUME'])
        utils.plt_figure_interval(df)


        # grid(table)
        plt.subplot(plt_grid[0:, 3:])  # 1 row, 2 column
        df = self.revenue(data, inputs, utils)
        plt.axis('tight')
        plt.axis('off')
        table = plt.table(cellText=df.values,
                          colLabels=df.columns,
                          colWidths=[0.5, 0.6],
                          loc='center left',
                          )
        table.set_fontsize(32)
        table.scale(1, 3)

        plt.savefig(f"{PICTURE_DIR}/breakpoint_{inputs['STOCK_CODE']}.jpg")
