import requests

vk = 'TOKEN_NUM'

response = requests.get('https://api.vk.com/method/friends.get?fields=sex&access_token=TOKEN_NUM&v=5.130')


print(response.text)

with open('friends.json','w', encoding='utf-8') as friends:
    friends.write(response.text)