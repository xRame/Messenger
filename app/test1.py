import requests
import datetime
	
import json
response = requests.post('http://messengerpy-env-1.eba-rs4kjrzc.us-east-2.elasticbeanstalk.com/login', json = {'login':'Nikita','password':'12345678'})
print(response.content)
