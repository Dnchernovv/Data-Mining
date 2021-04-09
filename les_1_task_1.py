import requests
import json

username = 'username'

token = ('TOKEN')

info = requests.get('https://api.github.com/user/repos', auth=(username, token))

print(info.text)


with open('repos.json','w') as repos:
    repos.write(info.text)