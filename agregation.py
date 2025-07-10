# agregation.py

from pymongo import MongoClient,errors



try:
    
    # Connexion à MongoDB Atlas
    client = MongoClient("mongodb://localhost:27017/")
    # client = MongoClient("mongodb+srv://appUser:MotDePasseAtlas123@cluster0.9d4zwcs.mongodb.net/Projet_Ecommerce?retryWrites=true&w=majority")
    db = client["Projet_Ecommerce"]

    # Accès aux collections
    produits_col = db["produits"]
    clients_col = db["clients"]
    commandes_col = db["commandes"]




    # 
    # $group
    # But : Calculer le total dépensé par chaque client.
    # Lecture : Affiche un document par client avec son total.
    # 
    pipeline = [
        {"$group": {"_id": "$client_id", "total_depense": {"$sum": "$total"}}}
    ]
    for doc in commandes_col.aggregate(pipeline):
        print("le total dépensé par chaque client.")
        print(doc)



    # 
    #  $group + $sort + $limit
    # But : Obtenir le top 3 des clients qui ont le plus dépensé.
    # Lecture : Classement décroissant par total.
    # 
    pipeline = [
        {"$group": {"_id": "$client_id", "total_depense": {"$sum": "$total"}}},
        {"$sort": {"total_depense": -1}},
        {"$limit": 3}
    ]
    for doc in commandes_col.aggregate(pipeline):
        print("top 3 des clients qui ont le plus dépensé.")
        print(doc)
        
        


    # 
    #  $project
    # But : Afficher les commandes avec un champ TVA calculé à 20%.
    # Lecture : Nouveau champ 'TVA' visible dans les résultats.
    # 
    pipeline = [
        {"$project": {"total":1, "TVA": {"$multiply": ["$total", 0.2]}}}
    ]
    for doc in commandes_col.aggregate(pipeline):
        print("Affichage des commandes avec un champ TVA calculé à 20%.")
        print(doc)



    # 
    #  $lookup
    # But : Faire une jointure pour enrichir les commandes avec les infos clients.
    # Lecture : Ajoute un tableau 'client_info' avec le client correspondant.
    # 
    pipeline = [
        {"$lookup": {
            "from": "clients",
            "localField": "client_id",
            "foreignField": "_id",
            "as": "client_info"
        }}
    ]
    for doc in commandes_col.aggregate(pipeline):
        print("Ajoute un tableau 'client_info' avec le client correspondant.")
        print(doc)



    # 
    # $unwind
    # But : Éclater le tableau 'produits' pour avoir un document par produit commandé.
    # Lecture : Chaque produit est sur une ligne différente.
    # 
    pipeline = [
        {"$unwind": "$produits"},
        {"$project": {"produits":1}}
    ]
    for doc in commandes_col.aggregate(pipeline):
        print("document par produit commandé.")
        print(doc)




    # 
    # $unwind + $group
    # But : Compter combien de fois chaque produit a été commandé.
    # Lecture : Affiche le nombre de commandes par produit.
    # 
    pipeline = [
        {"$unwind": "$produits"},
        {"$group": {"_id": "$produits.nom", "nb_commandes": {"$sum": 1}}},
        {"$sort": {"nb_commandes": -1}}
    ]
    for doc in commandes_col.aggregate(pipeline):
        print("Nombre de fois chaque produit a été commandé.")
        print(doc)
        



    # 
    # $group stats globales
    # But : Calculer le total et la moyenne des montants commandés.
    # Lecture : Donne deux indicateurs globaux sur toutes les commandes.
    # 
    pipeline = [
        {"$group": {
            "_id": None,
            "total_commande": {"$sum": "$total"},
            "moyenne_commande": {"$avg": "$total"}
        }}
    ]
    for doc in commandes_col.aggregate(pipeline):
        print("le total et la moyenne des montants commandés.")
        print(doc)




    # 
    #  $lookup + $unwind + $match
    # But : Trouver les commandes dont le client a un email contenant 'dupont'.
    # Lecture : Combine jointure et filtrage sur le champ client.
    # 
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
        print("les commandes dont le client a un email contenant 'dupont'.")
        print(doc)
        
except errors.ConnectionFailure as e:
    print("Échec de la connexion MongoDB :", e)
except errors.PyMongoError as e:
    print("Erreur PyMongo :", e)
except Exception as e:
    print("Erreur inattendue :", e)

