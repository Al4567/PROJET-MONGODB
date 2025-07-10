## remplissage de la base avec 20 produits ,clients et commandes

"""
    Génère aléatoirement 20 produits à partir d'un catalogue prédéfini 
    en variant leur prix et leur stock, puis insère ces produits dans 
    une collection MongoDB.

    Paramètres
    ----------
    collection : pymongo.collection.Collection
        La collection MongoDB dans laquelle les produits seront insérés.

    Retourne
    --------
    None
"""


from pymongo import MongoClient,errors
from datetime import datetime
import random

try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["Projet_Ecommerce"]

        # Collections
        produits_col = db["produits"]
        clients_col = db["clients"]
        commandes_col = db["commandes"]


        
        # Enrégistrement des produits
        produits_catalogue = [
            {"nom": "Clavier mécanique RGB", "categorie": "Informatique", "prix": 89.99, "stock": 50},
            {"nom": "Souris sans fil Logitech", "categorie": "Informatique", "prix": 45.00, "stock": 75},
            {"nom": "Écran 27 pouces Samsung", "categorie": "Informatique", "prix": 229.99, "stock": 20},
            {"nom": "Casque Bluetooth Sony", "categorie": "Informatique", "prix": 129.99, "stock": 40},
            {"nom": "Lampe LED bureau", "categorie": "Maison", "prix": 39.90, "stock": 100},
            {"nom": "Aspirateur Dyson", "categorie": "Maison", "prix": 399.00, "stock": 15},
            {"nom": "Tapis de course", "categorie": "Sport", "prix": 499.00, "stock": 10},
            {"nom": "Raquette de tennis Babolat", "categorie": "Sport", "prix": 79.90, "stock": 30},
            {"nom": "Ballon de football Adidas", "categorie": "Sport", "prix": 29.90, "stock": 60},
            {"nom": "Montre connectée Garmin", "categorie": "Sport", "prix": 199.00, "stock": 25}
        ]

        # Dupliquer et varier pour arriver à 20
        produits = []
        for i in range(20):
            p = random.choice(produits_catalogue).copy()
            p["stock"] = random.randint(5, 100)
            p["prix"] = round(random.uniform(p["prix"] * 0.8, p["prix"] * 1.2), 2)
            produits.append(p)

        produits_col.insert_many(produits)


        # Enrégistrement des clients

        prenoms = ["Jean", "Marie", "Paul", "Sophie", "Luc", "Emma", "Louis", "Julie", "Pierre", "Laura"]
        noms = ["Dupont", "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Moreau"]

        clients = []
        for i in range(20):
            nom_client = f"{random.choice(prenoms)} {random.choice(noms)}"
            email_client = nom_client.lower().replace(" ", ".") + "@gmail.com"
            client = {
                "nom": nom_client,
                "email": email_client,
                "adresse": f"{random.randint(1,100)} rue Exemple, Ville",
                "date_inscription": datetime(2025, 7, random.randint(1, 6))
            }
            clients.append(client)

        clients_result = clients_col.insert_many(clients)


        # Enrégistrement des commandes

        commandes = []
        for i in range(20):
            client_id = random.choice(clients_result.inserted_ids)
            nb_produits = random.randint(1, 3)
            produits_commande = []
            total = 0
            for _ in range(nb_produits):
                p = random.choice(produits)
                qte = random.randint(1, 4)
                produits_commande.append({
                    "nom": p["nom"],
                    "quantite": qte,
                    "prix_unitaire": p["prix"]
                })
                total += p["prix"] * qte
            commandes.append({
                "client_id": client_id,
                "date_commande": datetime(2025, 7, random.randint(1, 6)),
                "produits": produits_commande,
                "total": round(total, 2)
            })

        commandes_col.insert_many(commandes)

        print("Données  insérées dans MongoDB")
        
except errors.ConnectionFailure as e:
    print("Échec de la connexion MongoDB :", e)
except errors.PyMongoError as e:
    print("Erreur PyMongo :", e)
except Exception as e:
    print("Erreur inattendue :", e)
