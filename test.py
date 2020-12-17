from sqlalchemy import create_engine
import pymysql
import pandas as pd
import requests
import hashlib
import datetime
import random
import string
import smtplib
import json
import traceback
from flask import url_for
# Подключиться к базе данных.
 
db_connection = 'mysql+pymysql://artemkmp_web:*Lo02Kal@artemkmp.beget.tech/artemkmp_web'
conn = create_engine(db_connection)
df = pd.read_sql("SELECT * FROM usersBlackList", conn)


# conn.execute("DELETE FROM chats WHERE id=25",)
chat_id = '8'
user_id = '2'
messages = pd.read_sql("SELECT * FROM messages WHERE chat_id="+chat_id, conn)
is_admin = pd.read_sql("SELECT time FROM lastSeen WHERE chat_id="+str(chat_id)+" AND user_id="+ str(user_id), conn).loc[0, 'time']
date =  messages[-1:].date.iloc[0]
print(date, is_admin)
print(date > is_admin)
t = datetime.datetime.strptime('2000-12-17 16:37:56',"%Y-%m-%d %H:%M:%S")
print(t)