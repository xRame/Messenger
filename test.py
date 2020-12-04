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
# Подключиться к базе данных.
 
db_connection = 'mysql+pymysql://artemkmp_web:*Lo02Kal@artemkmp.beget.tech/artemkmp_web'
conn = create_engine(db_connection)
df = pd.read_sql("SELECT * FROM usersBlackList", conn)

def getChats(user_id):
	cm = pd.read_sql("SELECT * FROM chatMembers WHERE user_id="+str(user_id), conn)
	# print(cm.chat_id)
	json = {}
	for i in range(len(cm.chat_id)):
		data = {}
		chat_id = str(cm.chat_id[i])
		# chat_id = '7'
		chatInfo = pd.read_sql("SELECT * FROM chatInfo WHERE chat_id="+chat_id, conn)
		messages = pd.read_sql("SELECT * FROM messages WHERE chat_id="+chat_id, conn)
		lastSeen = pd.read_sql("SELECT * FROM lastSeen WHERE chat_id="+chat_id, conn)
		chats = pd.read_sql("SELECT * FROM chats WHERE id="+str(chat_id), conn)
		print(chat_id,'\n')
		try:
			type_chat = int(chats.loc[0, 'type'])
			if type_chat == 0:
				cm1 = pd.read_sql("SELECT * FROM chatMembers WHERE chat_id="+str(chat_id), conn)
				if cm1.user_id[0] == user_id:
					user = pd.read_sql("SELECT * FROM users WHERE id="+str(int(cm1.user_id[1])), conn)
					image = user.loc[0, 'avatarUrl']
					name = user.loc[0, 'login']	
					
				else:
					user = pd.read_sql("SELECT * FROM users WHERE id="+str(cm1.user_id[0]), conn)	
					image = user.loc[0, 'avatarUrl']
					name = user.loc[0, 'login']	
				
			else:
				try:
					image = chatInfo.loc[0, 'avatarUrl']
				except:
					image = 'None'
				name = chatInfo.loc[0, 'name']
			try:	
				text = messages[-1:].text.iloc[0]
				date =  messages[-1:].date.iloc[0]
			except:
				text = 'Чат пуст'	
				date = 'None'
			last = lastSeen.loc[0, 'time']
			
		except:
			print('err')
			pass

		data = {'image':image,'name':name,'text':text,'date':date,'last':last,'chat_id':chat_id,'type_chat':type_chat}
		json.update({chat_id:data})
		# print(image)
		# print(name)
		# print(text)
		# print(date)
		# print(last)
		# print(chat_id)
		# print(type_chat)
	print(json)
# conn.execute("UPDATE chatInfo SET avatarUrl = %s WHERE chat_id=%s",('https://st03.kakprosto.ru/images/article/2011/9/23/1_525518e6d765d525518e6d769a.png','4'))
# data = {'user_id':[2], 'chat_id':[7], 'time':['2020-11-02 13:34:19']}
# dfn = pd.DataFrame(data)
# dfn.to_sql(con=conn, name='lastSeen', if_exists='append', index = False)
# cm = pd.read_sql("SELECT * FROM lastSeen", conn)
# getChats(1)


def findUser(user_login):
	users = pd.read_sql("SELECT * FROM users WHERE login LIKE '%"+str(user_login)+"%'", conn)
	json = {}
	print(users)
	for i in range(len(users)):
		data = {}
		login = users.loc[i, 'login']
		avatarUrl = users.loc[i, 'avatarUrl']
		userId = str(users.loc[i, 'id'])
		lastActivity = users.loc[i, 'lastActivity']
		print(avatarUrl)
		data = {'login':login,'avatarUrl':avatarUrl,'userId':userId,'lastActivity':lastActivity}
		json.update({userId:data})
	print(json)	

# findUser('Nikita')
# data = {'user_id':['1'], 'blocked_user_id':['28']}
# dfn = pd.DataFrame(data)
# dfn.to_sql(con=conn, name='usersBlackList', if_exists='append', index = False)
name = 'Venne'
chats = pd.read_sql("SELECT * FROM chats", conn)
page = 2
messages = pd.read_sql("SELECT * FROM messages WHERE chat_id=7", conn)[-2*(page+1):-2*page]
print(chats)