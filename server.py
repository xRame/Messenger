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
db = []

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
	return "Hello  v 1.92"

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

@app.route("/send", methods = ['POST'])
def send():
	data = request.json
	
	db.append({
		'id':len(db),
		'name': data['name'],
		'text': data['text'],
		'timestamp': time.time()

		})
	return{'ok':True}

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
			continue

		data = {'image':image,'name':name,'text':text,'date':date,'last':last,'chat_id':chat_id,'type_chat':type_chat}
		json.update({chat_id:data})
	return json

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


@app.route("/messages")
def messages():
	if 'after_id' in request.args:
		after_id = int(request.args['after_id'])+1
	else:
		after_id = 0	

	limit = 100
	return{'messages':db[after_id:after_id+limit]}	

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