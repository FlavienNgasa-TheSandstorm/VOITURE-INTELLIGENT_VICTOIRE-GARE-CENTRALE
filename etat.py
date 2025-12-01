"""
Gestion des états de l'Agent Véhicule - VERSION KINSHASA
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import time

class StatutAgent(Enum):
    """Statuts possibles de l'agent"""
    INACTIF = "inactif"
    EN_ATTENTE = "en_attente" 
    EN_MOUVEMENT = "en_mouvement"
    ARRIVE = "arrivé"
    ERREUR = "erreur"

@dataclass
class Point:
    """Représente un point géographique"""
    nom: str
    latitude: float
    longitude: float
    type_point: str = "inconnu"  # "depart", "arrivee", "arret", "intermediaire"
    
    def to_dict(self) -> Dict:
        """Convertit le point en dictionnaire"""
        return {
            "nom": self.nom,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "type_point": self.type_point
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Crée un point depuis un dictionnaire"""
        return cls(
            nom=data["nom"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            type_point=data.get("type_point", "inconnu")
        )

@dataclass
class Trajet:
    """Représente un trajet entre deux points"""
    depart: Point
    arrivee: Point
    distance_km: float
    duree_estimee_min: float
    points_intermediaires: List[Point] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convertit le trajet en dictionnaire"""
        return {
            "depart": self.depart.to_dict(),
            "arrivee": self.arrivee.to_dict(),
            "distance_km": self.distance_km,
            "duree_estimee_min": self.duree_estimee_min,
            "points_intermediaires": [p.to_dict() for p in self.points_intermediaires]
        }

class EtatAgent:
    """
    Gère l'état courant de l'agent véhicule
    """
    
    def __init__(self, etat_initial: str, etat_final: str):
        self.etat_actuel = etat_initial
        self.etat_final = etat_final
        self.statut = StatutAgent.INACTIF
        self.historique_etats: List[str] = [etat_initial]
        self.trajets_effectues: List[Trajet] = []
        self.position_actuelle: Optional[Point] = None
        self.temps_debut: Optional[float] = None
        self.temps_fin: Optional[float] = None
        
    def demarrer(self):
        """Démarre l'agent"""
        self.statut = StatutAgent.EN_ATTENTE
        self.temps_debut = time.time()
        print("🚗 Agent démarré - Kinshasa")
    
    def arreter(self):
        """Arrête l'agent"""
        self.statut = StatutAgent.ARRIVE
        self.temps_fin = time.time()
        print("🛑 Agent arrêté")
    
    def mettre_a_jour_position(self, point: Point):
        """Met à jour la position actuelle"""
        self.position_actuelle = point
        self.etat_actuel = point.nom
        self.historique_etats.append(point.nom)
    
    def ajouter_trajet(self, trajet: Trajet):
        """Ajoute un trajet à l'historique"""
        self.trajets_effectues.append(trajet)
        self.mettre_a_jour_position(trajet.arrivee)
    
    def obtenir_duree_totale(self) -> float:
        """Calcule la durée totale en minutes"""
        if self.temps_debut and self.temps_fin:
            return (self.temps_fin - self.temps_debut) / 60
        return 0.0
    
    def obtenir_distance_totale(self) -> float:
        """Calcule la distance totale parcourue"""
        return sum(trajet.distance_km for trajet in self.trajets_effectues)
    
    def obtenir_statistiques(self) -> Dict:
        """Retourne les statistiques de l'agent"""
        return {
            "etat_actuel": self.etat_actuel,
            "statut": self.statut.value,
            "nombre_trajets": len(self.trajets_effectues),
            "distance_totale_km": self.obtenir_distance_totale(),
            "duree_totale_min": self.obtenir_duree_totale(),
            "historique_points": len(self.historique_etats)
        }
    
    def est_arrive(self) -> bool:
        """Vérifie si l'agent est arrivé à destination"""
        return self.etat_actuel == self.etat_final
    
    def __str__(self) -> str:
        """Représentation textuelle de l'état"""
        stats = self.obtenir_statistiques()
        return (
            f"🤖 État Agent: {self.statut.value}\n"
            f"📍 Position: {self.etat_actuel}\n"
            f"🎯 Destination: {self.etat_final}\n"
            f"📏 Distance parcourue: {stats['distance_totale_km']:.2f} km\n"
            f"⏱️  Durée: {stats['duree_totale_min']:.1f} min"
        )
