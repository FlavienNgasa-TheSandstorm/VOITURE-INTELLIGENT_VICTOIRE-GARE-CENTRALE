"""
Service de calcul d'itinéraires - VERSION KINSHASA
"""
from typing import List, Optional, Dict, Any

# Imports absolus
from core.etat import Point, Trajet
from utils.config import config
from utils.helpers import calculer_distance_haversine, calculer_duree_estimee

class ServiceRouting:
    """
    Service responsable du calcul des itinéraires à Kinshasa
    """
    
    def __init__(self):
        print("🛣️  Service de routing initialisé pour Kinshasa")
    
    def calculer_itineraire_direct(self, points: List[Point]) -> List[Trajet]:
        """
        Calcule un itinéraire direct entre une série de points
        
        Args:
            points: Liste des points à relier
            
        Returns:
            Liste des trajets entre chaque paire de points
        """
        trajets = []
        
        for i in range(len(points) - 1):
            depart = points[i]
            arrivee = points[i + 1]
            
            trajet = self.calculer_trajet(depart, arrivee)
            if trajet:
                trajets.append(trajet)
        
        return trajets
    
    def calculer_trajet(self, depart: Point, arrivee: Point) -> Optional[Trajet]:
        """
        Calcule un trajet entre deux points
        
        Args:
            depart: Point de départ
            arrivee: Point d'arrivée
            
        Returns:
            Trajet calculé ou None en cas d'erreur
        """
        try:
            # Calcul de distance utilisant la formule Haversine
            distance_km = calculer_distance_haversine(depart, arrivee)
            
            # Calcul de durée basé sur la vitesse moyenne à Kinshasa
            duree_min = calculer_duree_estimee(distance_km, config.VITESSE_MOYENNE_KMH)
            
            # Création du trajet
            trajet = Trajet(
                depart=depart,
                arrivee=arrivee,
                distance_km=distance_km,
                duree_estimee_min=duree_min
            )
            
            return trajet
            
        except Exception as e:
            print(f"❌ Erreur calcul trajet {depart.nom} → {arrivee.nom}: {e}")
            return None
    
    def optimiser_ordre_points(self, points: List[Point]) -> List[Point]:
        """
        Optimise l'ordre des points pour minimiser la distance totale
        Algorithme simple: garde l'ordre mais peut être amélioré
        
        Args:
            points: Liste des points à ordonner
            
        Returns:
            Liste des points ordonnés
        """
        if len(points) <= 2:
            return points
        
        # Pour l'instant, on garde l'ordre donné
        # On pourrait implémenter un algorithme de voyageur de commerce simple
        print("🔧 Optimisation de l'ordre des points (ordre conservé)")
        return points
    
    def obtenir_temps_trajet_estime(self, distance_km: float, conditions_trafic: str = "normal") -> float:
        """
        Estime le temps de trajet en fonction des conditions
        
        Args:
            distance_km: Distance à parcourir
            conditions_trafic: "fluid", "normal", "dense"
            
        Returns:
            Temps estimé en minutes
        """
        facteurs_trafic = {
            "fluid": 0.8,      # -20%
            "normal": 1.0,     # temps normal
            "dense": 1.3       # +30%
        }
        
        facteur = facteurs_trafic.get(conditions_trafic, 1.0)
        temps_normal = calculer_duree_estimee(distance_km, config.VITESSE_MOYENNE_KMH)
        
        return temps_normal * facteur
