import pandas as pd
from datetime import datetime

def dataframe_to_list_of_tuples(df: pd.DataFrame):
    """
    Transforme un DataFrame contenant des colonnes 'date' et 'prix' 
    en une liste de tuples (date, prix).
    
    :param df: DataFrame avec des colonnes 'date' et 'prix'
    :return: Liste de tuples (date, prix)
    """
    # S'assurer que la colonne 'date' est bien de type datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Convertir en liste de tuples
    liste_tuples = list(df.itertuples(index=False, name=None))
    return liste_tuples


