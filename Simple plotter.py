# -*- coding: cp1251 -*-
__Author__ = 'Gamza'

from mag_db_lib import timeline_plotter
sql = {'host': 'crsa.izmiran.ru', 'user': 'gamza', 'passwd': '12344321',
       'database': 'rsf_mag', 'db_type': 'mysql', 'driver': 'pymysql'}
# start_dt = dt.datetime.strptime('2018-04-01 20:00', '%Y-%m-%d %H:%M')
# end_dt = dt.datetime.strptime('2018-04-01 21:00', '%Y-%m-%d %H:%M')

start_dt = '2018-04-01 20:00'
end_dt = '2018-04-01 21:00'


timeline_plotter(sql, 'MOS', start_dt, end_dt)
