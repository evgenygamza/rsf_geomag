import k_index_calculator as kic
import pandas as pd
import numpy as np
import datetime

# df = pd.read_csv('MOS_20190401-04.csv', parse_dates=[0], index_col='dt',
df0 = pd.read_csv('MOS_20190400_60pp.csv', parse_dates=[0], index_col='dt',
                  dtype=float, decimal='.')
for day in range(20):
    df = df0['2019-04-{:02d} 00:00:29'.format(1+day): '2019-04-{:02d} 00:00:29'.format(5+day)]
    print(df.head(10))

    time = kic.Time2Float(pd.to_datetime(df.index.to_numpy()))
    print(time[:10])

    mosH = [float(hui) for hui in df['MOS_H'].to_numpy()]
    mosE = df['MOS_E'].to_numpy()
    mosZ = df['MOS_Z'].to_numpy()

    time_prepared, x, y, z = kic.MinuteBin(time, mosH, mosE, mosZ)
    k_index, k_time, order = kic.KIndexSuperCalc(time_prepared, x, y, 560)
    print(k_index)
    print(type(k_index))
    print(len(k_index[8:]))

    with open('k index.txt', 'a') as outfile:
        outfile.write('2019-04-{:02d}: {}  {:02d}\n'.format(day+2, [int(k) for k in k_index[8:16]],
                                                        sum([int(k) for k in k_index[8:16]])))
        # outfile.write('2019-04-', day+1, ': ', k_index[8:], '\n')
#     df['2019-04-01 00:00:29':'2019-04-05 00:00:29'].to_csv(outfile, sep=',', line_terminator="\n")
# df = pd.read_csv('MOS_20190401-04.csv', parse_dates=[0], index_col='dt', dtype=float, decimal='.')

# time = [kic.Time2Float(stamp) for stamp in df['dt'].to_numpy()]
# print(kic.KIndexSuperCalc(time, mosH, mosE, 560))


# print('HUIHUIHUI')
# print(k_index)




#
print(type(time))
print(time)
# print(df['dt'][1000])
# print(type(df['dt'][1000]))
# print(datetime.datetime.strptime(df['dt'][1000], '%Y-%m-%d %H:%M:%S'))
# print(type(datetime.datetime.strptime(df['dt'][1000], '%Y-%m-%d %H:%M:%S')))
#
