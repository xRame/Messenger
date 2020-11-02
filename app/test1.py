import requests
	
import json
response = requests.post('http://127.0.0.1:5000/login', json = {'login':'Anon','password':'12345678'})
print(response.content)