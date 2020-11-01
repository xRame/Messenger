import requests
r = requests.post('http://127.0.0.1:5000/login', json = {'login':'login','password':'password'})
print(r.content)