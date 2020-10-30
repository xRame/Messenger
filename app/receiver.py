import requests
import time
from datetime import datetime

def pr_print(message):
	dt = datetime.fromtimestamp(message['timestamp'])
	dt = dt.strftime('%H:%M')
	first_line = dt + ' ' + message['name']
	print(first_line)
	print(message['text'])


url = 'http://127.0.0.1:5000/messages'
after_id = -1

while  True:
	response = requests.get(url, params = {'after_id': after_id+1})
	messages = response.json()['messages']
	for message in messages:
		pr_print(message)
		after_id = message['id']


		if not message:
			time.sleep(1)