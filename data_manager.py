"""
Gestion des données locales et points d'intérêt - VERSION KINSHASA
"""
import json
import os
from typing import Dict, List, Optional

# Imports absolus
from core.etat import Point
from utils.config import config

class GestionnaireDonnees:
    """
    Gère le chargement et la sauvegarde des données locales - KINSHASA
    """
    
    def __init__(self):
        self.points_interet = self._charger_points_interet()
        self.arrets_bus = self._charger_arrets_bus()
    
    def _charger_points_interet(self) -> Dict[str, Point]:
        """Charge les points d'intérêt depuis le fichier"""
        try:
            if os.path.exists(config.FICHIER_POINTS_INTERET):
                with open(config.FICHIER_POINTS_INTERET, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                points_charges = {}
                for nom, point_data in data.items():
                    points_charges[nom] = Point.from_dict(point_data)
                return points_charges
            else:
                # Créer le fichier avec les points par défaut de Kinshasa
                self._sauvegarder_points_interet(config.POINTS_INTERET_KINSHASA)
                return {nom: Point.from_dict(point_data) for nom, point_data in config.POINTS_INTERET_KINSHASA.items()}
                
        except Exception as e:
            print(f"⚠️  Erreur chargement points intérêt: {e}")
            # Retourner les points par défaut de Kinshasa
            return {nom: Point.from_dict(point_data) for nom, point_data in config.POINTS_INTERET_KINSHASA.items()}
    
    def _sauvegarder_points_interet(self, points: Dict[str, Point]):
        """Sauvegarde les points d'intérêt dans le fichier"""
        try:
            data = {nom: point.to_dict() for nom, point in points.items()}
            with open(config.FICHIER_POINTS_INTERET, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Erreur sauvegarde points intérêt: {e}")
    
    def _charger_arrets_bus(self) -> Dict[str, Point]:
        """Charge les arrêts de bus depuis le fichier"""
        arrets_par_defaut = {
            "Arrêt Victoire": Point("Arrêt Victoire", -4.4420, 15.2665, "arret_bus"),
            "Arrêt Gare": Point("Arrêt Gare", -4.4405, 15.2695, "arret_bus"),
            "Arrêt Marché": Point("Arrêt Marché", -4.4435, 15.2645, "arret_bus"),
            "Arrêt Stade": Point("Arrêt Stade", -4.4475, 15.2585, "arret_bus"),
            "Arrêt Université": Point("Arrêt Université", -4.4210, 15.3040, "arret_bus"),
            "Arrêt Hôpital": Point("Arrêt Hôpital", -4.4355, 15.2755, "arret_bus")
        }
        
        try:
            if os.path.exists(config.FICHIER_ARRETS_BUS):
                with open(config.FICHIER_ARRETS_BUS, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                arrets_charges = {}
                for nom, point_data in data.items():
                    arrets_charges[nom] = Point.from_dict(point_data)
                return arrets_charges
            else:
                # Créer le fichier avec les arrêts par défaut
                self._sauvegarder_arrets_bus(arrets_par_defaut)
                return arrets_par_defaut
                
        except Exception as e:
            print(f"⚠️  Erreur chargement arrêts bus: {e}")
            return arrets_par_defaut
    
    def _sauvegarder_arrets_bus(self, arrets: Dict[str, Point]):
        """Sauvegarde les arrêts de bus dans le fichier"""
        try:
            data = {nom: point.to_dict() for nom, point in arrets.items()}
            with open(config.FICHIER_ARRETS_BUS, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Erreur sauvegarde arrêts bus: {e}")
    
    def obtenir_points_interet(self) -> List[Point]:
        """Retourne la liste des points d'intérêt"""
        return list(self.points_interet.values())
    
    def obtenir_arrets_bus(self) -> List[Point]:
        """Retourne la liste des arrêts de bus"""
        return list(self.arrets_bus.values())
    
    def ajouter_point_interet(self, nom: str, point: Point):
        """Ajoute un nouveau point d'intérêt"""
        self.points_interet[nom] = point
        self._sauvegarder_points_interet(self.points_interet)
    
    def ajouter_arret_bus(self, nom: str, point: Point):
        """Ajoute un nouvel arrêt de bus"""
        self.arrets_bus[nom] = point
        self._sauvegarder_arrets_bus(self.arrets_bus)
    
    def rechercher_point_par_nom(self, nom: str) -> Optional[Point]:
        """Recherche un point par son nom"""
        # Chercher dans les points d'intérêt
        for point_nom, point in self.points_interet.items():
            if nom.lower() in point_nom.lower():
                return point
        
        # Chercher dans les arrêts de bus
        for point_nom, point in self.arrets_bus.items():
            if nom.lower() in point_nom.lower():
                return point
        
        return None
    
    def obtenir_points_pour_itineraire(self) -> List[Point]:
        """
        Retourne une sélection de points pour créer un itinéraire intéressant
        """
        points_selectionnes = []
        
        # Points obligatoires
        depart = self.points_interet.get("Rond Point Victoire")
        arrivee = self.points_interet.get("Gare Centrale")
        
        if depart:
            points_selectionnes.append(depart)
        
        # Ajouter quelques points intermédiaires intéressants
        points_intermediaires = [
            "Marché Central",
            "Place de la Gare", 
            "Hôpital Général",
            "Palais du Peuple"
        ]
        
        for nom in points_intermediaires:
            point = self.points_interet.get(nom)
            if point:
                points_selectionnes.append(point)
        
        if arrivee:
            points_selectionnes.append(arrivee)
        
        return points_selectionnes

# Instance globale du gestionnaire de données
gestionnaire_donnees = GestionnaireDonnees()
