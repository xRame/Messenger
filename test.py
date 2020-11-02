from sqlalchemy import create_engine
import pymysql
import pandas as pd
import requests
import hashlib

# Подключиться к базе данных.
 
db_connection = 'mysql+pymysql://artemkmp_web:*Lo02Kal@artemkmp.beget.tech/artemkmp_web'
conn = create_engine(db_connection)

df = pd.read_sql("SELECT * FROM users", conn)

# print(df[df['login'].str.contains('Bob')]['token'][0])
# x = df[df['login'].str.contains('Anon')]['id']
print(df.loc[df['login'].str.contains('Anon'), 'token'].iloc[0])
print(df.loc[df['login'].str.contains('Anon'),'id'].iloc[0])
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