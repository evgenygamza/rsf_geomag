import k_index_calculator as kic
import pandas as pd
import datetime

df = pd.read_csv('MOS_20180400_60pp.csv', parse_dates=[0, 1, 2])
print(df.head(10))

# time = [kic.Time2Float(stamp) for stamp in df['dt'].to_numpy()]
time = kic.Time2Float(pd.to_datetime(df['dt'].to_numpy()))
mosH = df['MOS_H'].to_numpy()
mosE = df['MOS_E'].to_numpy()
print(kic.KIndexSuperCalc(time, mosH, mosE, 560))

#
print(type(time))
print(time)
# print(df['dt'][1000])
# print(type(df['dt'][1000]))
# print(datetime.datetime.strptime(df['dt'][1000], '%Y-%m-%d %H:%M:%S'))
# print(type(datetime.datetime.strptime(df['dt'][1000], '%Y-%m-%d %H:%M:%S')))
#
