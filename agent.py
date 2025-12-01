"""
Classe principale de l'Agent Véhicule - VERSION KINSHASA AVEC DÉCISION MULTI-ROUTES
"""
import time
from typing import List, Optional, Dict, Any

# Imports absolus
from core.etat import EtatAgent, Point, Trajet, StatutAgent
from core.decision_maker import DecisionMaker, RouteAlternative
from services.geocoding import service_geocoding
from services.data_manager import gestionnaire_donnees
from services.routing import ServiceRouting
from visualization.carte import GenerateurCarte
from visualization.rapport import GenerateurRapport
from utils.config import config
from utils.helpers import (
    calculer_distance_haversine, 
    calculer_duree_estimee,
    generer_points_intermediaires,
    formater_duree,
    formater_distance
)

class AgentVehicule:
    """
    Agent intelligent représentant un véhicule se déplaçant dans Kinshasa
    avec système de décision multi-routes
    """
    
    def __init__(self, etat_initial: str, etat_final: str, strategie: str = "rapide"):
        """
        Initialise l'agent véhicule pour Kinshasa
        
        Args:
            etat_initial: Point de départ (Place de la Victoire)
            etat_final: Point d'arrivée (Gare Centrale)
            strategie: Stratégie de décision ("rapide", "economique", "securise", "confort", "equilibre")
        """
        self.etat = EtatAgent(etat_initial, etat_final)
        self.service_routing = ServiceRouting()
        self.generateur_carte = GenerateurCarte()
        self.generateur_rapport = GenerateurRapport()
        self.decision_maker = DecisionMaker()
        self.strategie = strategie
        self.routes_alternatives = []
        self.route_choisie = None
        self.analyse_routes = {}
        
        print(f"🤖 Agent Véhicule initialisé pour Kinshasa")
        print(f"📍 Départ: {etat_initial}")
        print(f"🎯 Arrivée: {etat_final}")
        print(f"🎯 Stratégie: {strategie}")
    
    def demarrer(self):
        """Démarre l'agent"""
        self.etat.demarrer()
    
    def arreter(self):
        """Arrête l'agent"""
        self.etat.arreter()
    
    def planifier_itineraire(self) -> List[Point]:
        """
        Planifie l'itinéraire complet avec analyse multi-routes
        
        Returns:
            Liste des points formant l'itinéraire choisi
        """
        print("\n🗺️  DÉBUT DE LA PLANIFICATION AVEC DÉCISION MULTI-ROUTES")
        print("=" * 60)
        
        # 1. Géocoder les points de départ et d'arrivée
        print("🔍 Géocodage des points principaux...")
        point_depart = service_geocoding.geocoder_lieu(config.ETAT_INITIAL.split(',')[0].strip())
        point_arrivee = service_geocoding.geocoder_lieu(config.ETAT_FINAL.split(',')[0].strip())
        
        if not point_depart or not point_arrivee:
            print("❌ Impossible de géocoder les points principaux")
            return []
        
        # Définir les types de points
        point_depart.type_point = "depart"
        point_arrivee.type_point = "arrivee"
        
        # 2. Générer 5 routes alternatives
        print("🛣️  Génération des routes alternatives...")
        self.routes_alternatives = self.decision_maker.generer_routes_alternatives(
            point_depart, point_arrivee
        )
        
        # 3. Choisir la meilleure route selon la stratégie
        poids_strategie = self.decision_maker.definir_strategie(self.strategie)
        self.route_choisie, self.analyse_routes = self.decision_maker.choisir_meilleure_route(
            self.routes_alternatives, poids_strategie
        )
        
        # 4. Afficher l'itinéraire choisi
        print(f"\n📈 ITINÉRAIRE CHOISI ({self.route_choisie.nom}):")
        print("-" * 40)
        for i, point in enumerate(self.route_choisie.points):
            type_icon = "🚗" if i == 0 else "🏁" if i == len(self.route_choisie.points)-1 else "📍"
            print(f"{type_icon} {i+1:2d}. {point.nom}")
        
        # 5. Calculer les statistiques prévisionnelles
        caracteristiques = self.route_choisie.caracteristiques
        
        print(f"\n📊 STATISTIQUES PRÉVISIONNELLES:")
        print(f"   📏 Distance totale: {formater_distance(caracteristiques['distance_km'])}")
        print(f"   ⏱️  Durée estimée: {formater_duree(caracteristiques['temps_estime_min'])}")
        print(f"   💰 Coût estimé: {caracteristiques.get('cout_essence_usd', caracteristiques.get('cout_essence', 0)):.2f} USD")
        print(f"   🚦 Niveau embouteillages: {caracteristiques['niveau_embouteillage']:.1%}")
        print(f"   🛡️  Niveau sécurité: {caracteristiques['niveau_securite']:.1%}")
        print(f"   🛣️  Confort route: {caracteristiques['confort_route']:.1%}")
        print(f"   📍 Nombre d'étapes: {len(self.route_choisie.points)}")
        
        return self.route_choisie.points
    
    def executer_trajet(self, points_itineraire: List[Point]):
        """
        Exécute le trajet planifié étape par étape
        
        Args:
            points_itineraire: Liste des points de l'itinéraire
        """
        if len(points_itineraire) < 2:
            print("❌ Itinéraire insuffisant pour exécution")
            return
        
        print(f"\n🚗 DÉBUT DE L'EXÉCUTION DU TRAJET - {self.route_choisie.nom}")
        print("=" * 60)
        
        # Mettre à jour la position initiale
        self.etat.mettre_a_jour_position(points_itineraire[0])
        self.etat.statut = StatutAgent.EN_MOUVEMENT
        
        # Parcourir chaque segment de l'itinéraire
        for i in range(len(points_itineraire) - 1):
            depart = points_itineraire[i]
            arrivee = points_itineraire[i + 1]
            
            print(f"\n🛣️  SEGMENT {i+1}/{len(points_itineraire)-1}")
            print(f"   De: {depart.nom}")
            print(f"   À: {arrivee.nom}")
            
            # Calculer le trajet pour ce segment
            trajet_segment = self._calculer_trajet_segment(depart, arrivee, i+1)
            
            if trajet_segment:
                # Simuler le déplacement
                self._simuler_deplacement(trajet_segment)
                
                # Ajouter le trajet à l'historique
                self.etat.ajouter_trajet(trajet_segment)
                
                # Afficher les statistiques du segment
                self._afficher_statistiques_segment(trajet_segment)
            else:
                print(f"   ⚠️  Impossible de calculer le trajet pour ce segment")
                # Essayer de passer au segment suivant
                continue
            
            # Petite pause pour la simulation
            time.sleep(0.5)
        
        # Marquer l'arrivée
        self.etat.statut = StatutAgent.ARRIVE
        print(f"\n🎉 ARRIVÉE À DESTINATION: {points_itineraire[-1].nom}")
    
    def _calculer_trajet_segment(self, depart: Point, arrivee: Point, numero_segment: int) -> Optional[Trajet]:
        """
        Calcule un trajet entre deux points
        
        Args:
            depart: Point de départ du segment
            arrivee: Point d'arrivée du segment
            numero_segment: Numéro du segment pour l'affichage
            
        Returns:
            Trajet calculé ou None en cas d'erreur
        """
        try:
            # Calculer la distance
            distance_km = calculer_distance_haversine(depart, arrivee)
            
            # Calculer la durée estimée
            duree_min = calculer_duree_estimee(distance_km)
            
            # Générer des points intermédiaires pour la visualisation
            points_intermediaires = generer_points_intermediaires(depart, arrivee, nb_points=3)
            
            # Créer l'objet Trajet
            trajet = Trajet(
                depart=depart,
                arrivee=arrivee,
                distance_km=distance_km,
                duree_estimee_min=duree_min,
                points_intermediaires=points_intermediaires
            )
            
            return trajet
            
        except Exception as e:
            print(f"   ❌ Erreur calcul trajet segment {numero_segment}: {e}")
            return None
    
    def _simuler_deplacement(self, trajet: Trajet):
        """
        Simule le déplacement pour un trajet donné
        
        Args:
            trajet: Trajet à simuler
        """
        print(f"   🚦 Départ de {trajet.depart.nom}")
        
        # Simulation de progression
        for i in range(3):
            time.sleep(0.3)
            print(f"   {'>' * (i+1)} En route...")
        
        print(f"   🏁 Arrivée à {trajet.arrivee.nom}")
    
    def _afficher_statistiques_segment(self, trajet: Trajet):
        """
        Affiche les statistiques d'un segment
        
        Args:
            trajet: Trajet à analyser
        """
        print(f"   📊 Segment: {formater_distance(trajet.distance_km)}")
        print(f"   ⏱️  Durée: {formater_duree(trajet.duree_estimee_min)}")
        print(f"   🚗 Vitesse moyenne: {config.VITESSE_MOYENNE_KMH} km/h")
    
    def generer_rapports(self):
        """
        Génère tous les rapports et visualisations
        """
        print("\n📊 GÉNÉRATION DES RAPPORTS")
        print("=" * 50)
        
        # 1. Générer la carte interactive de l'itinéraire choisi
        print("🗺️  Génération de la carte de l'itinéraire choisi...")
        try:
            carte_html = self.generateur_carte.creer_carte_itineraire(
                self.etat.trajets_effectues,
                f"Itinéraire Agent Véhicule - {self.route_choisie.nom} - Kinshasa"
            )
            print(f"   ✅ Carte itinéraire générée: {carte_html}")
        except Exception as e:
            print(f"   ❌ Erreur génération carte itinéraire: {e}")
        
        # 2. Générer la carte multi-routes avec toutes les alternatives
        print("🗺️  Génération de la carte multi-routes...")
        try:
            carte_multi_html = self.generateur_carte.creer_carte_multi_routes(
                self.routes_alternatives,
                self.route_choisie,
                self.etat.trajets_effectues,
                f"Analyse Multi-Routes - {self.strategie.upper()} - Kinshasa"
            )
            print(f"   ✅ Carte multi-routes générée: {carte_multi_html}")
        except Exception as e:
            print(f"   ❌ Erreur génération carte multi-routes: {e}")
        
        # 3. Générer le rapport détaillé
        print("📄 Génération du rapport détaillé...")
        try:
            rapport_html = self.generateur_rapport.generer_rapport_complet(
                self.etat, 
                self.route_choisie,
                self.analyse_routes
            )
            if rapport_html:
                print(f"   ✅ Rapport généré: {rapport_html}")
            else:
                print("   ⚠️  Rapport non généré")
        except Exception as e:
            print(f"   ❌ Erreur génération rapport: {e}")
        
        # 4. Afficher le résumé dans la console
        print("\n📋 RÉSUMÉ DU VOYAGE")
        print("-" * 40)
        self._afficher_resume_voyage()
    
    def _afficher_resume_voyage(self):
        """Affiche un résumé du voyage dans la console"""
        stats = self.etat.obtenir_statistiques()
        
        print(f"📍 Point de départ: {self.etat.historique_etats[0]}")
        print(f"🎯 Point d'arrivée: {self.etat.historique_etats[-1]}")
        print(f"🛣️  Route choisie: {self.route_choisie.nom}")
        print(f"🎯 Stratégie: {self.strategie}")
        print(f"📏 Distance totale: {stats['distance_totale_km']:.2f} km")
        print(f"⏱️  Durée totale: {formater_duree(stats['duree_totale_min'])}")
        print(f"🛣️  Nombre de segments: {stats['nombre_trajets']}")
        print(f"📍 Points visités: {len(self.etat.historique_etats)}")
        
        print(f"\n🗺️  PARCOURS EFFECTUÉ:")
        for i, etape in enumerate(self.etat.historique_etats):
            icon = "🚗" if i == 0 else "🏁" if i == len(self.etat.historique_etats)-1 else "📍"
            print(f"   {icon} {i+1:2d}. {etape}")
    
    def obtenir_statistiques(self) -> Dict[str, Any]:
        """
        Retourne les statistiques complètes de l'agent
        
        Returns:
            Dictionnaire des statistiques
        """
        stats = self.etat.obtenir_statistiques()
        stats.update({
            "route_choisie": self.route_choisie.nom,
            "strategie": self.strategie,
            "analyse_routes": self.analyse_routes
        })
        return stats
    
    def est_mission_accomplie(self) -> bool:
        """
        Vérifie si la mission est accomplie
        
        Returns:
            True si l'agent est arrivé à destination
        """
        return self.etat.est_arrive()
    
    def __str__(self) -> str:
        """Représentation textuelle de l'agent"""
        return str(self.etat)