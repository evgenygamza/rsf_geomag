"""
2020-07-21  @gamza
pack of instruments for work with rsf_mag databases.
Contains folowing functions:
 - ftp_download
 - table_constructor (not ready)
 - bin2csv
 - csv2sql
 - bin2sql (not ready)
 - plotter (not ready)
"""

__author__ = 'Gamza'
__email__ = 'evgeny.gamza@gmail.com'

import os
import julian
from datetime import datetime
import numpy as np
import pandas as pd
from ftplib import FTP
from sqlalchemy import create_engine


def ftp_download(ftp_params, year, month, station):
    """
    function for getting paired flat files
    :type station: str
    :param ftp_params: {'host': 'ftp://serv.ismiran.ru',
    'user': 'dbnuser', 'passwd': '******'}
    :param year: '2009'
    :param month: '01'
    :param station: 'MOS'
    :return: local filename
    """
    host = ftp_params.get('host', '')  # 'serv.izmiran.ru'
    user = ftp_params.get('user', '')  # 'dbnuser'
    passwd = ftp_params.get('passwd', '')  # '****'
    filename = station.upper() + '_' + year + month + '00_60pp'
    lowcase_filename = station.lower() + '_' + year + month + '00_60pp'

    with FTP(host=host, user=user, passwd=passwd) as ftp:
        try:
            ftp.cwd('/' + year + '/' + month + '/mag/')  # template of filepath
            # ftp.dir()
            if (filename + '.ffh') in ftp.nlst() and (filename + '.ffd') in ftp.nlst():
                with open(filename + '.ffh', 'wb') as f:
                    ftp.retrbinary('RETR ' + filename + '.ffh', f.write)
                with open(filename + '.ffd', 'wb') as f:
                    ftp.retrbinary('RETR ' + filename + '.ffd', f.write)
                print(filename + ' dowloading complete')

            # once upon a time I saw in database files witn lowcase index, but where and when -
            # this is the question. So maybe today we finally found them! Let's try:
            elif (lowcase_filename + '.ffh') in ftp.nlst() and (lowcase_filename + '.ffd') in ftp.nlst():
                with open(lowcase_filename + '.ffh', 'wb') as f:
                    ftp.retrbinary('RETR ' + filename + '.ffh', f.write)
                with open(lowcase_filename + '.ffd', 'wb') as f:
                    ftp.retrbinary('RETR ' + filename + '.ffd', f.write)
                print(filename + ' dowloading complete')
                with open('faillog.txt', 'a') as logfile:  # fail logging
                    logfile.write('!!!!Lowcase Happened!!!! ' + filename + '\n')

            else:
                print('no *.ffh or *.ffd file on ftp')
                with open('faillog.txt', 'a') as logfile:  # fail logging
                    logfile.write('{:<30}|{:^25}|{:>35}  |  {}\n'.
                                  format(filename, host,
                                         'ftp download failure at:', datetime.now()))
                return filename
        except:
            print('troubles with ' + filename + ' on ftp')
            with open('faillog.txt', 'a') as logfile:  # fail logging
                logfile.write('{:<30}|{:^25}|{:>35}  |  {}\n'.
                              format(filename, host,
                                     'troubles with ftp at:', datetime.now()))
    # with open('ftp://dbnuser:****@serv.izmiran.ru/2009/01/mag/') as file:
    #     # это была бесполезная строчка, но так можно зайти через браузер
    return filename


def table_constructor(user, passwd, server, database, dbtype='mysql', driver='pymysql'):
    """
    creates new table in selected database
    :param user:
    :param passwd:
    :param server:
    :param database:
    :param dbtype:
    :param driver:
    :return:
    """
    pass


def bin2csv(filename, jtc=False, delete=False):
    """
    converts paired flat files (*.ffd + *.ffh) to *.csv
    :param filename: 'filename without .extension'
    :param jtc: julian time code
    :param delete: if True, removes ffd & ffh files after convertion
    :return: nothing
    """

    # 1. first we should get info from header files
    if not os.path.isfile(filename + '.ffh'):
        print(filename + '.ffh Not found')
        with open('faillog.txt', 'a') as logfile:  # fail logging
            logfile.write('{:<30}|{:^25}|{:>35}  |  {}\n'.
                          format(filename + '.ffh', 'local dir', 'processing failure at:', datetime.now()))
    else:
        with open(filename + '.ffh', 'r') as ffh:
            # reading first part of header file
            recsize = 0  # number of bytes in a single measure count
            Nrows = 0  # number of measurements
            Ncols = 0  # number of column headers
            Missvs = 0  # value flagging missing data
            for row in ffh:  # reading
                value = row.split('=')[-1]  # variable takes parameters while passing cycle
                if '----' in row:
                    break
                elif 'RECORD' in row:
                    recsize = int(value)
                elif 'COLUMNS' in row:
                    Ncols = int(value)
                elif 'ROWS' in row:
                    Nrows = int(value)
                elif 'MISSING' in row:
                    Missvs = np.float64(value)  # todo check out header file for other parameters
            ffh.readline()
            # then we read the rest of the header file
            colheaders = []  # headers of our csv-table
            for row in ffh:
                if row.find('<') >= 0:
                    colheaders.append(row.split('<')[1].split('>')[0])
                else:
                    break
            # end of header reading
        print('file length is: %d counts' % Nrows)
        print('number of column headers: %d' % (Ncols + 1))
        print('estimated file size: %d' % (recsize * Nrows))

    # 2. then we open binary file
    if not os.path.isfile(filename + '.ffd'):
        print(filename + '.ffd Not found')
        with open('faillog.txt', 'a') as logfile:  # fail logging
            logfile.write('{:<30}|{:^25}|{:>35}  |  {}\n'.
                          format(filename + '.ffd', 'local dir', 'processing failure at:', datetime.now()))
    else:
        with open(filename + '.ffd', 'rb') as ffd:
            dt = np.dtype([('time', 'f8'), ('data', repr(Ncols) + 'f4')])  # template for reading binary file
            n1 = 0  # first count
            n2 = Nrows  # last count
            array_a = np.fromfile(ffd, dtype=dt, count=int(n2 - n1))  # primary array
            array_b = []  # list in list todo make the numpy array
            for row in array_a:  # convert array format to simple table
                rowlist = [row[0]]
                for value in row[1]:
                    rowlist.append(value)
                array_b.append(rowlist)
            ffd.close()  # end of ffd reading

            # 3. and now we're going to convert our list to dataframe
            if jtc:
                timecode = [i[0] for i in array_b]  # we can use julian timecode
            else:
                timecode = [julian.from_jd(i[0], 'mjd').strftime('%Y-%m-%d %H:%M:%S') for i in array_b]
            data = [i[1:] for i in array_b]
            df = pd.DataFrame(data, index=timecode, columns=colheaders[1:])  # todo missing to None
            df.index.name = 'timecode' if jtc else 'dt'
            df = df.replace({Missvs: None, -1.0000000331813535e+32: None})  # it's time to remove missing values

        # 4. finally we make *.csv
        with open(filename + '.csv', 'w') as outfile:
            df.to_csv(outfile, sep=',')

    # 5. P.S. optional delete ff
    if delete and os.path.isfile(filename + '.ffh'):
        os.remove(filename + '.ffh')
        print(filename + '.ffh removed from this PC')
    if delete and os.path.isfile(filename + '.ffd'):
        os.remove(filename + '.ffd')
        print(filename + '.ffd removed from this PC')


def csv2sql(filename, sql_params, delete=False):
    """
    function for sending csv-data to sql-database
    :param sql_params: {host, user, passwd, database, bd_type, driver}
    :param filename: str
    :param delete: delete filename from local directory
    :return:
    """
    if not os.path.isfile(filename + '.csv'):
        print(filename + '.csv Not found')
        with open('faillog.txt', 'a') as logfile:  # fail logging
            logfile.write('{:<30}|{:^25}|{:>35}  |  {}\n'.
                          format(filename + '.csv', 'local dir', 'processing failure at:', datetime.now()))
        return
    host = sql_params.get('host', '')  # 'crsa.izmiran.ru'
    user = sql_params.get('user', '')  # 'gamza'
    passwd = sql_params.get('passwd', '')  # '*****'
    database = sql_params.get('database', '')  # 'rsf_mag'
    db_type = sql_params.get('db_type', '')  # 'mysql'
    driver = sql_params.get('driver', '')  # 'pymysql'

    # taking csv & create df  # todo X, Y, Z variations
    # df = pd.read_csv(filename + '.csv', skiprows=1, names=['dt', 'H', 'E', 'Z', 'temp'])
    df = pd.read_csv(filename + '.csv')
    df.rename(columns={filename[:4]+'T': 'temp', filename[:4]+'t': 'temp'}, inplace=True)
    df.rename(columns=lambda x: x.replace(filename[:4], ''), inplace=True)
    print(df.head(5))

    # connecting to DB
    # engine = create_engine('mysql+pymysql://gamza:*****@crsa.izmiran.ru/rsf_mag', echo=True)
    try:
        engine = create_engine('{}+{}://{}:{}@{}/{}'.
                               format(db_type, driver, user, passwd, host, database), echo=False)
    except:
        with open('faillog.txt', 'a') as logfile:  # fail logging
            logfile.write('{:<30}|{:^25}|{:>35}  |  {}\n'.
                          format(filename + '.csv', host, 'sql insertion failure at:', datetime.now()))
            return

    # inserting df into database
    try:
        df.to_sql(filename[:3], index=False, con=engine, if_exists='append')
    except:
        with open('faillog.txt', 'a') as logfile:  # fail logging
            logfile.write('{:<30}|{:^25}|{:>35}  |  {}\n'.
                          format(filename + '.csv', host, 'sql insertion failure at:', datetime.now()))

    # optional delete csv
    if delete:
        os.remove(filename + '.csv')
        print(filename + '.csv removed from this PC')


def bin2sql(filename):  # todo
    """
    for straight transit from *.ffd to sql database
    :param filename:
    :return:
    """
    pass


def plotter(some, variables):  # todo
    pass
