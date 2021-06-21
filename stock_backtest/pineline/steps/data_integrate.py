from stock_backtest.pineline.steps.step import IntegrateABC


class Integrate(IntegrateABC):
    def __init__(self):
        pass

    def integrate(self, df, require_inputs):
        # caculate avg
        df_tmp = df[df['SECURITY_CODE'] == require_inputs['code']].reset_index(drop=True)
        df_tmp = df_tmp[(df_tmp['DATE'] >= require_inputs['startDate']) & (df_tmp['DATE'] <= require_inputs['endDate'])]
        df_tmp['DAY_MEAN5'] = df_tmp['CLOSING_PRICE'].rolling(5).mean()
        df_tmp['DAY_MEAN20'] = df_tmp['CLOSING_PRICE'].rolling(20).mean()
        df_tmp['DAY_MEAN60'] = df_tmp['CLOSING_PRICE'].rolling(60).mean()
        df_tmp['DAY_MEAN120'] = df_tmp['CLOSING_PRICE'].rolling(120).mean()
        df_tmp['DAY_MEAN240'] = df_tmp['CLOSING_PRICE'].rolling(240).mean()
        df_tmp['RISE'] = (((df_tmp['CLOSING_PRICE'].shift(1) / df_tmp['CLOSING_PRICE']) - 1) * -100).round(4)
        df_tmp.loc[(df_tmp['RISE'] > 9.5) & (df_tmp['RISE'] < 11), 'LIMIT_UP'] = 1
        return df_tmp

    def break_integrate(self, df, require_inputs):
        df_tmp = self.integrate(df, require_inputs)
        # define break point
        lst_break = []
        for i in range(len(df_tmp)):
            if df_tmp.iloc[i]['CLOSING_PRICE'] > df_tmp.iloc[:i]['CLOSING_PRICE'].max():
                lst_break.append(1)
            else:
                lst_break.append(0)
        df_tmp['BREAK'] = lst_break
        df_tmp['BREAK_PRICE'] = df_tmp['BREAK'] * df_tmp['CLOSING_PRICE']
        df_tmp['+10%'] = df_tmp['BREAK_PRICE'] * 1.1
        df_tmp['-3%'] = df_tmp['BREAK_PRICE'] * 0.97
        # define sold date and price
        lst_date = []
        lst_sold = []
        for k in range(len(df_tmp)):
            tmpA = df_tmp.iloc[k]['BREAK_PRICE'] * 1.1
            tmpB = df_tmp.iloc[k]['BREAK_PRICE'] * 0.97
            for i, j in zip(df_tmp.iloc[k:]['CLOSING_PRICE'], df_tmp.iloc[k:]['DATE']):
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
        df_tmp['SOLD_DATE'] = lst_date
        df_tmp['SOLD_PRICE'] = lst_sold
        df_tmp['REVENUE'] = df_tmp['SOLD_PRICE'] - df_tmp['BREAK_PRICE']
        return df_tmp

    def revernue(self, df, require_inputs):
        # Revenue calculate
        df_tmp = self.break_integrate(df, require_inputs)
        df_tmpResult = df_tmp[(df_tmp['BREAK_PRICE'] != 0) & (df_tmp['LIMIT_UP'] != 1) & (df_tmp['SOLD_PRICE'] != 0)]
        lst_result = [require_inputs['code'], df_tmp.iloc[-1]['CLOSING_PRICE'], round(df_tmpResult['REVENUE'].sum(), 2),
                      round(df_tmpResult['CLOSING_PRICE'].sum(), 2), len(df_tmpResult)]
        return lst_result
