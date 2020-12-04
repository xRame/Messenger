from flask import Flask, request
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import time
import hashlib
import numpy
import datetime
import smtplib
import random
import string


app = Flask(__name__)

db_connection = 'mysql+pymysql://artemkmp_web:*Lo02Kal@artemkmp.beget.tech/artemkmp_web'
conn = create_engine(db_connection)

df = pd.read_sql("SELECT * FROM users", conn)
app.debug = True
app.SECURITY_EMAIL_SENDER = 'messengerweb1@gmail.com'

MAIL_DEBUG = 1 
SECURITY_EMAIL_SENDER = 'messengerweb1@gmail.com'
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login('messengerweb1@gmail.com','lFCMnO3H')
# smtpObj.connect('smtp.gmail.com')


print ("connect successful!!")

@app.route("/")
def hello():
	return "Hello  v 1.94"

@app.route("/status")
def status():
	return{
	'status':'OK',
	'messages':len(db),
	'user_cnt':len(set(message['name'] for message in db))
	}	

@app.route("/login", methods = ['POST'])
def login():
	data = request.json
	# print('login with',end = ' ')
	# print(data['login'])
	for l in df['login']:
		if data['login'] == l:
			password_enter = hashlib.md5(data['password'].encode()).hexdigest()
			password = df.loc[df['login'].str.contains(data['login']), 'token'].iloc[0]
			if (password_enter == password):
				return{
					  "status":"ok",
					  "description":"ok",
					  "userId":str(df.loc[df['login'].str.contains(data['login']),'id'].iloc[0]),
					  "token": str(password_enter)
					}
			else:
				return{
					  "status":"error",
					  "description":"wrong password"
					}		
	return{
			  "status":"error",
			  "description":"login not found"
			}	

@app.route("/register", methods = ['POST'])
def register():
	data = request.json
	print(data['login'])
	print(data['email'])
	print(data['password'])
	for l in df['login']:
		if data['login'] == l:
			return{
				  "status":"error",
				  "description":"login is already taken"
				}
	for l in df['email']:
		if data['email'] == l:
			return{
				  "status":"error",
				  "description":"email is already taken"
				}			
	if len(data['password']) < 4:
		return{
				  "status":"error",
				  "description":"password must be more than four characters"
				}
	today = datetime.datetime.today()
	idp = df.iloc[-1,0]
	image = 'None'
	login = data['login']
	email = data['email']
	lastActivity = today.strftime("%Y-%m-%d %H:%M")
	token = hashlib.md5(data['password'].encode()).hexdigest()
	data = {'avatarUrl':[image], 'login':[login], 'email':[email], 'lastActivity':[lastActivity], 'token':[token]}
	dfn = pd.DataFrame(data)
	dfn.to_sql(con=conn, name='users', if_exists='append', index = False)
	df.loc[idp] = {'id':idp+1, 'avatarUrl':image, 'login':login, 'email':email, 'lastActivity':lastActivity, 'token':token}
	return{
				  "status":"ok",
				  "description":"ok"
				}

@app.route("/restore", methods = ['POST'])
def restore():
	data = request.json
	login = data['login']

	new_password = data['password']
	new_password_hashed =  hashlib.md5(new_password.encode()).hexdigest()
	df.loc[df['login'].str.contains(login), 'token'] = new_password_hashed
	id_user = int(df.loc[df['login'].str.contains(login), 'id'].iloc[0])
	try:
		conn.execute("UPDATE users SET token = %s WHERE id=%s",(new_password_hashed, id_user))
	except(sqlalchemy.exc.OperationalError):
		print('hello')
	return{
				  "status":"ok",
				  "description":"ok"
				}

@app.route("/forget", methods = ['POST'])
def forget():
	data = request.json
	login = data['login']
	for l in df['login']:
		if login == l:
			id_user = int(df.loc[df['login'].str.contains(login), 'id'].iloc[0])
			new_password = ''.join(random.choice(string.ascii_letters) for _ in range(8))
			new_password_hashed =  hashlib.md5(new_password.encode()).hexdigest()
			df.loc[df['login'].str.contains(login), 'token'] = new_password_hashed
			FROM = 'messengerweb1@gmail.com'
			SUBJECT = "Restore password"
			TO = df.loc[df['login'].str.contains(login), 'email'].iloc[0]
			text = "Your new password: " + new_password

			BODY = "\r\n".join((
			    "From: %s" % FROM,
			    "To: %s" % TO,
			    "Subject: %s" % SUBJECT ,
			    "",
			    text
			))
			smtpObj.sendmail(FROM,TO,BODY)
			conn.execute("UPDATE users SET token = %s WHERE id=%s",(new_password_hashed, id_user))
			return{
						  "status":"ok",
						  "description":"ok"
						}

	return{
				  "status":"error",
				  "description":"login does not exist"
				}			

@app.route("/chats", methods = ['POST'])
def getChats():
	data = request.json
	user_id = data['id']
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
			skip = 0
			if type_chat == 0:
				cm1 = pd.read_sql("SELECT * FROM chatMembers WHERE chat_id="+str(chat_id), conn)
				block = pd.read_sql("SELECT * FROM usersBlackList WHERE user_id="+str(user_id), conn)
				if str(cm1.user_id[0]) == user_id:
					for i in range(len(block.blocked_user_id)):
						if str(cm1.user_id[1]) == str(block.blocked_user_id[i]):
							skip = 1 
					if skip == 1:
						print('skip')
						continue		
					user = pd.read_sql("SELECT * FROM users WHERE id="+str(cm1.user_id[1]), conn)
					image = user.loc[0, 'avatarUrl']
					name = user.loc[0, 'login']	
					online = user.loc[0, 'lastActivity']	
				else:
					for i in range(len(block.blocked_user_id)):
						if str(cm1.user_id[0]) == str(block.blocked_user_id[i]):
							skip = 1 
					if skip == 1:
						print('skip')
						continue		
					user = pd.read_sql("SELECT * FROM users WHERE id="+str(cm1.user_id[0]), conn)	
					image = user.loc[0, 'avatarUrl']
					name = user.loc[0, 'login']	
					online = user.loc[0, 'lastActivity']
			else:
				try:
					image = chatInfo.loc[0, 'avatarUrl']
				except:
					image = 'None'
				name = chatInfo.loc[0, 'name']
				online = 'None'
			try:	
				text = messages[-1:].text.iloc[0]
				date =  messages[-1:].date.iloc[0]
			except:
				text = 'Чат пуст'	
				date = 'None'
			try:	
				last = lastSeen.loc[0, 'time']
			except:
				last = 'New'
			
		except:
			print('err')
			continue

		data = {'image':image,'name':name,'text':text,'date':date,'last':last,'chat_id':chat_id,'type_chat':type_chat,'online':online}
		json.update({chat_id:data})
	return json

@app.route("/addChat", methods = ['POST'])
def addChat():
	data = request.json
	user_id = data['id']
	name = data['name']
	users = data['users']
	for_chats = {'owner_id':[user_id], 'type':[1]}
	dfn = pd.DataFrame(for_chats)
	dfn.to_sql(con=conn, name='chats', if_exists='append', index = False)

	chat_id = str(pd.read_sql("SELECT * FROM chats ORDER BY ID DESC LIMIT 1", conn).loc[0, 'id'])

	for_chatInfo = {'chat_id':chat_id,'name':[name], 'avatarUrl':['None']}
	dfn = pd.DataFrame(for_chatInfo)
	dfn.to_sql(con=conn, name='chatInfo', if_exists='append', index = False)
	new_users = []
	for i in range(len(users)):
		new_users.append(str(pd.read_sql("SELECT id FROM users WHERE login = '"+users[i]+"'", conn).loc[0, 'id']))
	new_users.append(user_id)
	users = new_users	
	print(new_users)
	for i in range(len(users)):
		is_admin = 0
		if users[i]==user_id:
			is_admin = 1
		for_chatMembers = {'chat_id':[chat_id], 'user_id':[users[i]], 'is_admin':[is_admin]}
		dfn = pd.DataFrame(for_chatMembers)
		dfn.to_sql(con=conn, name='chatMembers', if_exists='append', index = False)
	return{
	  "name": name,
	  "chatId": chat_id,
	  "chatType": 1
	}

@app.route("/addPrivateChat", methods = ['POST'])
def addPrivateChat():
	data = request.json
	user_id = data['id']
	name = data['login']
	user = str(pd.read_sql("SELECT id FROM users WHERE login = '"+name+"'", conn).loc[0, 'id'])
	
	for_chats = {'owner_id':[user_id], 'type':[0]}
	dfn = pd.DataFrame(for_chats)
	dfn.to_sql(con=conn, name='chats', if_exists='append', index = False)

	chat_id = str(pd.read_sql("SELECT * FROM chats ORDER BY ID DESC LIMIT 1", conn).loc[0, 'id'])

	for_chatInfo = {'chat_id':chat_id,'name':[name], 'avatarUrl':['None']}
	dfn = pd.DataFrame(for_chatInfo)
	dfn.to_sql(con=conn, name='chatInfo', if_exists='append', index = False)

	users = [user_id ,user]
	for i in range(len(users)):
		for_chatMembers = {'chat_id':[chat_id], 'user_id':[users[i]], 'is_admin':[0]}
		dfn = pd.DataFrame(for_chatMembers)
		dfn.to_sql(con=conn, name='chatMembers', if_exists='append', index = False)
	return{
	  "name": name,
	  "chatId": chat_id,
	  "chatType": 1
	}

@app.route("/getNote", methods = ['POST'])
def getNote():
	data = request.json
	user_id = data['id']
	login = data['noted_user_login']
	noted_user_id = str(pd.read_sql("SELECT id FROM users WHERE login = '"+str(login)+"'", conn).loc[0, 'id'])
	try:
		note = str(pd.read_sql("SELECT note_content FROM userNote WHERE author_user_id="+str(user_id)+" AND about_user_id="+noted_user_id, conn).loc[0, 'note_content'])
	except:
		print('except')
		return{
		'note':'NONE'
	}
	# print(user_id)
	# print(noted_user_id)
	return{
		'note': note
	}

@app.route("/addNote", methods = ['POST'])
def addNote():
	data = request.json
	user_id = data['id']
	login = data['noted_user_login']
	note = data['note']
	noted_user_id = str(pd.read_sql("SELECT id FROM users WHERE login = '"+str(login)+"'", conn).loc[0, 'id'])
	try:
		note_1 = str(pd.read_sql("SELECT note_content FROM userNote WHERE author_user_id="+str(user_id)+" AND about_user_id="+noted_user_id, conn).loc[0, 'note_content'])
	except:
		data = {'about_user_id':[noted_user_id], 'author_user_id':[user_id],'note_content':[note]}
		dfn = pd.DataFrame(data)
		dfn.to_sql(con=conn, name='userNote', if_exists='append', index = False)
		return{
		  "status":"ok",
		  "description":"note added"
		}
	conn.execute("UPDATE userNote SET note_content = %s WHERE author_user_id=%s AND about_user_id=%s",(note, user_id, noted_user_id))
	return{
		  "status":"ok",
		  "description":"note changed"
		}

@app.route("/addBlockedUsers", methods = ['POST'])
def addBlockedUsers():
	data = request.json
	user_id = data['id']
	name = data['blocked_user_login']
	blocked_user_id = str(pd.read_sql("SELECT id FROM users WHERE login = '"+str(name)+"'", conn).loc[0, 'id'])
	data = {'user_id':[user_id], 'blocked_user_id':[blocked_user_id]}
	dfn = pd.DataFrame(data)
	dfn.to_sql(con=conn, name='usersBlackList', if_exists='append', index = False)
	return{
		  "status":"ok",
		  "description":"ok"
		}

@app.route("/removeBlockedUsers", methods = ['POST'])
def removeBlockedUsers():
	data = request.json
	user_id = data['id']
	name = data['blocked_user_login']
	blocked_user_id = str(pd.read_sql("SELECT id FROM users WHERE login = '"+str(name)+"'", conn).loc[0, 'id'])
	conn.execute("DELETE FROM usersBlackList WHERE user_id=%s AND blocked_user_id=%s",(user_id, blocked_user_id))
	return{
	  "status":"ok",
	  "description":"ok"
	}

@app.route("/getBlockedUsers", methods = ['POST'])
def getBlockedUsers():
	data = request.json
	user_id = data['id']
	cm = pd.read_sql("SELECT * FROM usersBlackList WHERE user_id="+str(user_id), conn)
	# print(cm)
	json = {}
	for i in range(len(cm.blocked_user_id)):
		blocked_user_id = str(cm.blocked_user_id[i])
		userInfo = pd.read_sql("SELECT * FROM users WHERE id="+blocked_user_id, conn)
		try:
			avatarUrl = userInfo.loc[0, 'avatarUrl']
			login = userInfo.loc[0, 'login']
			lastActivity = userInfo.loc[0, 'lastActivity']
		except:
			continue
		data = {'login':login, 'avatarUrl':avatarUrl, 'userId':blocked_user_id, 'lastActivity':lastActivity}
		json.update({blocked_user_id:data})
		# print(blocked_user_id)
		# print(avatarUrl)
		# print(login)
		# print(lastActivity)
		# print(json)
	return json	

@app.route("/findUser", methods = ['POST'])
def findUser():
	data = request.json
	user_login = data['login']
	users = pd.read_sql("SELECT * FROM users WHERE login LIKE '%"+str(user_login)+"%'", conn)
	if len(users) == 0:
		return{"status":"error",
				"description":"login not found"}
	json = {}
	for i in range(len(users)):
		data = {}
		login = users.loc[i, 'login']
		avatarUrl = users.loc[i, 'avatarUrl']
		userId = str(users.loc[i, 'id'])
		lastActivity = users.loc[i, 'lastActivity']
		data = {'login':login,'avatarUrl':avatarUrl,'userId':userId,'lastActivity':lastActivity}
		json.update({userId:data})

	return json

@app.route("/newMessage", methods = ['POST'])
def newMessage():
	today = datetime.datetime.today()
	time = today.strftime("%Y-%m-%d %H:%M")
	data = request.json
	user_id = data['id']
	text = data['message']
	chatId = data['chatId']
	data = {'text':[text], 'date':[time],'user_id':[user_id],'chat_id':[chatId]}
	dfn = pd.DataFrame(data)
	dfn.to_sql(con=conn, name='messages', if_exists='append', index = False)
	return{
	  "status":"ok",
	  "description":"ok"
	}

@app.route("/getMessages", methods = ['POST'])
def getMessages():
	data = request.json
	user_id = data['id']
	chatId = data['chatId']
	page = int(data['page'])
	json = {}
	messages_list = []
	try:
		if page == 0:
			messages = pd.read_sql("SELECT * FROM messages WHERE chat_id="+chatId, conn)[-20:]
		else:
			messages = pd.read_sql("SELECT * FROM messages WHERE chat_id="+chatId, conn)[-2*(page+1):-2*page]
	except:
		return{"status":"error",
				"description":"empty chat"}
	for i in range(len(messages)):
		message_id = str(messages.loc[i, 'id'])
		message = messages.loc[i, 'text']
		timestamp = messages.loc[i, 'date']
		id_user = str(messages.loc[i, 'user_id'])
		user = pd.read_sql("SELECT * FROM users WHERE id="+id_user, conn)
		name = user.loc[0, 'login']
		avatarUrl = user.loc[0, 'avatarUrl']
		mes = {
		"id": message_id,
	      "user": {
	        "id": id_user,
	        "name": name,
	        "avatarUrl": avatarUrl
	      },
	      "message": message,
	      "timestamp": timestamp
	    }
		messages_list.append(mes)

	data = {'page':page,
	'messages':messages_list}
	json.update(data)
	return data

@app.route("/getLastTime", methods = ['POST'])
def getLastTime():
	data = request.json
	user_id = data['id']
	time = pd.read_sql("SELECT lastActivity FROM users WHERE id="+user_id, conn).loc[0, 'lastActivity']
	return{
		'time':time
	}

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    return response

@app.before_request
def before_request():
	data = request.json
	today = datetime.datetime.today()
	time = today.strftime("%Y-%m-%d %H:%M")
	try:
		user_id = data['id']
		conn.execute("UPDATE users SET lastActivity = %s WHERE id=%s",(time, user_id))
	except:
		pass
	try:
		login = data['login']
		conn.execute("UPDATE users SET lastActivity = %s WHERE login=%s",(time, login))
	except:
		pass	

app.run(host = '0.0.0.0', port=5000)	