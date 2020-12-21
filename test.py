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
logins = []
for user_id in range(2):
	login = 'login' + 'user_id'
	avatarUrl = 'avatarUrl' + 'user_id'
	data = {'login':login,'avatarUrl':avatarUrl}
	logins.append(data)
req = {
	'users':logins
}	

print(req)