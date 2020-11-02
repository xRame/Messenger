import requests
	
import json
response = requests.post('http://127.0.0.1:5000/login', json = {'login':'Bob','password':'12345678'})
print(response.text)