# -*- coding: utf-8 -*-

import pymysql
from datetime import datetime, timedelta

db = pymysql.connect(host="crsa.izmiran.ru", user="user", passwd="user", db='geomag')
cursor = db.cursor()
def datas(sql):
    cursor.execute(sql)
    return cursor.fetchall()


#    Input data
sdt = datetime(2019,1,1,0,0,0)
edt = datetime(2019,1,2,0,0,0)

print('Example 1')
#    Example 1
for i in datas("""SELECT dt,kp1,kp2,kp3,kp4,kp5,kp6,kp7,kp8 FROM izmiran WHERE dt BETWEEN '%s' AND '%s'""" % (sdt,edt)):
    print(i)

#    Example 2
print('\nExample 2')
for i in datas("""SELECT * FROM izmiran WHERE dt BETWEEN '%s' AND '%s'""" % (sdt,edt)):
    print(i)

#    Example 3
print('\nExample 3')
data = [i for i in datas("""SELECT * FROM izmiran WHERE dt BETWEEN '%s' AND '%s'""" % (sdt,edt))]
print(data)

#    Example 4
print('\nExample 4')
dt,kp1,kp2,kp3,kp4,kp5,kp6,kp7,kp8 = zip(*[i for i in datas("""SELECT * FROM izmiran WHERE dt BETWEEN '%s' AND '%s'""" % (sdt,edt))])
print(dt)
print(kp1)
print(kp2)
