import pandas as pd
from .analysis_method import AnalysisMethod


class BreakPoint(AnalysisMethod):
    def analysis_info(self, data, inputs, utils):
        print('break point analysis')
        pass

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
            tmpA = data.iloc[k]['BREAK_PRICE'] * 1.1
            tmpB = data.iloc[k]['BREAK_PRICE'] * 0.97
            for i, j in zip(data.iloc[k:]['CLOSING_PRICE'], data.iloc[k:]['DATE']):
                if (i > tmpA) | (i < tmpB):
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

        return data

    def revenue(self, data, inputs, utils):
        df_result = pd.DataFrame(columns=['股票代號', '最後股價', '總收益', '進出金額', '進出次數'])
        df_tmp = self.analysis(data, inputs, utils)
        df_tmpResult = df_tmp[(df_tmp['BREAK_PRICE'] != 0)
                              & (df_tmp['LIMIT_UP'] != 1)
                              & (df_tmp['SOLD_PRICE'] != 0)]
        lst_result = [
            # inputs['code'],
            df_tmp.iloc[-1]['CLOSING_PRICE'],
            round(df_tmpResult['REVENUE'].sum(), 2),
            round(df_tmpResult['CLOSING_PRICE'].sum(), 2),
            len(df_tmpResult)
        ]
        return lst_result

        for i in list(data['SECURITY_CODE'].drop_duplicates()):
            lst_data = I.revernue(df=df, require_inputs=require_inputs)
            df_result.loc[len(df_result)] = lst_data
            print(lst_data)
        data = 3
        print(data)
        return data

    def plot_graph(self, data, inputs, utils):
        data = 4
        return data
