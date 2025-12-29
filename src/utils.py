import pandas as pd


#création d'une fonction pour convertir les formats en date
def convert_dates(df):
    """
    Convertit les colonnes de dates en datetime.
    Colonnes converties : 'item_created_at', 'order_created_at', 'shipped_at','delivered_at'
    """
    date_cols = ['item_created_at', 'order_created_at', 'shipped_at',"delivered_at"]
    
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
    
    return df


#création d'une fonction générique pour le KPI Chiffre d'Affaire -> permet d'avoir une seule fonction déclinable par une ou plusieurs dimensions
#.reset_index() permet de transformer l'index en colonne, ce qui est plus lisible
#name="chiffre d'affaire" permet d'avoir un titre plus compréhensible que "sale_price"
def kpi_CA(df,dimensions=None):
    if dimensions is None:
        return df['sale_price'].sum()
    return (df.groupby(dimensions)['sale_price'].sum().reset_index(name='chiffre_affaires'))


#Création d'une fonction gérérique pour le KPI Marge Brute -> permet d'avoir une seule fonction déclinable par une ou plusieurs dimensions
#df_WIP : dataframe intermediarei(Work In Progress) permettant d'ajouter une colonne marge (plus sûr que de modifier directement dans df)
#.reset_index() permet de transformer l'index en colonne, ce qui est plus lisible
#name="marge" permet d'avoir un titre plus compréhensible
def kpi_Margin(df,dimensions=None):
    df_WIP=df.assign(margin=df["sale_price"]-df["cost"])
    if dimensions is None:
        return df_WIP['margin'].sum()
    return (df_WIP.groupby(dimensions)['margin'].sum().reset_index(name='marge'))


#Création d'une fonction générique pour le Panier Moyen -> permet d'avoir une seule fonction déclinable par une ou plusieurs dimensions
#Hypothèses :
#sale_price = revenu par ligne
#order_id = identifiant de commande
#une commande peut avoir plusieurs lignes
#on exclut les commandes dont le CA est inférieur à zéro
#une commande peut avoir plusieurs lignes
#on exclut les commandes dont le CA total ≤ 0

def kpi_panier_moyen(df, dimensions=None):
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
    
    # Cas 2 : panier moyen décliné par dimensions
    df_cmd = (df.groupby(dimensions + ['order_id'])['sale_price'].sum().reset_index())

    df_cmd = df_cmd[df_cmd['sale_price'] > 0]

    result = (df_cmd.groupby(dimensions)['sale_price'].mean().reset_index(name='panier_moyen'))
    return result