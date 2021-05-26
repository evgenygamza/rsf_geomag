import mag_db_lib as mdl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as md
import mag_db_lib

# files = 'godograph/BEY_20180400_60pp.csv'
# files = ['godograph/BEY_20180400_60pp.csv',
#          'godograph/KHS_20180400_60pp.csv',
#          'godograph/SKD_20180400_60pp.csv']
# start_dt = dt.datetime.strptime('2018-04-27 13:00', '%Y-%m-%d %H:%M')
# end_dt = dt.datetime.strptime('2018-04-27 18:30', '%Y-%m-%d %H:%M')

files = 'MOS_20180401-04.csv'
# for file in files:
#     mag_db_lib.bin2csv(file[:-4], jtc=False, delete=False)
start_dt = dt.datetime.strptime('2018-04-01 20:00', '%Y-%m-%d %H:%M')
end_dt = dt.datetime.strptime('2018-04-01 21:00', '%Y-%m-%d %H:%M')


def timeline_plotter(filenames, start, end, shift_step=30):  # todo csv, sql or ffd
    """

    :param shift_step: difference between colors for multiple magnetograms
    :param filenames: 'path/file.csv' or [list of 'path/file.csv']
    :param start:
    :param end:
    :param shiftstep: y-distance between timelines
    :return:
    """
    df_north_list = []
    df_east_list = []
    df_down_list = []

    if type(filenames) == str:
        filenames = [filenames]
    elif type(filenames) != list:
        print('You must give "path/***.csv" file name to this function')
        raise SystemExit

    timeline_shifter = len(filenames) * shift_step
    for file in filenames:  # todo read_csv with 'date and time' or 'dt'
        df = pd.read_csv(file, index_col='dt', parse_dates=['dt']).dropna()
        df = df[(df.index > start) & (df.index < end)]
        if end - start < dt.timedelta(days=1):
            df1 = df.copy()

        df_north_current = df.filter(regex=r'[A-Z]{3}_[HXhx]')
        df_north_current = df_north_current - df_north_current.min() + timeline_shifter  # to zero & shift
        df_north_list.append(df_north_current)

        df_east_current = df.filter(regex=r'[A-Z]{3}_[EYey]')
        df_east_current = df_east_current - df_east_current.min() + timeline_shifter
        df_east_list.append(df_east_current)

        df_down_current = df.filter(regex=r'[A-Z]{3}_[Zz]')
        df_down_current = df_down_current - df_down_current.min() + timeline_shifter
        df_down_list.append(df_down_current)

        timeline_shifter -= shift_step

    df_north = pd.concat(df_north_list, axis=1).sort_index()
    df_east = pd.concat(df_east_list, axis=1).sort_index()
    df_down = pd.concat(df_down_list, axis=1).sort_index()

    # Set up the matplotlib figure
    f, axes = plt.subplots(3, 1, figsize=(3, 6), sharex=True)
    sns.despine(left=True)
    # sns.set_style("ticks", {"xtick.major.size": 1, "ytick.major.size": 88})  # fixme why it doesn't work, suka?

    # sns.lineplot(data=df_north, palette="Reds_r", dashes=False, linewidth=1.2, ax=axes[0]).legend(loc=3)
    # sns.lineplot(data=df_east, palette="BuGn_r", dashes=False, linewidth=1.2, ax=axes[1]).legend(loc=6)
    # sns.lineplot(data=df_down, palette="Blues_r", dashes=False, linewidth=1.2, ax=axes[2]).legend(loc=2)
    # todo make this shit less shitable
    a = sns.lineplot(data=df_north, palette="Reds_r", dashes=False, linewidth=1.2, ax=axes[0])
    b = sns.lineplot(data=df_east, palette="BuGn_r", dashes=False, linewidth=1.2, ax=axes[1])
    c = sns.lineplot(data=df_down, palette="Blues_r", dashes=False, linewidth=1.2, ax=axes[2])
    a.legend(loc=3)
    b.legend(loc=6)
    c.legend(loc=2)
    a.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    b.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    c.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))

    # a.set(xticks=df_north.index.strftime('%H:%M'))
    # b.set(xticks=df_east.index.strftime('%H:%M'))
    # c.set(xticks=df_down.index.strftime('%H:%M'))


timeline_plotter(files, start=start_dt, end=end_dt)
plt.show()
# fixme empty image when savefig
# plt.savefig(fname='godograph/{}_Pivot.png'.format('_'.join([file.split('/')[-1][:3] for file in files])))
