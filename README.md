# Exam_Datagong_Doliveux

# 1. Contexte et objectifs du projet :

# Ce projet s’inscrit dans un contexte d’analyse des performances commerciales d’une entreprise de distribution multicanale.
# L’objectif principal est de fournir une vision synthétique et exploitable de plusieurs KPIs (chiffre d’affaires, marge, panier moyen, taux de retour) selon plusieurs axes d’analyse (catégorie de produits, marque, région/ville), afin d’aider à la prise de décision stratégique. Le KPI taux de réachat est calculé uniquement par année.

# Les objectifs principaux sont les suivants :

# - Analyser l'évolution des différents KPIs 2024 vs 2023 
# - Mettre en évidence la saisonalité, en particulier pour la Marge et le Chiffre d'Affaires
# - Identifier les catégories & zones géographiques les plus performantes
# - Identifier les catégories / marques "à risque" (taux de retour)- 
# - Comprendre la structure du panier moyen 



# 2. Description du sous-périmètre (filtres, tables, clés)
# Le fichier utilisé (CSV) provient d'un jeu public de Big Query, qui utilise les tables suivantes de 'bigquery-public-data.thelook_ecommerce': 
# - orders (commande, user_id)
# - order_items (lignes, sale_price, status, created_at)
# - products (référentiel produit : cost, brand, category, department)
# - users (profil client et géographie).

# Les clés utilisées sont :
# - users.id = orders.user_id
# - orders.order_id = order_items.order_id
# - products.id = order_items.product_id.

# Les filtres utilisés sont :
# - users.country = 'France' 
# - products.department = 'Women' 
# - DATE(order_items.created_at) entre '2023‑01‑01' et '2024‑12‑31'

# Le fichier CSV correspondant à la requête est dans le dossier "data": "thelook_fr_women_2023_2024"
# La requête SQL correspondant à l'extraction est stockée dans le dossier "sql" : "00_ma_table-extract_sous_perimetre"



# 3. Instructions d'installation et d'exécution :
# - Environnement Python venv. Plusieurs librairies sont nécessaires (cf fichier requirement.txt):pandas, numpy, seaborn, matplotlib
# - Installation des dépendances (bash) : pip install -r requirements.txt



# 4. Cheminement pour reproduire les résultats :
# 4.1. Extraction des données :
# - Exécution de la requêtes SQL "00_ma_table-extract_sous_perimetre" et extraction du CSV "thelook_fr_women_2023_2024.csv"

# 4.2 Exécution des fonctions (fonction pour convertir les dates, calculs des KPIs, fonction pour gérer la currency des graphiques)
# - S'assurer que les fonctions de src.utils.py ont bien été exécutées
# NB : Les fonctions ont été construites volontairement de façon "non-restrictives" de façon à pouvoir les utiliser avec un maximum d'axes / différents filtres. En particulier, il a été choisi de NE PAS intégrer d'office le filtre "order_status" == "Complete" dans les définitions des fonctions KPIs de CA, Marge, Panier Moyen, Taux de Réachat.

# 4.3 Test des fonctions (optionnel) :
# - Exécution du notebook 02_checks_coherence.ipynb -> Test de chaque fonction définie dans src.utils.py

# 4.4 Nettoyage, préparation des données, analyse exploratoire :
# 4.4.1 Exécuter le notebook 01_EDA_python.ipynb :
# La première partie du notebook permet d'importer le CSV, nettoyer et préparer les données (gestion des valeurs manquantes, contrôle de cohérence, ajout de colonnes mois / années)

# La seconde partie du notebook permet de créer des graphiques pour une analyses des KPIs selon les différents axes d'analyse:
# - Une page de vue d'ensemble permettant de voir la saisonalité du Chiffre d'Affaires & Marge ainsi que le Panier Moyen, Taux de rachat & Taux de Retour 2024 vs 2023
# - Une page dédiée à une investigation sur les catégories
# - une page d'analyse par région (X catégorie)
# - une page avec un zoom sur les villes (X catégories & pourcentage de nouvelles villes en 2024)
# - une page mettant en avant les Marques "Top performantes"

# 4.4.2  Vérification des KPIs calculés dans VS Code vs requêtes SQL:
# L'ensemble des requêtes du dossier sql (à l'exception de "00_ma_table-extract_sous_perimetre" qui permet de reconstituer le csv "thelook_fr_women_2023_2024.csv") permettent de recalculer les KPIs à partir d'un requête SQL. 
# Pour chaque KPI, il existe :
# - une requête SQL qui permet de calculer le KPI directement depuis une table "ma_table" ("ma_table" correspond au résultat de la requête SQL "00_ma_table-extract_sous_perimetre") -> SQL 01 à 044 "_from_ma_table"
# - une requête SQL qui permet de claculer le KPI directement depuis les tables existantes dans Big Query (pas de table intermédiaire) -> SQL 91 à 94 "_from scratch"




# 5. Décisions de design Power BI et principaux enseignements :
# 5.1 Choix de design : 
# Couleurs : #12239E pour l'année N-1 / #118DFF pour l'année sélectionnée, de façon harmonieuse avec le notebook

# 5.2 Principaux pré-requis et étapes à la construction du dashboard Power BI :
# - Load du fichier CSV "thelook_fr_women_2023_2024.csv" qui devient SOURCE_REF ->  base pour toutes les autres tables "Clients, Produits", "Ventes", 
# - Les 3 tables "Clients", "Produits", "Ventes" sont issues de "SOURCE_REF" en ne gardant que les colonnes utiles à chaque table
# - Traitement manuel des marques (brands) manquantes : dans la table "Produits" il manque deux valeurs dans "Brand". En filtrant on voit qu'on peut déduire une des valeurs en fonction du Nom Produit -> création d'une nouvelle colonne "Brand" remplaçant l'ancienne, en ajoutant l'une des valeur manquante
# Création d'un calendrier sur la base de "order_created_at". C'est cette dimension temporelle qui a été retenue pour rester cohérent avec les paramètres de l'extraction SQL. Il faut également créer un mois d'affichage (Mois_Aff) pour pouvoir avoir les noms des mois au lieu de 1, 2, 3 ...
# Création des KPIs dans une table "Mesure" : Pour les KPIs que l'on souhaite afficher mensuellement (CA & Marge), l'utilisation de la fonction COALESCE est impérative pour pouvoir afficher aussi les mois pour lesquels il n'y a pas de valeurs
# Création des filtres de sélection : "CA VS Marge" / "Brand VS Region"

# 5.3 Choix des pages et visuels :
# 5.3.1 Une page "Synthèse" mettant en avant les KPIs + évolution mensuelle. Des filtres en haut de page permettent de sélectionner l'année et le Chiffre d'Affaires OU Marge pour le graphique mensuel. Cette page montre aussi les CA / marge à venir en filtrant sur les commandes avec un order_status "Shipped" & "Processed"

# 5.3.2 Une page "Catégories" qui met en avant :
# - l'évolution du CA OU marge par catégorie sur l'année sélectionnée VS année précédente. 
# - la mensualité du CA OU Marge pour une ou plusieurs catégorie(s) sélectionnée(s) par l'utlisateur, avec possibilité de voir une décaomposition par Marque OU Région.
# - Le taux de retour par catégorie sur l'année sélectionnée. Les catégories sont classées du plus fort taux de retour au plus faible. 
# - Des filtres en haut de page permettent de sélectionner l'année (impact pour tous les visuels) et le Chiffre d'Affaires OU Marge (impact sur visuels 1 & 2)

# 5.3.3 Une page "Régions" qui met en avant :
# - l'évolution du CA OU marge par région sur l'année sélectionnée VS année précédente.
# - Une carte interactive qui montre la proportion de CA OU Marge entre l'année sélectionnée et année précédente.
# - NB : Les deux visuels sont liés : Si l'utilisateur filtre sur une région en cliquant sur le premier graphique, la carte zoom sur la région pour une meilleure visibilité sur les villes
# - Des filtres en haut de page permettent de sélectionner l'année et le Chiffre d'Affaires OU Marge 

# 5.3.4 Une parge "Marque" qui met en avant : 
# - l'évolution du CA OU marge pour le Top 15 des Marques sur l'année sélectionnée VS année précédente.
# - Une Heatmap qui permet de visualiser la répartition en part de marché (contribution de chaque Marque au Chiffre d'Affaires)
# - Le taux de retour par marque sur l'année sélectionnée. Les marques sont classées du plus fort taux de retour au plus faible. 
# - Des filtres en haut de page permettent de sélectionner l'année (impact pour tous les visuels) et le Chiffre d'Affaires OU Marge (impact sur visuels 1)

# 5.3.5 Une page "Autres KPIs" avec :
# - un treemap qui permet de visualiser la décomposition du panier moyen. L'utilisateur peut utiliser le visuel de façon interactive pour voir le panier moyen par région / catégorie / marque.
# - un graphique représentant la corrélation entre la Marge (en %) et le taux de retour par catégorie pour l'année sélectionnée et l'année précédente
# - Un filtre en haut de page permet de sélectionner l'année (impact sur tous les visuels) 



