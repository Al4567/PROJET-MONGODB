# Crud_et_requetes_simple.py

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

    # CRUD INSERT 
    # But : Ajouter un produit "Webcam Logitech" .
    # Lecture : Affiche le document inséré. 
    new_product = {
        "nom": "Webcam Logitech",
        "categorie": "Informatique",
        "prix": 69.90,
        "stock": 30
    }
    produits_col.insert_one(new_product)
    print("Produit ajouté :", new_product)




    # CRUD FIND simple
    # But : Lister tous les produits de la catégorie 'Informatique'.
    # Lecture : Affiche les documents correspondant.

    for prod in produits_col.find({"categorie": "Informatique"}):
        print("les produits de la catégorie 'Informatique'sont:")
        print(prod)

    # 
    # CRUD UPDATE
    # But : Incrémenter le stock de la Webcam Logitech de +10.
    # Lecture : Confirmation de la mise à jour.
    # 
    produits_col.update_one(
        {"nom": "Webcam Logitech"},
        {"$inc": {"stock": 10}}
    )
    print(" Stock mis à jour")

    # 
    #  CRUD DELETE
    # But : Supprimer le produit 'Webcam Logitech' du catalogue.
    # Lecture : Confirmation de la suppression.
    # 
    produits_col.delete_one({"nom": "Webcam Logitech"})
    print("Produit supprimé")



    # 
    #  FIND ONE
    # But : Trouver le client nommé 'Jean Dupont'.
    # Lecture : Affiche son document si trouvé.
    # 
    client = clients_col.find_one({"nom": "Laura Dupont"})
    print("le client est:",client)

    # 
    # Projection simple
    # But : Lister les commandes en affichant uniquement le total et la date.
    # Lecture : Affiche les commandes avec champs filtrés.
    # 
    for cmd in commandes_col.find({}, {"total":1, "date_commande":1}):
        print("Liste des commandes en affichant uniquement le total et la date.")
        print(cmd)
        
except errors.PyMongoError as e:
    print("Erreur MongoDB :", e)
except Exception as e:
    print("Erreur inattendue :", e)

