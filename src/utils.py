import pandas as pd


#création d'une fonction pour convertir les formats en date
def convert_dates(df):
    """
    Convertit les colonnes de dates en datetime.
    Colonnes converties : 'item_created_at', 'order_created_at', 'shipped_at','delivered_at'
    Les valeurs non convertibles sont remplacées par NaT.

    Args :
        df : DataFrame
        DataFrame contenant les colonnes de dates à convertir. Seules les colonnes qui s'appellent 'item_created_at', 'order_created_at', 'shipped_at','delivered_at' seront converties.

    Returns :
        Le même dataframe avec les colonnes ci-dessous converties en date
        NB :La conversion est effectuée avec `errors='coerce'`, ce qui force les valeurs invalides ou manquantes à être remplacées par NaT.
    """
    date_cols = ['item_created_at', 'order_created_at', 'shipped_at',"delivered_at"]
    
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df


# CREATION DES KPI.
# Dans la création des fonctions KPI de Chiffre d'Affaire, Marge Brute et Panier Moyen, on ne met pas par défaut les statuts considérés comme "vente" (ie status "Complete") qui devront donc être ajoutés en dimension. 
# Cela permettra de faire aussi des analyses concernant les ventes futures (en particulier "Shipped" & "Processed" qui constituent des revenus à venir)

#création d'une fonction générique pour le KPI Chiffre d'Affaire -> permet d'avoir une seule fonction déclinable par une ou plusieurs dimensions

def kpi_CA(df,dimensions=None):
    """
    Calcule le chiffre d'affaires total ou par dimensions spécifiques.
    Si aucune dimension n'est fournie, la fonction retourne la somme totale de la colonne 'sale_price'. 
    Si une ou plusieurs dimensions sont spécifiées, le chiffre d'affaires est calculé par regroupement sur ces dimensions.
    
    Args :
        df : DataFrame
            DataFrame contenant au minimum la colonne 'sale_price' et éventuellement les colonnes utilisées comme dimensions.
        dimensions : str ou list[str], optionnel
            Nom de la colonne ou liste de colonnes sur lesquelles effectuer le regroupement pour calculer le chiffre d'affaires.
            Par défaut None.

    Returns : 
        float ou DataFrame
        - si Dimension est None  -> float : chiffre d'affaires total 
        - si Dimension est mentionnée (une ou plusieurs) -> DataFrame : chiffre d'affaires par dimension(s) avec une colonne 'chiffre_affaires'.
    
    Notes :
        .reset_index() permet de transformer l'index en colonne, ce qui est plus lisible
        name="chiffre d'affaire" permet d'avoir un titre plus compréhensible que "sale_price"

    """
    if dimensions is None:
        return df['sale_price'].sum()
    return (df.groupby(dimensions)['sale_price'].sum().reset_index(name='chiffre_affaires'))


#Création d'une fonction gérérique pour le KPI Marge Brute -> permet d'avoir une seule fonction déclinable par une ou plusieurs dimensions

def kpi_Margin(df,dimensions=None):
    """
    Calcule la marge totale ou la marge par dimensions spécifiques.

    La marge est calculée comme la différence entre le prix de vente ('sale_price') et le coût ('cost'). 
    Si aucune dimension n'est fournie, la fonction retourne la marge totale. 
    Sinon, la marge est calculée par regroupement sur les dimensions spécifiées.
    
    Args:
        df : Dataframe
            DataFrame contenant au minimum les colonnes 'sale_price' et 'cost', ainsi que les colonnes utilisées comme dimensions (optionnelles).
        dimensions : str ou list[str], optionnel
            Nom de la colonne ou liste de colonnes sur lesquelles effectuer le regroupement pour calculer la marge (par défaut -> None)

    Returns:
        float ou DataFrame
            - Si pas de dimensions (None)) -> float : marge totale 
            - Si dimensions existe (une ou plusieurs) -> DataFrame : marge par dimension(s) avec une colonne 'marge' 
    
    Notes : 
        .reset_index() permet de transformer l'index en colonne, ce qui est plus lisible
        name = "marge" permet d'avoir un titre plus compréhensible
        Df_WIP : dataframe intermediarei(Work In Progress) permettant d'ajouter une colonne marge (plus sûr que de modifier directement dans df)
    
    """
    df_WIP=df.assign(margin=df["sale_price"]-df["cost"])
    if dimensions is None:
        return df_WIP['margin'].sum()
    return (df_WIP.groupby(dimensions)['margin'].sum().reset_index(name='marge'))


#Création d'une fonction générique pour le Panier Moyen -> permet d'avoir une seule fonction déclinable par une ou plusieurs dimensions
#Hypothèses :
#sale_price = revenu par ligne
#order_id = identifiant de commande
#une commande peut avoir plusieurs lignes


def kpi_panier_moyen(df, dimensions=None):
    """
    Calcule le panier moyen (commande moyenne) global ou par dimensions.

    Le panier moyen correspond au chiffre d'affaires moyen par commande.
    Il est calculé à partir de la somme des 'sale_price' par 'order_id', en excluant les commandes dont le chiffre d'affaires est nul ou négatif.
    Si aucune dimension n'est fourniée, la fonction retourne le panier moyen global.
    Sinon, la fonction retourne le panier moyen par dimension(s).

    Args :
        df : DataFrame
            DataFrame contenant au minimum les colonnes 'order_id' et 'sale_price', ainsi que les colonnes utilisées comme dimensions (optionnelles)
        dimensions : list[str], optionnel
            Liste des colonnes sur lesquelles calculer le panier moyen.
            Par défaut None.

    Returns :
         float ou pandas.DataFrame
        - Si pas de dimensions (None)) -> float : panier moyen global
        - Si dimensions existe (une ou plusieurs) -> DataFrame : panier moyen par dimension(s) avec une colonne 'panier_moyen' 
   
    """
    # Cas 1 : panier moyen global
    if dimensions is None:
        # CA par commande
        ca_par_commande = (df.groupby('order_id')['sale_price'].sum())

        # Commandes valides
        ca_par_commande = ca_par_commande[ca_par_commande > 0]

        if len(ca_par_commande) == 0:
            return 0
        else:
            return ca_par_commande.mean()
    
    # Cas 2 : panier moyen (commande moyenne) par dimensions
    df_cmd = (df.groupby(dimensions + ['order_id'])['sale_price'].sum().reset_index())

    df_cmd = df_cmd[df_cmd['sale_price'] > 0]

    result = (df_cmd.groupby(dimensions)['sale_price'].mean().reset_index(name='panier_moyen'))
    return result


#Création de la fonction Taux de retour (part des lignes au statut Returned parmi les lignes vendues : ventes + retours).
# NB : nous avons au préalable vérifié dans le Notebook que les order_status et item_status sont parfaitement cohérents

def kpi_tx_retour(df,dimensions=None):
    """
    Calcule le taux de retour global ou par dimensions.

    Le taux de retour est défini comme le ratio :
    -> nombre d'items avec le statut 'Returned' divisé par le nombre total d'items ayant un statut 'Returned' ou 'Complete'.

    Avant le calcul, le DataFrame est nettoyé pour ne conserver que les lignes dont le statut est 'Returned' ou 'Complete'.

    Deux cas sont gérés :
    - Sans dimensions : retourne le taux de retour global.
    - Avec dimensions : retourne le taux de retour par dimension(s).

    Args :
         df : DataFrame
            DataFrame contenant au minimum la colonne 'item_status' ainsi que les colonnes utilisées comme dimensions (optionnelles)
        dimensions : str ou list[str], optionnel
            Nom de la colonne ou liste de colonnes sur lesquelles calculer le taux de retour.
            Par défaut None.

    Returns :
        float ou DataFrame
        - Si pas de dimensions (None)) -> float : taux de retour global (valeur comprise entre 0 et 1).
        - Si dimensions existe (une ou plusieurs) -> DataFrame : taux de retour par dimension(s) avec une colonne 'taux_retour'.

      Notes :
        - Seuls les statuts 'Returned' et 'Complete' sont pris en compte.
        - Les groupes sans valeur 'Returned' ou 'Complete' retournent un taux de retour égal à 0.
        - La fonction gère indifféremment une ou plusieurs dimensions  
    
    :param df: Description
    :param dimensions: Description
    """
    
    #Nettoyage : garder uniquement les ligne "Returned" & "Complete"
    df = df[df['item_status'].isin(['Returned', 'Complete'])]

    # Cas 1 : taux global (pas de dimensions) -> on divise simplement le total des lignes "Returned" par le nombre de lignes du df nettoyé (filtré sur Complete + Returned)
    if dimensions is None:
        nb_returned = (df['item_status'] == 'Returned').sum()
        nb_total = len(df)
        return nb_returned / nb_total if nb_total > 0 else 0

    # Cas 2 : taux par dimensions
    else:
        # On normalise le type de dimensions pour qu'on puisse utiliser une seule dimension (type string) ou plusieurs (donc dimension sera une liste). 
        # Pour pouvoir utiliser sans problème, on convertit d'office dimensions en liste (donc si c'est initialement string -> devient une liste d'une seule colonne)
        if isinstance(dimensions, str):
            dimensions = [dimensions]

        # Grouper par dimensions et calculer
        #df.groupby(dimensions) -> on regroupe df par la ou les colonnes mentionnées dans dimensions
        #['item_status'].value_counts() -> on compte combien de fois chaque item_status apparaît
        #unstack() -> permet de convertir la colonne "item_status" en plusieurs colonnes distinctes (ici une colonne pour "Retruned" + une colonne pour "Complete")
        #(fill_value=0) -> si on cherche à convertir une ligne manquante (par excemple: on a une ligne pour "Complete" mais rien pour "Returned" -> que mettre dana la colonne "Returned"?) -> on met zeo
        grouped = df.groupby(dimensions)['item_status'].value_counts().unstack(fill_value=0)

        # Calcul du taux
        #on a une nouvelle colonne "taux_retour" qui, pour chaque ligne, fait la division des colonnes : "Returned"/("Returned"+"Complete")
        #Mais avant on modifie les grouped["Returned]" et grouped["Complete"] -> si jamais on appelle une dimension qui n'a aucun item_status Complete ni Returned, alors on aura zéro.
        # c'est nécessaire en plus du unstack(fill_value=0) ci-dessous, qui permettait d'attribuer zéro si l'une OU l'autre (Complete OU Returned) était manquante
        grouped['Returned'] = grouped.get('Returned', 0)
        grouped['Complete'] = grouped.get('Complete', 0)
        grouped['taux_retour'] = grouped['Returned'] / (grouped['Returned'] + grouped['Complete'])

        # On garde juste les dimensions + taux
        #reset_index() permet de passer les dimensions en colonnes normales, alors que dans le dataframe grouped elles sont en index
        #dimensions + ['taux_retour']-> crée une liste des colonnes qu’on veut garder (on ne garde que les colonnes utiles pour le résultat final)

        return grouped.reset_index()[dimensions + ['taux_retour']]



#Creation de la fonction Taux de réachat (part des clients ayant ≥ 2 commandes complètes sur une année).
# Hypothèse : L'année doit obligatoirement être mentionnée pour appeler la fonction 
# df : DataFrame avec colonnes 'user_id', 'order_id', 'order_status', 'order_date'
# Pour l'année : on part du principe qu'on filtre sur la date de livraison ("delivered at")

def kpi_tx_reachat(df, annee):
    """
    Calcule le taux de ré-achat des clients sur une année donnée.
    Le taux de ré-achat correspond à la proportion de clients ayant passé au moins deux commandes complètes (statut "Complete") au cours de l'année spécifiée, par rapport au nombre total de clients ayant passé au moins une commande complète sur cette même période.
    Le calcul est effectué uniquement sur les commandes dont le statut est 'Complete' et dont la date de livraison correspond à l'année fournie.

    Args :
        df : DataFrame
            DataFrame contenant au minimum les colonnes 'order_status', 'delivered_at', 'user_id' et 'order_id'.
        annee : int
            Année sur laquelle calculer le taux de ré-achat (ex. 2023).

    Returns :
        float -> taux de réachat (valeur comprise entre 0 et 1)
    
    Notes: 
        - Un client est considéré comme ré-acheteur s'il a passé au moins 2 commandes distinctes sur l'année.
        - Si aucun client n'est présent sur la période, la fonction retourne 0.
    
    """
    # Filtrer les commandes complètes
    df_complete = df[df['order_status'] == 'Complete'].copy()
    #Filtrer sur l'année 
    df_complete = df_complete[df_complete['delivered_at'].dt.year == annee]
    # Compter le nombre de commandes par client
    commandes_par_client = df_complete.groupby('user_id')['order_id'].nunique()
    # Clients avec ≥2 commandes
    clients_reacheteurs = commandes_par_client[commandes_par_client >= 2].count()
    # Nombre total de clients uniques sur la période
    total_clients = commandes_par_client.count()
    # Taux de ré-achat
    tx_reachat = clients_reacheteurs / total_clients if total_clients > 0 else 0
    return tx_reachat


# Création de la fonction curreny pour optimiser les graphiques
# La fonction currency permet de modifier l'affichage des valeurs sur l'axis y
def currency(x, pos):
    """
    Format currency values in euros as K€ or €.

    Parameters
    ----------
    x : float
        Currency value in euros.
    pos : int
        Tick position (unused).

    Returns
    -------
    str
        Formatted currency string.
    """
    if x >= 1e3:
        pos = '{:1.1f}K€'.format(x /1000)
    else:
        pos = '{:1.0f}€'.format(x)
    return pos