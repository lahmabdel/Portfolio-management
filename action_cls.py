import numpy as np
from datetime import datetime, timedelta

class Action:
    def __init__(self):
        # Liste de tuples (date, prix)
        self.prix_data = []
        self.stock_name=''
        
        
    def ajouter_donnees(self, date: datetime, prix: float):
        """Ajoute une nouvelle donnée de prix pour une date spécifique."""
        self.prix_data.append((date, prix))
        # Tri de la liste par date pour s'assurer qu'elle est toujours ordonnée
        self.prix_data.sort(key=lambda x: x[0])

    def calcul_rendement_journalier(self,period=252):
        """Calcule le rendement journalier pour chaque jour."""
        rendements = []
        for i in range(1, min(len(self.prix_data),period)):
            _, prix1 = self.prix_data[i - 1]
            _, prix2 = self.prix_data[i]
            rendement = (prix2 - prix1) / prix1
            rendements.append( rendement)
        return rendements

    def calcul_rendement_moyen(self,period=252):
        """Calcule le rendement moyen journalier sur les 'period' derniers jours.
        period: int"""
        rendements = self.calcul_rendement_journalier()
        derniers_rendements = rendements[-period:]  # Sélectionne les 252 derniers rendements
        moyenne = sum(derniers_rendements) / len(derniers_rendements)
        return moyenne

    def calcul_rendement_annualise(self,period=252):
        """Calcule le rendement moyen annualisé."""
        rendement_moyen = self.calcul_rendement_moyen(period)
        rendement_annualise = (1 + rendement_moyen) ** 252 - 1
        return rendement_annualise

    def calcul_volatilite(self,period=252):
        """Calcule la volatilité (écart-type) des rendements journaliers."""
        rendements_journaliers = self.calcul_rendement_journalier()
        rendements = rendements_journaliers[-period:] #ajouter la period
        return np.std(rendements)

    def calcul_volatilite_annualisee(self,period=252):
        """Calcule la volatilité annualisée à partir des rendements journaliers."""
        volatilite_journaliere = self.calcul_volatilite(period)
        return volatilite_journaliere * np.sqrt(252)

    def calcul_sharpe_ratio(self, taux_sans_risque=0.02,period=252):
        """Calcule le Sharpe Ratio à partir des rendements journaliers et d'un taux sans risque."""
        # Calcul du rendement moyen journalier
        rendement_moyen = self.calcul_rendement_moyen(period)

        # Calcul de la volatilité annualisée
        volatilite_ann = self.calcul_volatilite_annualisee(period)

        # Calcul du rendement moyen annualisé
        rendement_annualise = (1 + rendement_moyen) ** 252 - 1

        # Calcul du Sharpe Ratio
        sharpe_ratio = (rendement_annualise - taux_sans_risque) / volatilite_ann
        return sharpe_ratio
    
    def calcul_moving_average(self, period: int):
        """
        Calcule la moyenne mobile (Moving Average) sur une période donnée.
        
        :param periode: Nombre de jours pour la période de la moyenne mobile.
        :return: Liste de tuples (date, moving_average)
        """
        if len(self.prix_data) < period:
            raise ValueError("Pas assez de données pour calculer la moyenne mobile sur cette période.")

        moving_averages = []
        # Parcourir la liste de prix pour calculer la moyenne mobile
        for i in range(period - 1, len(self.prix_data)):
            # Récupérer les prix pour la fenêtre de la période spécifiée
            window = [prix for date, prix in self.prix_data[i - period + 1:i + 1]]
            # Calcul de la moyenne pour cette fenêtre
            moving_avg = sum(window) / period
            # Ajouter le résultat à la liste (date courante, moving average)
            moving_averages.append((self.prix_data[i][0], moving_avg))
        
        return moving_averages

