"""
Système de décision multi-routes pour l'Agent Véhicule - VERSION KINSHASA RÉELLE
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple
import random
import math
from core.etat import Point

@dataclass
class RouteAlternative:
    """Représente une alternative de route"""
    nom: str
    points: List[Point]
    caracteristiques: Dict[str, float] = field(default_factory=dict)
    
    def __str__(self):
        return f"{self.nom} ({len(self.points)} points)"

class DecisionMaker:
    """
    Prend des décisions intelligentes sur les itinéraires
    """
    
    def __init__(self):
        self.routes_predefinies = {}
        self._initialiser_routes_kinshasa()
    
    def _initialiser_routes_kinshasa(self):
        """Initialise les routes prédéfinies pour Kinshasa avec points réels"""
        self.routes_predefinies = {
            "route_principale": {
                "nom": "Route Principale - Boulevard du 30 Juin",
                "points_cles": [
                    "Place de la Victoire", 
                    "Tour de l'Échangeur",
                    "Boulevard du 30 Juin", 
                    "Avenue de la Justice",
                    "Palais du Peuple", 
                    "Gare Centrale"
                ],
                "poids": {"temps": 0.8, "cout": 0.6, "securite": 0.7, "confort": 0.8}
            },
            "route_secondaire": {
                "nom": "Route Secondaire - Avenue des Aviateurs",
                "points_cles": [
                    "Place de la Victoire",
                    "Carrefour Forescom",
                    "Avenue des Aviateurs", 
                    "Place du Marché",
                    "Marché Central",
                    "Gare Centrale"
                ],
                "poids": {"temps": 0.6, "cout": 0.8, "securite": 0.8, "confort": 0.6}
            },
            "route_scenique": {
                "nom": "Route Scénique - Centre Ville",
                "points_cles": [
                    "Place de la Victoire",
                    "Stade des Martyrs",
                    "Avenue de la Libération",
                    "Hôpital Général de Kinshasa", 
                    "Immeuble Sozacom",
                    "Gare Centrale"
                ],
                "poids": {"temps": 0.4, "cout": 0.7, "securite": 0.9, "confort": 0.9}
            },
            "route_rapide": {
                "nom": "Route Rapide - Voie Express",
                "points_cles": [
                    "Place de la Victoire",
                    "Boulevard du 30 Juin", 
                    "Avenue de la Justice",
                    "Avenue des Aviateurs",
                    "Palais du Peuple",
                    "Gare Centrale"
                ],
                "poids": {"temps": 0.9, "cout": 0.5, "securite": 0.6, "confort": 0.7}
            },
            "route_economique": {
                "nom": "Route Économique - Itinéraire Court",
                "points_cles": [
                    "Place de la Victoire",
                    "Tour de l'Échangeur", 
                    "Avenue de la Libération",
                    "Hôpital Général de Kinshasa",
                    "Marché Central",
                    "Gare Centrale"
                ],
                "poids": {"temps": 0.5, "cout": 0.9, "securite": 0.7, "confort": 0.5}
            }
        }
    
    def definir_strategie(self, strategie: str) -> Dict[str, float]:
        """
        Définit les poids de décision selon la stratégie
        
        Args:
            strategie: "rapide", "economique", "securise", "confort", "equilibre"
            
        Returns:
            Dictionnaire des poids pour chaque critère
        """
        strategies = {
            "rapide": {"temps": 0.5, "cout": 0.2, "securite": 0.15, "confort": 0.15},
            "economique": {"temps": 0.2, "cout": 0.5, "securite": 0.15, "confort": 0.15},
            "securise": {"temps": 0.15, "cout": 0.2, "securite": 0.5, "confort": 0.15},
            "confort": {"temps": 0.15, "cout": 0.15, "securite": 0.2, "confort": 0.5},
            "equilibre": {"temps": 0.25, "cout": 0.25, "securite": 0.25, "confort": 0.25}
        }
        
        return strategies.get(strategie, strategies["rapide"])
    
    def generer_routes_alternatives(self, depart: Point, arrivee: Point) -> List[RouteAlternative]:
        """
        Génère plusieurs routes alternatives entre départ et arrivée
        
        Args:
            depart: Point de départ
            arrivee: Point d'arrivée
            
        Returns:
            Liste des routes alternatives
        """
        routes = []
        
        for route_id, route_info in self.routes_predefinies.items():
            # Créer les points pour cette route en utilisant les coordonnées réelles
            points_route = [depart]  # Commence par le départ
            
            # Ajouter les points intermédiaires avec coordonnées réelles
            for point_nom in route_info["points_cles"][1:-1]:  # Exclure départ et arrivée
                point_intermediaire = self._creer_point_intermediaire(point_nom, depart, arrivee)
                points_route.append(point_intermediaire)
            
            # Terminer par l'arrivée
            points_route.append(arrivee)
            
            # Calculer les caractéristiques de la route
            caracteristiques = self._calculer_caracteristiques_route(
                points_route, route_info["poids"]
            )
            
            # Créer la route alternative
            route = RouteAlternative(
                nom=route_info["nom"],
                points=points_route,
                caracteristiques=caracteristiques
            )
            
            routes.append(route)
        
        return routes
    
    def _creer_point_intermediaire(self, nom_point: str, depart: Point, arrivee: Point) -> Point:
        """Crée un point intermédiaire avec coordonnées réalistes"""
        # Coordonnées prédéfinies pour les points connus de Kinshasa
        points_coordonnees = {
            "Tour de l'Échangeur": (-4.33500, 15.30600),
            "Boulevard du 30 Juin": (-4.32800, 15.30900),
            "Avenue de la Justice": (-4.32000, 15.31100),
            "Palais du Peuple": (-4.31800, 15.31200),
            "Carrefour Forescom": (-4.33000, 15.30700),
            "Avenue des Aviateurs": (-4.32200, 15.30800),
            "Place du Marché": (-4.32600, 15.31000),
            "Marché Central": (-4.32500, 15.31000),
            "Stade des Martyrs": (-4.33200, 15.30800),
            "Avenue de la Libération": (-4.31900, 15.31200),
            "Hôpital Général de Kinshasa": (-4.32200, 15.31100),
            "Immeuble Sozacom": (-4.31700, 15.31300)
        }
        
        if nom_point in points_coordonnees:
            lat, lon = points_coordonnees[nom_point]
            return Point(nom_point, lat, lon, "intermediaire")
        else:
            # Point non prédéfini, générer aléatoirement
            return Point(
                nom_point,
                depart.latitude + (arrivee.latitude - depart.latitude) * random.uniform(0.2, 0.8),
                depart.longitude + (arrivee.longitude - depart.longitude) * random.uniform(0.2, 0.8),
                "intermediaire"
            )
    
    def _calculer_caracteristiques_route(self, points: List[Point], poids_base: Dict[str, float]) -> Dict[str, float]:
        """
        Calcule les caractéristiques d'une route en USD
        """
        # Calculer la distance totale
        distance_km = self._calculer_distance_totale(points)
        
        # Calculer le temps estimé (25 km/h moyenne à Kinshasa)
        temps_estime_min = (distance_km / 25) * 60
        
        # Calculer le coût en essence en USD (environ 1.5 USD/litre, consommation 7L/100km)
        cout_essence_usd = distance_km * 0.07 * 1.5  # 7L/100km * 1.5 USD/L
        
        # Générer des caractéristiques basées sur les poids
        return {
            "distance_km": round(distance_km, 2),
            "temps_estime_min": round(temps_estime_min, 2),
            "cout_essence_usd": round(cout_essence_usd, 2),
            "niveau_embouteillage": round(random.uniform(0.3, 0.9) * poids_base["temps"], 2),
            "niveau_securite": round(random.uniform(0.6, 0.95) * poids_base["securite"], 2),
            "confort_route": round(random.uniform(0.5, 0.9) * poids_base["confort"], 2),
            "score_global": round(sum(poids_base.values()) / len(poids_base), 2)
        }
    
    def _calculer_distance_totale(self, points: List[Point]) -> float:
        """Calcule la distance totale d'une route en km"""
        if len(points) < 2:
            return 0.0
        
        distance_totale = 0.0
        for i in range(len(points) - 1):
            # Utiliser la formule Haversine pour une distance précise
            distance_segment = self._calculer_distance_haversine(points[i], points[i+1])
            distance_totale += distance_segment
        
        return distance_totale
    
    def _calculer_distance_haversine(self, point1: Point, point2: Point) -> float:
        """Calcule la distance entre deux points avec la formule Haversine"""
        R = 6371  # Rayon de la Terre en km
        
        lat1 = math.radians(point1.latitude)
        lon1 = math.radians(point1.longitude)
        lat2 = math.radians(point2.latitude)
        lon2 = math.radians(point2.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def choisir_meilleure_route(self, routes: List[RouteAlternative], poids_strategie: Dict[str, float]) -> Tuple[RouteAlternative, Dict[str, Any]]:
        """
        Choisit la meilleure route selon la stratégie
        """
        if not routes:
            raise ValueError("Aucune route disponible pour l'analyse")
        
        analyse = {}
        meilleure_route = None
        meilleur_score = -1
        
        for route in routes:
            # Calculer le score pondéré selon la stratégie
            score = self._calculer_score_route(route, poids_strategie)
            
            # Stocker l'analyse
            analyse[route.nom] = {
                "score": round(score, 3),
                "caracteristiques": route.caracteristiques,
                "nombre_points": len(route.points)
            }
            
            # Mettre à jour la meilleure route
            if score > meilleur_score:
                meilleur_score = score
                meilleure_route = route
        
        return meilleure_route, analyse
    
    def _calculer_score_route(self, route: RouteAlternative, poids_strategie: Dict[str, float]) -> float:
        """
        Calcule le score d'une route selon la stratégie
        """
        carac = route.caracteristiques
        
        # Normaliser les caractéristiques (inverser pour l'embouteillage et coût)
        score_temps = (1 - carac["niveau_embouteillage"]) * poids_strategie["temps"]
        score_cout = (1 - carac["cout_essence_usd"] / 5) * poids_strategie["cout"]  # Normaliser le coût (max 5 USD)
        score_securite = carac["niveau_securite"] * poids_strategie["securite"]
        score_confort = carac["confort_route"] * poids_strategie["confort"]
        
        return score_temps + score_cout + score_securite + score_confort