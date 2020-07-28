
from ftplib import FTP

host = 'serv.izmiran.ru'
user = 'dbnuser'
passwd = 'FFmaftp5b'

year = '2019'
filename = 'NAD_'+year+'0100_60pp'

with FTP(host=host, user=user, passwd=passwd) as ftp:
    # ftp.dir()
    ftp.cwd('/'+year+'/01/mag/')

    with open(filename+'.ffh', 'wb') as f:
        ftp.retrbinary('RETR ' + filename+'.ffh', f.write)

    with open(filename+'.ffd', 'wb') as f:
        ftp.retrbinary('RETR ' + filename+'.ffd', f.write)


# with open('ftp://dbnuser:FFmaftp5b@serv.izmiran.ru/2009/01/mag/MOS_20090100_60pp.ffh') as file:
#     # это была красивая бесполезная строчка, но так можно зайти через бровзер
