# Présentation du projet

## Projet E-commerce - MongoDB / PyMongo

## Contexte

- Projet de base de données NoSQL sous MongoDB pour le module Big Data / NoSQL.
- Domaine choisi : e-commerce
- Utilisation de PyMongo (Python) pour manipuler les données.
- Base hébergée localement et sur MongoDB Atlas pour la partie sécurité.

---

## Binôme

1. **AMEKOUDJI Arvin Lauris Gildas Efoé**
1. **TEKO EMMANUELLA**

## Structure du projet

``` bash
PROJETMONGODB
│
├── insert_data.py # Remplit la base avec produits, clients, commandes
├── create_user.py # Crée l'utilisateur MongoDB avec rôle readWrite
├── requetes.py # Exécute les 20 requêtes documentées
│
├── produits.json # Export JSON des produits
├── clients.json # Export JSON des clients
├── commandes.json # Export JSON des commandes
│
├── requêtes_et_sécurité.md # Document listant les requêtes, explications 
├── requêtes_et_sécurité.pdf # Version PDF du document
├── README.md 
├── requirements.txt # Liste des dépendances Python
|___ requetes_text.py # pour se connecter a la base de donnes sur Atlas
│
└── .vscode/ # Paramètres VS Code

---

## Exécution du projet

### Installer les dépendances

Dans ton terminal VS Code :

```bash
# contient les packages utilisés
pip install -r requirements.txt


## Execution des scripts A faire dans l'ordre

#  Cela insère les produits, clients et commandes dans la base MongoDB locale Projet_Ecommerce.
python insert_data.py


#  Cela lance les 20 requêtes (CRUD, filtres, agrégations) avec explications affichées dans le terminal.
python requetes.py

#  Créer l’utilisateur MongoDB local, Cela crée un utilisateur appUser avec rôle readWrite sur la base Projet_Ecommerce.
python create_user.py

```

## Bonus : Hébergement MongoDB Atlas

1. **Cluster gratuit M0 créé sur MongoDB Atlas.**

1. **Utilisateur appUser avec le même rôle readWrite.**

1. **IP whitelistée 0.0.0.0/0 pour les tests.**

1. **Import des données locales via mongoimport depuis produits.json, clients.json et commandes.json**

``` bash
# scripts d'export
mongoexport --db Projet_Ecommerce --collection produits --out produits.json --jsonArray
mongoexport --db Projet_Ecommerce --collection clients --out clients.json --jsonArray
mongoexport --db Projet_Ecommerce --collection commandes --out commandes.json --jsonArray

# scripts d'import sur le cluster 0 de Mongo Atlas

# pour la collection produits
mongoimport --uri "mongodb+srv://appUser:Atlas123@cluster0.9d4zwcs.mongodb.net/Projet_Ecommerce?retryWrites=true&w=majority&appName=Cluster0" --collection produits --file produits.json --jsonArray

# pour la collection clients

mongoimport --uri "mongodb+srv://appUser:Atlas123@cluster0.9d4zwcs.mongodb.net/Projet_Ecommerce?retryWrites=true&w=majority&appName=Cluster0" --collection clients --file clients.json --jsonArray


# pour la collection commandes
mongoimport --uri "mongodb+srv://appUser:Atlas123@cluster0.9d4zwcs.mongodb.net/Projet_Ecommerce?retryWrites=true&w=majority&appName=Cluster0" --collection commandes --file commandes.json --jsonArray



# Pour utiliser Atlas, il suffit de remplacer dans vos scripts dans requete.py:
client = MongoClient("mongodb+srv://appUser:Atlas123@cluster0.mongodb.net/Projet_Ecommerce")

