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
import pyautogui
 
db_connection = 'mysql+pymysql://artemkmp_web:*Lo02Kal@artemkmp.beget.tech/artemkmp_web'
conn = create_engine(db_connection)
df = pd.read_sql("SELECT * FROM usersBlackList", conn)


# conn.execute("DELETE FROM chats WHERE id=25",)
for i in range(2000):
	pyautogui.click()