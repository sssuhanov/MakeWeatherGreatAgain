#%%
import sqlalchemy as db
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
# Подключаемся к базе и считываем данные
engine = db.create_engine('postgresql://postgres:kilo98ui@localhost/weather')
connection = engine.connect()
# Считываем из базы таблицу observ
df = pd.read_sql_table('observ', engine)

#%%
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['year'] = df['date'].dt.year

#%%
# Отбираем только летние месяца
df_summer = df[df['month'].isin(['6', '7', '8'])]

#%%
# Смотрим количество дней по годам
df_group_year = df_summer.groupby('year').count()
df_group_year

#%%
# Отбираем только теплые дни лета
df_summer_hot = df_summer[5/9*(df_summer['temperature']-32) >= 23]
# Группируем данные по годам
df_sh_group_year = df_summer_hot.groupby('year').count()

x = df_sh_group_year.index
y = df_sh_group_year['date']

fig, ax = plt.subplots()
line1, = ax.plot(x, y, label='Using set_dashes()')
plt.show()

#%%
df_summer_cold = df_summer[5/9*(df_summer['temperature']-32) < 23]
# Группируем данные по годам
df_sc_group_year = df_summer_cold.groupby('year').count()

x = df_sc_group_year.index
y = df_sc_group_year['date']

fig, ax = plt.subplots()
line1, = ax.plot(x, y, label='Using set_dashes()')
plt.show()

#%%
# График количества дождливых дней летом по годам
df_summer_rain = df_summer[df_summer['rain'] == True]
df_sr_group_year = df_summer_rain.groupby('year').count()

x = df_sr_group_year.index
y = df_sr_group_year['date']

fig, ax = plt.subplots()
line1, = ax.plot(x, y, label='Using set_dashes()')
plt.show()

#%%
