# okay, I have to say few words about it.
# This script takes old binary files from serv.izmiran.ru
# and places data from there to SQL-server crsa.izmiran.ru

import mag_db_lib as mdl

years = [str(y) for y in range(2017, 2022)]
months = ['%02d' % m for m in range(1, 13)]
# stations = ['MOS', 'NAD', 'KHS', 'BEY']
stations = ['BEY']

# years = [str(y) for y in range(2019, 2020)]
# months = ['%02d' % m for m in range(2, 4)]
# stations = ['mos']

ftp = {'host': 'serv.izmiran.ru', 'user': 'dbnuser', 'passwd': 'FFmaftp5b'}
sql = {'host': 'crsa.izmiran.ru', 'user': 'gamza', 'passwd': '12344321',
       'database': 'rsf_mag', 'db_type': 'mysql', 'driver': 'pymysql'}

# action!
for year in years:
    for month in months:
        for stn in stations:
            print('\nnow processing: {}-{}-{}'.format(stn, year, month))
            file = mdl.ftp_download(ftp_params=ftp, year=year, month=month, station=stn)
            mdl.bin2csv(file, delete=True)
            mdl.csv2sql(file, sql_params=sql, delete=True)
            # todo zaebashit' logfile
            print(file+' processing complete\n')

print('migration done')
