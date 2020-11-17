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
# Подключиться к базе данных.
 
db_connection = 'mysql+pymysql://artemkmp_web:*Lo02Kal@artemkmp.beget.tech/artemkmp_web'
conn = create_engine(db_connection)
df = pd.read_sql("SELECT * FROM messages", conn)

print(df)