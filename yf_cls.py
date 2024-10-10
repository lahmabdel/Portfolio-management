import yfinance as yf
from datetime import datetime


class YahooFinanceExtractor:
    def __init__(self, ticker: str):
        """
        Initialise l'extracteur avec le ticker de l'action.
        
        :param ticker: Le symbole boursier de l'action (ex. "AAPL" pour Apple).
        """
        self.ticker = ticker
        self.data = None



    def get_prices(self,start_date: str, end_date: str):
        """
        Télécharge les données de prix pour l'action spécifiée sur une période donnée.

        :param start_date: La date de début au format 'YYYY-MM-DD'.
        :param end_date: La date de fin au format 'YYYY-MM-DD'.


        Récupère les prix de l'action sous forme de liste de tuples (date, prix de clôture).
        
        :return: Une liste de tuples (datetime, prix de clôture).
        """
        self.data = yf.download(self.ticker, start=start_date, end=end_date)
        if self.data is None:
            raise ValueError("Les données doivent être téléchargées d'abord en utilisant download_data().")

        # Convertir les dates en objets datetime et extraire les prix de clôture
        return [(datetime.strptime(date.strftime('%Y-%m-%d'), '%Y-%m-%d'), row['Close']) 
                for date, row in self.data.iterrows()]
    

    