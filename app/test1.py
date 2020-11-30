import requests
import datetime
import smtplib
import json
 #'login':'Nikita','password':'12345678', 'email':'wildflex@gm.com' http://127.0.0.1:5000
 # http://messengerpy-env-1.eba-rs4kjrzc.us-east-2.elasticbeanstalk.com/

response = requests.post(' http://127.0.0.1:5000/login', json = {'login':'Venne','password':'BLuAnGxJ'}) 
print(response.headers)
print(response.content)

# conn.execute("UPDATE users SET token = %s WHERE id=%s",(new_password, '2'))