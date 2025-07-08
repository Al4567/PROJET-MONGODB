# Exécute les 20 requêtes (CRUD, avancées, agrégations)

from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
produits_col = db["produits"]
clients_col = db["clients"]
commandes_col = db["commandes"]

############################## CRUD ET REQUETES SIMPLES #####################################

print("\n==============================")
print("CRUD & requêtes simples")
print("==============================")

""" 
 CRUD INSERT 
But : Ajouter un produit "Webcam Logitech" dans la boutique.
Lecture : Affiche le document inséré.
"""
new_product = {
    "nom": "Webcam Logitech",
    "categorie": "Informatique",
    "prix": 69.90,
    "stock": 30
}
produits_col.insert_one(new_product)
print(" Produit ajouté :", new_product)

"""
 CRUD FIND simple
But : Lister tous les produits de la catégorie 'Informatique'.
Lecture : Affiche les documents correspondant.
"""
for prod in produits_col.find({"categorie": "Informatique"}):
    print(prod)

"""
 CRUD UPDATE
But : Incrémenter le stock de la Webcam Logitech de +10.
Lecture : Confirmation de la mise à jour.
"""
produits_col.update_one(
    {"nom": "Webcam Logitech"},
    {"$inc": {"stock": 10}}
)
print(" Stock mis à jour")

"""
 CRUD DELETE
But : Supprimer le produit 'Webcam Logitech' du catalogue.
Lecture : Confirmation de la suppression.
"""
produits_col.delete_one({"nom": "Webcam Logitech"})
print("Produit supprimé")

"""
 FIND ONE
But : Trouver le client nommé 'Jean Dupont'.
Lecture : Affiche son document si trouvé.
"""
client = clients_col.find_one({"nom": "Jean Dupont"})
print(client)

"""
Projection simple
But : Lister les commandes en affichant uniquement le total et la date.
Lecture : Affiche les commandes avec champs filtrés.
"""
for cmd in commandes_col.find({}, {"total":1, "date_commande":1}):
    print(cmd)


############################ Requêtes avancées ###################################################

print("\n==============================")
print(" Requêtes avancées")
print("==============================")

"""
 $and
But : Trouver les clients inscrits en juillet 2025 avec un email se terminant par @example.com.
Lecture : Liste des clients qui satisfont les deux conditions.
"""
for client in clients_col.find({
    "$and": [
        {"email": {"$regex": "@example.com$"}},
        {"date_inscription": {"$gte": datetime(2025,7,1)}}
    ]
}):
    print(client)

"""
 $or
But : Trouver les produits ayant moins de 10 en stock ou coûtant plus de 300€.
Lecture : Affiche les produits qui répondent à au moins une condition.
"""
for prod in produits_col.find({
    "$or": [
        {"stock": {"$lt": 10}},
        {"prix": {"$gt": 300}}
    ]
}):
    print(prod)

"""
 $regex
But : Lister les clients dont le nom commence par 'J'.
Lecture : Affiche tous les clients correspondants.
"""
for client in clients_col.find({"nom": {"$regex": "^J"}}):
    print(client)

"""
 $in
But : Trouver les produits 'Tapis de course' ou 'Aspirateur Dyson'.
Lecture : Affiche uniquement ces produits.
"""
for prod in produits_col.find({"nom": {"$in": ["Tapis de course", "Aspirateur Dyson"]}}):
    print(prod)

"""
$exists
But : Lister les commandes qui contiennent bien un champ 'produits'.
Lecture : Affiche toutes les commandes valides avec ce champ.
"""
for cmd in commandes_col.find({"produits": {"$exists": True}}):
    print(cmd)

"""
 Projection + sort
But : Lister les clients triés par date d'inscription décroissante, avec nom et date uniquement.
Lecture : Permet de voir les plus récents d'abord.
"""
for client in clients_col.find({}, {"nom":1, "date_inscription":1}).sort("date_inscription", -1):
    print(client)






################################ Agrégations ###################################################

print("\n==============================")
print("Agrégations")
print("==============================")

"""
    $group
But : Calculer le total dépensé par chaque client.
Lecture : Affiche un document par client avec son total.
"""
pipeline = [
    {"$group": {"_id": "$client_id", "total_depense": {"$sum": "$total"}}}
]
for doc in commandes_col.aggregate(pipeline):
    print(doc)



"""
 $group + $sort + $limit
But : Obtenir le top 3 des clients qui ont le plus dépensé.
Lecture : Classement décroissant par total.
"""
pipeline = [
    {"$group": {"_id": "$client_id", "total_depense": {"$sum": "$total"}}},
    {"$sort": {"total_depense": -1}},
    {"$limit": 3}
]
for doc in commandes_col.aggregate(pipeline):
    print(doc)
    
    


"""
 $project
But : Afficher les commandes avec un champ TVA calculé à 20%.
Lecture : Nouveau champ 'TVA' visible dans les résultats.
"""
pipeline = [
    {"$project": {"total":1, "TVA": {"$multiply": ["$total", 0.2]}}}
]
for doc in commandes_col.aggregate(pipeline):
    print(doc)



"""
 $lookup
But : Faire une jointure pour enrichir les commandes avec les infos clients.
Lecture : Ajoute un tableau 'client_info' avec le client correspondant.
"""
pipeline = [
    {"$lookup": {
        "from": "clients",
        "localField": "client_id",
        "foreignField": "_id",
        "as": "client_info"
    }}
]
for doc in commandes_col.aggregate(pipeline):
    print(doc)



"""
$unwind
But : Éclater le tableau 'produits' pour avoir un document par produit commandé.
Lecture : Chaque produit est sur une ligne différente.
"""
pipeline = [
    {"$unwind": "$produits"},
    {"$project": {"produits":1}}
]
for doc in commandes_col.aggregate(pipeline):
    print(doc)




"""
$unwind + $group
But : Compter combien de fois chaque produit a été commandé.
Lecture : Affiche le nombre de commandes par produit.
"""
pipeline = [
    {"$unwind": "$produits"},
    {"$group": {"_id": "$produits.nom", "nb_commandes": {"$sum": 1}}},
    {"$sort": {"nb_commandes": -1}}
]
for doc in commandes_col.aggregate(pipeline):
    print(doc)
    



"""
$group stats globales
But : Calculer le total et la moyenne des montants commandés.
Lecture : Donne deux indicateurs globaux sur toutes les commandes.
"""
pipeline = [
    {"$group": {
        "_id": None,
        "total_commande": {"$sum": "$total"},
        "moyenne_commande": {"$avg": "$total"}
    }}
]
for doc in commandes_col.aggregate(pipeline):
    print(doc)




"""
 $lookup + $unwind + $match
But : Trouver les commandes dont le client a un email contenant 'dupont'.
Lecture : Combine jointure et filtrage sur le champ client.
"""
pipeline = [
    {"$lookup": {
        "from": "clients",
        "localField": "client_id",
        "foreignField": "_id",
        "as": "client_info"
    }},
    {"$unwind": "$client_info"},
    {"$match": {"client_info.email": {"$regex": "dupont"}}}
]
for doc in commandes_col.aggregate(pipeline):
    print(doc)
    


print("\n Fin des requêtes ! Tout a été exécuté avec succès.")
