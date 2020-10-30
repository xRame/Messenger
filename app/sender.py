import requests

url = 'https://messengerpy-env-1.eba-rs4kjrzc.us-east-2.elasticbeanstalk.com/status'

response = requests.get(url)
	
print(response.status_code)