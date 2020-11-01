from flask import Flask, request
import time

app = Flask(__name__)
db = []
db_users = {'login':{'email':'email','password':'password','id':'1'}}

@app.route("/")
def hello():
	return "Hello  v 1.1"

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
	print('login with')
	print(data['login'])
	if data['login'] in db_users:
		if data['password'] == db_users[data['login']]['password']:
			return{
				  "status":"ok",
				  "description":"ok",
				  "userId":"",
				  "token": ""
				}
		else:
			return{
				  "status":"error",
				  "description":"wrong password"
				}	
	else: 	
		return{
				  "status":"error",
				  "description":"login not found"
				}	

@app.route("/register", methods = ['POST'])
def register():
	data = request.json
	if data['login'] in db_users:
		return{
			  "status":"error",
			  "description":"login is already taken"
			}
	# elif data['email'] in db_users.keys():
	# 	return{
	# 		  "status":"error",
	# 		  "description":"email is already taken"
	# 		}
	else:
		db_users.update({
			data['login']:{'email':data['email'],'password':data['password']}
		})
		
		return{
				  "status":"ok",
				  "description":""
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

print(db_users.keys())
app.run(host = '0.0.0.0', port=5000)	
