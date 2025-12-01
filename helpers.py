"""
Fonctions utilitaires pour le projet - VERSION KINSHASA
"""
import math
from typing import List, Tuple

# Import absolu
from core.etat import Point

def calculer_distance_haversine(point1: Point, point2: Point) -> float:
    """
    Calcule la distance en kilomètres entre deux points
    en utilisant la formule Haversine
    
    Args:
        point1: Premier point
        point2: Deuxième point
        
    Returns:
        Distance en kilomètres
    """
    R = 6371  # Rayon de la Terre en km
    
    lat1_rad = math.radians(point1.latitude)
    lat2_rad = math.radians(point2.latitude)
    delta_lat = math.radians(point2.latitude - point1.latitude)
    delta_lon = math.radians(point2.longitude - point1.longitude)
    
    a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lon/2) * math.sin(delta_lon/2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def calculer_duree_estimee(distance_km: float, vitesse_moyenne_kmh: float = 25.0) -> float:
    """
    Calcule la durée estimée en minutes pour parcourir une distance
    
    Args:
        distance_km: Distance à parcourir en km
        vitesse_moyenne_kmh: Vitesse moyenne en km/h (25 pour Kinshasa)
        
    Returns:
        Durée estimée en minutes
    """
    return (distance_km / vitesse_moyenne_kmh) * 60

def generer_points_intermediaires(depart: Point, arrivee: Point, nb_points: int = 3) -> List[Point]:
    """
    Génère des points intermédiaires le long d'une ligne droite
    avec de légères variations pour simuler un trajet réaliste
    
    Args:
        depart: Point de départ
        arrivee: Point d'arrivée
        nb_points: Nombre de points intermédiaires à générer
        
    Returns:
        Liste des points intermédiaires
    """
    points = []
    
    for i in range(1, nb_points + 1):
        ratio = i / (nb_points + 1)
        
        # Interpolation linéaire
        lat = depart.latitude + (arrivee.latitude - depart.latitude) * ratio
        lon = depart.longitude + (arrivee.longitude - depart.longitude) * ratio
        
        # Ajouter une variation sinusoïdale pour simuler des routes
        variation_lat = math.sin(ratio * math.pi) * 0.002
        variation_lon = math.cos(ratio * math.pi) * 0.002
        
        point_intermediaire = Point(
            nom=f"Étape {i}",
            latitude=lat + variation_lat,
            longitude=lon + variation_lon,
            type_point="intermediaire"
        )
        points.append(point_intermediaire)
    
    return points

def formater_duree(minutes: float) -> str:
    """
    Formate une durée en minutes en chaîne lisible
    
    Args:
        minutes: Durée en minutes
        
    Returns:
        Chaîne formatée (ex: "2h 15min")
    """
    if minutes < 60:
        return f"{int(minutes)}min"
    else:
        heures = int(minutes // 60)
        mins_restantes = int(minutes % 60)
        if mins_restantes > 0:
            return f"{heures}h {mins_restantes}min"
        else:
            return f"{heures}h"

def formater_distance(km: float) -> str:
    """
    Formate une distance en chaîne lisible
    
    Args:
        km: Distance en kilomètres
        
    Returns:
        Chaîne formatée (ex: "5.2 km")
    """
    if km < 1:
        return f"{int(km * 1000)}m"
    else:
        return f"{km:.1f} km"

def calculer_barycentre(points: List[Point]) -> Tuple[float, float]:
    """
    Calcule le barycentre d'une liste de points
    
    Args:
        points: Liste des points
        
    Returns:
        Tuple (latitude_moyenne, longitude_moyenne)
    """
    if not points:
        return (0, 0)
    
    somme_lat = sum(point.latitude for point in points)
    somme_lon = sum(point.longitude for point in points)
    
    return (somme_lat / len(points), somme_lon / len(points))

def verifier_points_proches(point1: Point, point2: Point, seuil_km: float = 0.1) -> bool:
    """
    Vérifie si deux points sont proches l'un de l'autre
    
    Args:
        point1: Premier point
        point2: Deuxième point
        seuil_km: Seuil de proximité en km
        
    Returns:
        True si les points sont proches, False sinon
    """
    distance = calculer_distance_haversine(point1, point2)
    return distance <= seuil_km
