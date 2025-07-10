from pymongo import MongoClient,errors

try:
    client = MongoClient("mongodb+srv://appUser:Atlas123@cluster0.9d4zwcs.mongodb.net/Projet_Ecommerce?retryWrites=true&w=majority")
    db = client["Projet_Ecommerce"]

    # Vérifier que ça marche
    print("Connexion réussie à Atlas !")

    # le nombre de documents dans chaque table
    print("Nombre de produits :", db["produits"].count_documents({}))
    print("Nombre de clients :", db["clients"].count_documents({}))
    print("Nombre de commandes :", db["commandes"].count_documents({}))
    
except errors.ConnectionFailure as e:
    print("Échec de la connexion à MongoDB :", e)
except errors.PyMongoError as e:
    print("Erreur PyMongo lors des opérations :", e)
except Exception as e:
    print("Erreur inattendue :", e)
