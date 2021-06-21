# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 16:19:22 2021

@author: pimi
"""
# %%
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import math
import os

# %%

host = os.getenv('sql_host')
port = 3306
user = os.getenv('sql_user')
passwd = os.getenv('sql_passwd')
db = 'stock'
conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
df_db = pd.read_sql('SELECT * FROM stock_everyday_new', con=conn)
df_db.head()
df = df_db.copy()

# %%
df = df
require_inputs = {
    'code': '2330',
    'startDate': '2019-01-01',
    'endDate': '2020-12-01'}

# %%
from stock_backtest.pineline.steps.data_integrate import Integrate

I = Integrate()
df_result = pd.DataFrame(columns=['股票代號', '最後股價', '總收益', '進出金額', '進出次數'])
for i in list(df['SECURITY_CODE'].drop_duplicates()):
    lst_data = I.revernue(df=df, require_inputs=require_inputs)
    df_result.loc[len(df_result)] = lst_data
    print(lst_data)
# %%
df_tmp = I.break_integrate(df=df, require_inputs=require_inputs)
# %%
plt.figure(figsize=(16, 6))

# avg line
plt.plot(df_tmp['DATE'], df_tmp['CLOSING_PRICE'])
# plt.bar(df_tmp['DATE'],plt.ylim()[1],width=0.15)
plt.plot(df_tmp['DATE'], df_tmp['DAY_MEAN5'])
plt.plot(df_tmp['DATE'], df_tmp['DAY_MEAN20'])
plt.plot(df_tmp['DATE'], df_tmp['DAY_MEAN60'])
plt.plot(df_tmp['DATE'], df_tmp['DAY_MEAN120'])
plt.plot(df_tmp['DATE'], df_tmp['DAY_MEAN240'])
# breakpoint
plt.scatter(df_tmp[df_tmp['BREAK'] == 1]['DATE'], df_tmp[df_tmp['BREAK'] == 1]['CLOSING_PRICE'], c='r', zorder=10, s=14)
# interval
df_tmp['YEAR'] = df_tmp['DATE'].apply(lambda x: x.split('-')[0])
df_tmp['MONTH'] = df_tmp['DATE'].apply(lambda x: x.split('-')[1])
lst_month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
lst_month_odd = ['01', '03', '05', '07', '09', '11']
lst_xsticks = []
for i in df_tmp['YEAR'].drop_duplicates():
    for k in lst_month:
        try:
            df_tmp_interval = df_tmp[(df_tmp['YEAR'] == i) & (df_tmp['MONTH'] == k)]
            lst_xsticks.append(df_tmp_interval.iloc[0]['DATE'])
            lst_xsticks.append(df_tmp_interval.iloc[math.ceil(len(df_tmp_interval) / 2)]['DATE'])
        except:
            continue
    for j in lst_month_odd:
        try:
            df_tmp_interval = df_tmp[(df_tmp['YEAR'] == i) & (df_tmp['MONTH'] == j)]
            plt.axvspan(xmin=df_tmp_interval.iloc[0]['DATE'],
                        xmax=df_tmp_interval.iloc[-1]['DATE'],
                        facecolor='grey', alpha=0.3)
        except:
            continue
plt.legend(['1days', '5days', '20days', '60days', '120days', '240days'])
plt.xticks(lst_xsticks, rotation=80)
# plt.minorticks_on()
# plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.grid(b=True, which='major', color='gray')

plt.show()

# %%
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Major ticks every 20, minor ticks every 5
major_ticks = np.arange(0, 101, 20)
minor_ticks = np.arange(0, 101, 5)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

# And a corresponding grid
ax.grid(which='both')

# Or if you want different settings for the grids:
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)
plt.xticks(lst_xsticks, rotation=60)

plt.show()
# %%
import matplotlib.pyplot as plt

# The Data
x = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', 12]
y = [234, 124, 368, 343, 222]
z = [1, 2, 3, 4, 5]
# Create the figure and axes objects
fig, ax = plt.subplots(1, figsize=(8, 6))
fig.suptitle('Example Of Plot With Major and Minor Grid Lines')

# Plot the data
ax.plot(x, y)
ax.plot(z, y)
# Show the major grid lines with dark grey lines
plt.grid(b=True, which='major', color='#666666', linestyle='-')

# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

plt.show()
