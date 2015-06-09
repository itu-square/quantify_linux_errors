import sys
import csv
import pymysql


db = pymysql.connect(host='mysql.itu.dk',
    user='elvis_thesis',
    passwd='linux',
    db='elvis_thesis')

cursor = db.cursor()

cursor.execute('insert into types (name, severity) values ("-Wwhat", 2)')
cursor.close()
