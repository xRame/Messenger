from sqlalchemy import create_engine
import pymysql
import pandas as pd
import requests
import hashlib

# json = {'login':'login','password':'password'}
# r = requests.get('http://messengerpy-env-1.eba-rs4kjrzc.us-east-2.elasticbeanstalk.com/messages',params = {'after_id': 0})
# print(r.content)

 
# Подключиться к базе данных.
connection = pymysql.connect(host='artemkmp.beget.tech',
                             user='artemkmp_web',
                             password='*Lo02Kal',                             
                             db='artemkmp_web')
 
print ("connect successful!!")
 
db_connection = 'mysql+pymysql://artemkmp_web:*Lo02Kal@artemkmp.beget.tech/artemkmp_web'
conn = create_engine(db_connection)

df = pd.read_sql("SELECT * FROM users", conn)

# print(df[df['login'].str.contains('Bob')]['token'][0])
print(str(df[df['login'].str.contains('Anon')]['token'] == str(hashlib.md5('12345678'.encode()).hexdigest()))[5])
# print(df[df['login'].str.contains('Anon')]['token'])
# print(str(hashlib.md5('12345678'.encode()).hexdigest()))
# for l in df['login']:
# 	if 'Bob' == l:
# 		print(df[l])

# if 'Bob' in df['login']:
# 	print('yes')
# print(df['login'][2])


# hash_object = hashlib.md5('12345678'.encode())
# print(hash_object.hexdigest())