from sqlalchemy import create_engine
import pymysql
import pandas as pd
import requests
import hashlib
import datetime

# Подключиться к базе данных.
 
db_connection = 'mysql+pymysql://artemkmp_web:*Lo02Kal@artemkmp.beget.tech/artemkmp_web'
conn = create_engine(db_connection)

df = pd.read_sql("SELECT * FROM users", conn)


# print(df.loc[df['login'].str.contains('Anon'), 'token'].iloc[0])
# print(df.loc[df['login'].str.contains('Anon'),'id'].iloc[0])

# print(df['email'])
# Index(['id', 'avatarUrl', 'login', 'email', 'lastActivity', 'token'], dtype='object')
print(len(df))
# df.loc[4] = {1,2}
# today = datetime.datetime.today()
# image = 'None'
# login = 'login'
# email = 'email'
# lastActivity = today.strftime("%Y-%m-%d %H:%M")
# token = hashlib.md5('12345678'.encode()).hexdigest()
# dfn = {'avatarUrl':image, 'login':login, 'email':email, 'lastActivity':lastActivity, 'token':token}
# # df.loc[4] = {'id':idp, 'avatarUrl':image, 'login':login, 'email':email, 'lastActivity':lastActivity, 'token':token}
# data = {'avatarUrl':[image], 'login':[login], 'email':[email], 'lastActivity':[lastActivity], 'token':[token]}
# dfn = pd.DataFrame(data)
print((df.iloc[-1,0]+1))
print(df.id)
# hash_object = hashlib.md5('12345678'.encode())
# print(hash_object.hexdigest())