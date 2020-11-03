from flask import Flask, request
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import time
import hashlib
import numpy
import datetime

app = Flask(__name__)
db = []

db_connection = 'mysql+pymysql://artemkmp_web:*Lo02Kal@artemkmp.beget.tech/artemkmp_web'
conn = create_engine(db_connection)

df = pd.read_sql("SELECT * FROM users", conn)
 
print ("connect successful!!")

@app.route("/")
def hello():
	return "Hello  v 1.5"

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

@app.route("/messages")
def messages():
	if 'after_id' in request.args:
		after_id = int(request.args['after_id'])+1
	else:
		after_id = 0	

	limit = 100

	return{'messages':db[after_id:after_id+limit]}	

@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    return response

app.run(host = '0.0.0.0', port=5000)	