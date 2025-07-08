from pymongo import MongoClient

"""
But : Créer un utilisateur 'appUser' directement sur la base 'Projet_Ecommerce',
avec un rôle readWrite sur cette même base.
"""

client = MongoClient("mongodb://localhost:27017/")
db = client["Projet_Ecommerce"]

try:
    db.command("createUser", "appUser",
        pwd="MotDePasse123",
        roles=[{"role": "readWrite", "db": "Projet_Ecommerce"}]
    )
    print("Utilisateur 'appUser' créé sur 'Projet_Ecommerce' avec succès.")
except Exception as e:
    print(" Erreur (peut-être utilisateur déjà existant) :", e)
