import requests

username = 'ItsKaffwory'

response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")



if response.status_code == 200:
    print('Utente trovato')
    print(response.json())
else:
    print('Utente non trovato')
    print(response)


