import action_cls
import numpy as np
class WeightSumExceededError(Exception):
    """Exception levée lorsque la somme des poids dépasse 1."""
    pass

class Portefeuille:
    def __init__(self):
        # Liste de tuples (Quantity, action), où action est un objet de la classe Action
        Quantity=0
        action=action_cls.Action()
        self.actions = [(Quantity,action)]
        self.montant_investi = 100


    def afficher_portefeuille(self):
        port=[]
        for i in self.actions:
            port.append((i[0],i[1].stock_name))
        return port
    
   
    def calculer_valeur_portefeuille(self):
        """
        Calcule la valeur totale actuelle du portefeuille, en fonction des actions et de leurs prix actuels.

        :return: La valeur totale du portefeuille.
        """
        valeur_totale = 0.0
        for  parts_possedes,action in self.actions:
            prix_actuel = action.prix_data[-1][1]  # Le dernier prix de l'action
            valeur_totale += parts_possedes * prix_actuel
        return valeur_totale


    def calculer_weights(self):
        weights=[]
        valeur_totale= self.calculer_valeur_portefeuille()
        
        sum_weights=0
        for  quantity,action in self.actions:
            prix_actuel = action.prix_data[-1][1]
            weight= quantity * prix_actuel/self.montant_investi

            weights.append([weight,action])
            sum_weights+=weight

        if sum_weights > 1.0001:  # Tolérance de 0.0001 pour les erreurs d'arrondi
                raise WeightSumExceededError(f"La somme des poids ({sum_weights}) dépasse 1.")
        return weights
        
        
    def calculer_rendement_journalier_portefeuille(self,period=252):
        """
        Calcule le rendement journalier moyen pondéré du portefeuille.
        
        :return: Le rendement journalier moyen pondéré du portefeuille.
        """
        
        rendement_journalier_portefeuille = []
        for i in range(0,len(self.actions)):
            for weight, action in self.calculer_weights():

                rendements_journaliers_action = weight *action.calcul_rendement_journalier(period)
            
                rendement_journalier_portefeuille = [a + b for a, b in zip(rendement_journalier_portefeuille, rendements_journaliers_action)]

        return rendement_journalier_portefeuille

    
    
    def calculer_rendement_moyen_portefeuille(self,period=252):
        """
        Calcule le rendement moyen pondéré du portefeuille sur les 252 derniers jours.
        
        :return: Le rendement moyen pondéré du portefeuille.
        """
        rendement_moyen_portefeuille = 0
        for weight, action in self.calculer_weights():
            rendement_moyen_action = action.calcul_rendement_moyen(period)
            rendement_moyen_portefeuille += weight * rendement_moyen_action
        return rendement_moyen_portefeuille

    
    
    def calculer_rendement_annualise_portefeuille(self,period=252):
        """
        Calcule le rendement annualisé moyen pondéré du portefeuille.
        
        :return: Le rendement annualisé moyen pondéré du portefeuille.
        """
        rendement_moyen_portefeuille = self.calculer_rendement_moyen_portefeuille(period)
        rendement_annualise_portefeuille = (1 + rendement_moyen_portefeuille) ** 252 - 1
        return rendement_annualise_portefeuille
    
    
    def calculer_volatilite_portefeuille(self,period =252):
        """
        Calcule la volatilité du portefeuille en utilisant les poids des actifs, leurs volatilities et la matrice de corrélation.
        
        :param correlation_matrix: La matrice de corrélation entre les actifs.
        :return: La volatilité du portefeuille.
        """
        # Extraire les poids des actions
        weights = np.array([w[0] for w in self.calculer_weights()])
        
        # Convertir la matrice de corrélation en numpy array
        rendement_data = np.array([action[1].calcul_rendement_journalier()[-period:] for action in self.actions])
        covariance_matrix = np.cov(rendement_data)
        
        portfolio_variance=np.dot(weights.T, np.dot(covariance_matrix, weights))
        # Calcul de la volatilité du portefeuille (écart type)
        portfolio_volatility = np.sqrt(portfolio_variance)
        
        return portfolio_volatility



    def calculer_volatilite_annualisee_portefeuille(self,period=252):
        """
        Calcule la volatilité annualisée pondérée du portefeuille.
        
        :return: La volatilité annualisée pondérée du portefeuille.
        """
    
        return self.calculer_volatilite_portefeuille(period)* np.sqrt(252)
    

    def calculer_sharpe_ratio_portefeuille(self, taux_sans_risque=0.02,period=252):
        """
        Calcule le Sharpe Ratio du portefeuille pondéré par les poids des actions.
        
        :param taux_sans_risque: Le taux sans risque (par défaut 2% ou 0.02)
        :return: Le Sharpe Ratio pondéré du portefeuille.
        """
        volatilite_annualisee_portefeuille = self.calculer_volatilite_annualisee_portefeuille(period)
        
        rendement_annualise_portefeuille = self.calculer_rendement_annualise_portefeuille()
        sharpe_ratio_portefeuille = (rendement_annualise_portefeuille - taux_sans_risque) / volatilite_annualisee_portefeuille
        
        return sharpe_ratio_portefeuille



