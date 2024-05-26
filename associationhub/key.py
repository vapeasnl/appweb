import os

# Générer une clé secrète aléatoire
secret_key = os.urandom(24)
print(secret_key.hex())

