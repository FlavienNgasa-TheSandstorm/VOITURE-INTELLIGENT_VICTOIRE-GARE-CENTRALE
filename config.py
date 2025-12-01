"""
Configuration du projet Agent Véhicule - VERSION KINSHASA RÉELLE
"""
from dataclasses import dataclass
from typing import Dict, Any
import json
import os

@dataclass
class Config:
    """Configuration principale de l'application - KINSHASA RÉELLE"""
    
    # Points de départ et d'arrivée - KINSHASA RÉELLE
    ETAT_INITIAL: str = "Place de la Victoire, Kalamu, Kinshasa, République Démocratique du Congo"
    ETAT_FINAL: str = "Gare Centrale, Gombe, Kinshasa, République Démocratique du Congo"
    
    # Paramètres OpenStreetMap
    NOMINATIM_URL: str = "https://nominatim.openstreetmap.org/search"
    NOMINATIM_DELAY: float = 1.0
    
    # Paramètres de l'agent
    VITESSE_MOYENNE_KMH: float = 25.0
    RAYON_RECHERCHE_KM: float = 2.0
    
    # Fichiers de données
    FICHIER_POINTS_INTERET: str = "data/points_interet.json"
    FICHIER_ARRETS_BUS: str = "data/arrets_bus.json"
    FICHIER_CACHE_GEOCODING: str = "data/cache_geocoding.json"
    
    # Paramètres de visualisation
    COULEUR_DEPART: str = "green"
    COULEUR_ARRIVEE: str = "red"
    COULEUR_INTERMEDIAIRE: str = "blue"
    COULEUR_ARRET_BUS: str = "orange"
    ZOOM_CARTE: int = 13
    
    # Ville et pays par défaut - KINSHASA
    VILLE_DEFAUT: str = "Kinshasa"
    PAYS_DEFAUT: str = "République Démocratique du Congo"
    
    # Coordonnées exactes réelles
    LATITUDE_VICTOIRE: float = -4.33787
    LONGITUDE_VICTOIRE: float = 15.30553
    LATITUDE_GARE: float = -4.31600
    LONGITUDE_GARE: float = 15.31300
    
    # Points d'intérêt par défaut pour Kinshasa
    POINTS_INTERET_KINSHASA: Dict = None
    
    def __post_init__(self):
        """Vérification et création des dossiers nécessaires"""
        self._creer_structure_dossiers()
        self._initialiser_points_interet()
    
    def _creer_structure_dossiers(self):
        """Crée la structure de dossiers si elle n'existe pas"""
        dossiers = [
            "data",
            "src/core",
            "src/services", 
            "src/visualization",
            "src/utils",
            "tests",
            "docs",
            "examples"
        ]
        
        for dossier in dossiers:
            os.makedirs(dossier, exist_ok=True)
    
    def _initialiser_points_interet(self):
        """Initialise les points d'intérêt réels pour Kinshasa"""
        self.POINTS_INTERET_KINSHASA = {
            "Place de la Victoire": {
                "nom": "Place de la Victoire",
                "latitude": -4.33787,    # Coordonnées exactes Kalamu
                "longitude": 15.30553,   # Coordonnées exactes Kalamu
                "type_point": "depart",
                "commune": "Kalamu"
            },
            "Gare Centrale": {
                "nom": "Gare Centrale",
                "latitude": -4.31600,    # Coordonnées exactes Gombe
                "longitude": 15.31300,   # Coordonnées exactes Gombe
                "type_point": "arrivee",
                "commune": "Gombe"
            },
            "Marché Central": {
                "nom": "Marché Central",
                "latitude": -4.32500,
                "longitude": 15.31000,
                "type_point": "intermediaire",
                "commune": "Gombe"
            },
            "Stade des Martyrs": {
                "nom": "Stade des Martyrs",
                "latitude": -4.33200,
                "longitude": 15.30800,
                "type_point": "intermediaire",
                "commune": "Lingwala"
            },
            "Université de Kinshasa": {
                "nom": "Université de Kinshasa",
                "latitude": -4.41500,
                "longitude": 15.30300,
                "type_point": "intermediaire",
                "commune": "Lemba"
            },
            "Hôpital Général de Kinshasa": {
                "nom": "Hôpital Général de Kinshasa",
                "latitude": -4.32200,
                "longitude": 15.31100,
                "type_point": "intermediaire",
                "commune": "Gombe"
            },
            "Palais du Peuple": {
                "nom": "Palais du Peuple",
                "latitude": -4.31800,
                "longitude": 15.31200,
                "type_point": "intermediaire",
                "commune": "Gombe"
            },
            "Tour de l'Échangeur": {
                "nom": "Tour de l'Échangeur",
                "latitude": -4.33500,
                "longitude": 15.30600,
                "type_point": "intermediaire",
                "commune": "Kalamu"
            },
            "Avenue de la Justice": {
                "nom": "Avenue de la Justice",
                "latitude": -4.32000,
                "longitude": 15.31100,
                "type_point": "intermediaire",
                "commune": "Gombe"
            },
            "Boulevard du 30 Juin": {
                "nom": "Boulevard du 30 Juin",
                "latitude": -4.32800,
                "longitude": 15.30900,
                "type_point": "intermediaire",
                "commune": "Gombe"
            },
            "Avenue des Aviateurs": {
                "nom": "Avenue des Aviateurs",
                "latitude": -4.32200,
                "longitude": 15.30800,
                "type_point": "intermediaire",
                "commune": "Gombe"
            },
            "Place du Marché": {
                "nom": "Place du Marché",
                "latitude": -4.32600,
                "longitude": 15.31000,
                "type_point": "intermediaire",
                "commune": "Gombe"
            },
            "Carrefour Forescom": {
                "nom": "Carrefour Forescom",
                "latitude": -4.33000,
                "longitude": 15.30700,
                "type_point": "intermediaire",
                "commune": "Gombe"
            },
            "Avenue de la Libération": {
                "nom": "Avenue de la Libération",
                "latitude": -4.31900,
                "longitude": 15.31200,
                "type_point": "intermediaire",
                "commune": "Gombe"
            },
            "Immeuble Sozacom": {
                "nom": "Immeuble Sozacom",
                "latitude": -4.31700,
                "longitude": 15.31300,
                "type_point": "intermediaire",
                "commune": "Gombe"
            }
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit la configuration en dictionnaire"""
        return {
            key: value for key, value in self.__dict__.items() 
            if not key.startswith('_')
        }
    
    def sauvegarder(self, fichier: str = "config.json"):
        """Sauvegarde la configuration dans un fichier"""
        with open(fichier, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def charger(cls, fichier: str = "config.json"):
        """Charge la configuration depuis un fichier"""
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls(**data)
        except FileNotFoundError:
            return cls()

# Instance globale de configuration
config = Config()