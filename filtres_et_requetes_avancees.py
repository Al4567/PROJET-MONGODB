# filtres_et_requetes_avancees

from pymongo import MongoClient
from datetime import datetime

# Connexion à MongoDB Atlas
client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient("mongodb+srv://appUser:MotDePasseAtlas123@cluster0.9d4zwcs.mongodb.net/Projet_Ecommerce?retryWrites=true&w=majority")
db = client["Projet_Ecommerce"]

# Accès aux collections
produits_col = db["produits"]
clients_col = db["clients"]
commandes_col = db["commandes"]


# 
#  $and
# But : Trouver les clients inscrits en juillet 2025 avec un email se terminant par @gmail.com.
# Lecture : Liste des clients qui satisfont les deux conditions.
# 
for client in clients_col.find({
    "$and": [
        {"email": {"$regex": "@gmail.com$"}},
        {"date_inscription": {"$gte": datetime(2025,7,1)}}
    ]
}):
    print("les clients inscrits en juillet 2025 avec un email se terminant par @gmail.com sont:")
    print(client)

# 
#  $or
# But : Trouver les produits ayant moins de 10 en stock ou coûtant plus de 300€.
# Lecture : Affiche les produits qui répondent à au moins une condition.
# 
for prod in produits_col.find({
    "$or": [
        {"stock": {"$lt": 10}},
        {"prix": {"$gt": 300}}
    ]
}):
    print("les produits ayant moins de 10 en stock ou coûtant plus de 300€ sont:")
    print(prod)

# 
#  $regex
# But : Lister les clients dont le nom commence par 'J'.
# Lecture : Affiche tous les clients correspondants.
# 
for client in clients_col.find({"nom": {"$regex": "^J"}}):
    print("les clients dont le nom commence par J sont:")
    print(client)

# 
#  $in
# But : Trouver les produits 'Tapis de course' ou 'Aspirateur Dyson'.
# Lecture : Affiche uniquement ces produits.
# 
for prod in produits_col.find({"nom": {"$in": ["Tapis de course", "Aspirateur Dyson"]}}):
    print("les produits 'Tapis de course' ou 'Aspirateur Dyson'")
    print(prod)

# 
# $exists
# But : Lister les commandes qui contiennent bien un champ 'produits'.
# Lecture : Affiche toutes les commandes valides avec ce champ.
# 
for cmd in commandes_col.find({"produits": {"$exists": True}}):
    print("Liste des commandes qui contiennent bien un champ 'produits'. ")
    print(cmd)

# 
#  Projection + sort
# But : Lister les clients triés par date d'inscription décroissante, avec nom et date uniquement.
# Lecture : Permet de voir les clients  plus récents .
# 
for client in clients_col.find({}, {"nom":1, "date_inscription":1}).sort("date_inscription", -1):
    print("Liste des clients triés par date d'inscription décroissante, avec nom et date uniquement.")
    print(client)

