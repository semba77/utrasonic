import requests

url = 'http://Ondra-GamePC.sembera.net:80/count'

x = requests.put(url, json={'value': 11})

print(x)
