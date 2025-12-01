"""
Génération de cartes interactives - VERSION KINSHASA CORRIGÉE
"""
import folium
from typing import List, Dict, Any

# Imports absolus
from core.etat import Trajet, Point
from utils.config import config
from utils.helpers import calculer_barycentre

class GenerateurCarte:
    """
    Génère des cartes interactives avec Folium/OpenStreetMap pour Kinshasa
    Version corrigée avec toutes les routes visibles
    """
    
    def __init__(self):
        self.couleurs = {
            "depart": config.COULEUR_DEPART,
            "arrivee": config.COULEUR_ARRIVEE,
            "intermediaire": config.COULEUR_INTERMEDIAIRE,
            "arret_bus": config.COULEUR_ARRET_BUS
        }
    
    def creer_carte_itineraire(self, trajets: List[Trajet], titre: str = "Itinéraire Agent Véhicule") -> str:
        """
        Crée une carte interactive avec l'itinéraire complet
        
        Args:
            trajets: Liste des trajets à afficher
            titre: Titre de la carte
            
        Returns:
            Chemin du fichier HTML généré
        """
        if not trajets:
            print("❌ Aucun trajet à afficher sur la carte")
            return ""
        
        # Calculer le centre de la carte
        tous_points = []
        for trajet in trajets:
            tous_points.append(trajet.depart)
            tous_points.append(trajet.arrivee)
            tous_points.extend(trajet.points_intermediaires)
        
        centre_lat, centre_lon = calculer_barycentre(tous_points)
        
        # Créer la carte centrée sur Kinshasa
        carte = folium.Map(
            location=[centre_lat, centre_lon],
            zoom_start=config.ZOOM_CARTE,
            tiles='OpenStreetMap'
        )
        
        # Ajouter chaque trajet
        for i, trajet in enumerate(trajets):
            self._ajouter_trajet_carte(carte, trajet, i)
        
        # Ajouter les marqueurs des points importants
        self._ajouter_marqueurs_carte(carte, trajets)
        
        # Ajouter un titre amélioré
        self._ajouter_titre_carte_ameliore(carte, titre)
        
        # Ajouter une légende
        self._ajouter_legende_carte_amelioree(carte)
        
        # Sauvegarder la carte
        nom_fichier = f"carte_itineraire_kinshasa.html"
        carte.save(nom_fichier)
        
        return nom_fichier
    
    def creer_carte_multi_routes(self, routes_alternatives, route_choisie, trajets_effectues, titre: str = "Analyse Multi-Routes - Kinshasa") -> str:
        """
        Crée une carte interactive avec TOUTES les routes alternatives
        Version corrigée avec toutes les routes visibles
        """
        if not routes_alternatives:
            print("❌ Aucune route alternative à afficher sur la carte")
            return ""
        
        # Calculer le centre de la carte basé sur toutes les routes
        tous_points = []
        for route in routes_alternatives:
            tous_points.extend(route.points)
        
        centre_lat, centre_lon = calculer_barycentre(tous_points)
        
        # Créer la carte centrée sur Kinshasa
        carte = folium.Map(
            location=[centre_lat, centre_lon],
            zoom_start=config.ZOOM_CARTE,
            tiles='OpenStreetMap'
        )
        
        # Couleurs pour les différentes routes - CORRECTION DES COULEURS
        couleurs_routes = {
            "Route Principale - Boulevard du 30 Juin": 'blue',
            "Route Secondaire - Avenue des Aviateurs": 'purple', 
            "Route Scénique - Centre Ville": 'orange',
            "Route Rapide - Voie Express": 'green',
            "Route Économique - Itinéraire Court": 'red'
        }
        
        print(f"   🎨 Génération de {len(routes_alternatives)} routes avec couleurs...")
        
        # Ajouter chaque route alternative avec tous ses points
        for route in routes_alternatives:
            couleur = couleurs_routes.get(route.nom, 'gray')
            epaisseur = 8 if route.nom == route_choisie.nom else 4
            opacite = 0.9 if route.nom == route_choisie.nom else 0.6
            
            # Coordonnées pour la ligne
            coords = [[point.latitude, point.longitude] for point in route.points]
            
            # CORRECTION : Créer l'objet PolyLine et l'ajouter à la carte
            ligne = folium.PolyLine(
                locations=coords,
                color=couleur,
                weight=epaisseur,
                opacity=opacite,
                popup=f"<b>{route.nom}</b><br>"
                      f"Distance: {route.caracteristiques['distance_km']:.1f}km<br>"
                      f"Temps: {route.caracteristiques['temps_estime_min']:.1f}min<br>"
                      f"Points: {len(route.points)}",
                tooltip=f"{route.nom} (Temps: {route.caracteristiques['temps_estime_min']:.1f}min)"
            )
            ligne.add_to(carte)
            
            print(f"      ✅ Route '{route.nom}' ajoutée (couleur: {couleur})")
            
            # Ajouter des marqueurs pour TOUS les points de cette route
            for i, point in enumerate(route.points):
                # Déterminer l'icône et la couleur selon le type de point
                if i == 0:  # Départ
                    icon_color = 'green'
                    icon_type = 'play'
                    prefix = 'fa'
                    type_point = "Départ"
                elif i == len(route.points) - 1:  # Arrivée
                    icon_color = 'red'
                    icon_type = 'stop'
                    prefix = 'fa'
                    type_point = "Arrivée"
                else:  # Point intermédiaire
                    icon_color = couleur
                    icon_type = 'info-circle'
                    prefix = 'fa'
                    type_point = "Intermédiaire"
                
                # Créer le popup détaillé
                popup_html = f"""
                <div style="min-width: 280px; font-family: Arial, sans-serif;">
                    <h4 style="color: #2c3e50; margin-bottom: 10px; border-bottom: 2px solid {couleur}; padding-bottom: 5px;">
                        <b>{point.nom}</b>
                    </h4>
                    <p><b>Route:</b> {route.nom}</p>
                    <p><b>Type:</b> {type_point}</p>
                    <p><b>Position:</b> {i+1}/{len(route.points)}</p>
                    <p><b>Coordonnées:</b><br>
                    Lat: {point.latitude:.6f}<br>
                    Lon: {point.longitude:.6f}</p>
                    <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                        <p style="margin: 5px 0; font-size: 0.9em;"><b>Caractéristiques:</b></p>
                        <p style="margin: 3px 0; font-size: 0.85em;">• Distance: {route.caracteristiques['distance_km']:.1f} km</p>
                        <p style="margin: 3px 0; font-size: 0.85em;">• Temps: {route.caracteristiques['temps_estime_min']:.1f} min</p>
                        <p style="margin: 3px 0; font-size: 0.85em;">• Coût: {route.caracteristiques.get('cout_essence_usd', route.caracteristiques.get('cout_essence', 0)):.2f} USD</p>
                    </div>
                </div>
                """
                
                # CORRECTION : Créer le marqueur et l'ajouter à la carte
                marqueur = folium.Marker(
                    location=[point.latitude, point.longitude],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{route.nom}: {point.nom} ({type_point})",
                    icon=folium.Icon(color=icon_color, icon=icon_type, prefix=prefix)
                )
                marqueur.add_to(carte)
        
        # Ajouter un titre amélioré
        self._ajouter_titre_carte_ameliore(carte, titre)
        
        # Ajouter une légende améliorée
        self._ajouter_legende_multi_routes_amelioree(carte, couleurs_routes, route_choisie.nom)
        
        # Sauvegarder la carte
        nom_fichier = f"carte_multi_routes_kinshasa.html"
        carte.save(nom_fichier)
        
        print(f"   ✅ Carte multi-routes générée: {nom_fichier}")
        print(f"   📍 Routes affichées:")
        for route in routes_alternatives:
            couleur = couleurs_routes.get(route.nom, 'gray')
            print(f"      • {route.nom} ({couleur}, {len(route.points)} points)")
        
        return nom_fichier
    
    def _ajouter_trajet_carte(self, carte: folium.Map, trajet: Trajet, index: int):
        """
        Ajoute un trajet à la carte
        
        Args:
            carte: Carte Folium
            trajet: Trajet à ajouter
            index: Index du trajet pour la couleur
        """
        couleurs = ['blue', 'red', 'green', 'purple', 'orange', 'darkred', 'lightred']
        couleur = couleurs[index % len(couleurs)]
        
        # Points du trajet (départ + intermédiaires + arrivée)
        points_trajet = [trajet.depart]
        points_trajet.extend(trajet.points_intermediaires)
        points_trajet.append(trajet.arrivee)
        
        # Coordonnées pour la ligne
        coords = [[point.latitude, point.longitude] for point in points_trajet]
        
        # Ajouter la ligne
        folium.PolyLine(
            coords,
            color=couleur,
            weight=6,
            opacity=0.7,
            popup=f"Segment {index+1}: {trajet.depart.nom} → {trajet.arrivee.nom}",
            tooltip=f"Distance: {trajet.distance_km:.1f} km"
        ).add_to(carte)
    
    def _ajouter_marqueurs_carte(self, carte: folium.Map, trajets: List[Trajet]):
        """
        Ajoute les marqueurs des points importants à la carte
        
        Args:
            carte: Carte Folium
            trajets: Liste des trajets
        """
        if not trajets:
            return
        
        # Points uniques pour éviter les doublons
        points_deja_ajoutes = set()
        
        for trajet in trajets:
            # Marqueur de départ (sauf si déjà ajouté)
            if trajet.depart.nom not in points_deja_ajoutes:
                self._ajouter_marqueur_point(
                    carte, trajet.depart, 
                    "green", "play", "fa", "Départ - Place de la Victoire"
                )
                points_deja_ajoutes.add(trajet.depart.nom)
            
            # Marqueur d'arrivée (sauf si déjà ajouté)
            if trajet.arrivee.nom not in points_deja_ajoutes:
                self._ajouter_marqueur_point(
                    carte, trajet.arrivee,
                    "red", "stop", "fa", "Arrivée - Gare Centrale"
                )
                points_deja_ajoutes.add(trajet.arrivee.nom)
            
            # Marqueurs des points intermédiaires
            for point_inter in trajet.points_intermediaires:
                if point_inter.nom not in points_deja_ajoutes:
                    self._ajouter_marqueur_point(
                        carte, point_inter,
                        "blue", "info-circle", "fa", "Point intermédiaire"
                    )
                    points_deja_ajoutes.add(point_inter.nom)
    
    def _ajouter_marqueur_point(self, carte: folium.Map, point: Point, 
                              couleur: str, icone: str, prefixe: str, type_point: str):
        """
        Ajoute un marqueur individuel à la carte
        
        Args:
            carte: Carte Folium
            point: Point à marquer
            couleur: Couleur du marqueur
            icone: Icône à utiliser
            prefixe: Préfixe de l'icône
            type_point: Type de point pour le popup
        """
        popup_html = f"""
        <div style="min-width: 250px; font-family: Arial, sans-serif;">
            <h4 style="color: #2c3e50; margin-bottom: 10px; border-bottom: 2px solid {couleur}; padding-bottom: 5px;">
                <b>{point.nom}</b>
            </h4>
            <p style="margin: 8px 0;"><i class="fas fa-map-marker-alt"></i> <b>{type_point}</b></p>
            <p style="margin: 5px 0;"><b>Coordonnées:</b></p>
            <p style="margin: 3px 0; font-size: 0.9em;">Latitude: {point.latitude:.6f}</p>
            <p style="margin: 3px 0; font-size: 0.9em;">Longitude: {point.longitude:.6f}</p>
        </div>
        """
        
        folium.Marker(
            location=[point.latitude, point.longitude],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{point.nom} ({type_point})",
            icon=folium.Icon(color=couleur, icon=icone, prefix=prefixe)
        ).add_to(carte)
    
    def _ajouter_titre_carte_ameliore(self, carte: folium.Map, titre: str):
        """
        Ajoute un titre amélioré à la carte
        
        Args:
            carte: Carte Folium
            titre: Titre à afficher
        """
        titre_html = f'''
        <div style="position: fixed; 
                    top: 10px; 
                    left: 50%; 
                    transform: translateX(-50%);
                    z-index: 9999; 
                    background: white; 
                    padding: 20px 40px; 
                    border-radius: 15px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                    border: 3px solid #3498db;
                    text-align: center;
                    max-width: 80%;
                    font-family: Arial, sans-serif;">
            <h2 style="margin: 0; color: #2c3e50; font-size: 24px; font-weight: bold;">
                🗺️ {titre}
            </h2>
            <p style="margin: 8px 0 0 0; color: #7f8c8d; font-size: 16px; font-weight: 500;">
                Kinshasa, RDC | Place de la Victoire (Kalamu) → Gare Centrale (Gombe)
            </p>
        </div>
        '''
        carte.get_root().html.add_child(folium.Element(titre_html))
    
    def _ajouter_legende_carte_amelioree(self, carte: folium.Map):
        """
        Ajoute une légende améliorée à la carte
        
        Args:
            carte: Carte Folium
        """
        legende_html = '''
        <div style="position: fixed; 
                    bottom: 50px; 
                    left: 20px; 
                    width: 280px; 
                    background-color: white; 
                    border: 3px solid #34495e; 
                    z-index: 9999; 
                    font-size: 14px; 
                    padding: 20px; 
                    border-radius: 12px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                    font-family: Arial, sans-serif;">
            <h4 style="margin-top: 0; 
                       color: #2c3e50; 
                       border-bottom: 2px solid #3498db; 
                       padding-bottom: 12px;
                       text-align: center;">
                🧭 LÉGENDE
            </h4>
            <div style="margin: 15px 0;">
                <div style="display: flex; align-items: center; margin: 10px 0;">
                    <div style="width: 20px; height: 20px; background: #27ae60; border-radius: 50%; margin-right: 10px;"></div>
                    <span><b>Départ:</b> Place de la Victoire (Kalamu)</span>
                </div>
                <div style="display: flex; align-items: center; margin: 10px 0;">
                    <div style="width: 20px; height: 20px; background: #e74c3c; border-radius: 50%; margin-right: 10px;"></div>
                    <span><b>Arrivée:</b> Gare Centrale (Gombe)</span>
                </div>
                <div style="display: flex; align-items: center; margin: 10px 0;">
                    <div style="width: 20px; height: 20px; background: #3498db; border-radius: 50%; margin-right: 10px;"></div>
                    <span><b>Points intermédiaires</b></span>
                </div>
                <div style="display: flex; align-items: center; margin: 10px 0;">
                    <div style="width: 20px; height: 20px; background: #f39c12; border-radius: 50%; margin-right: 10px;"></div>
                    <span><b>Arrêts de bus</b></span>
                </div>
            </div>
            <div style="margin-top: 15px; padding-top: 12px; border-top: 1px solid #ecf0f1; color: #7f8c8d; font-size: 12px;">
                <p style="margin: 5px 0;"><b>ℹ️ Information:</b></p>
                <p style="margin: 3px 0;">• Cliquez sur les points pour plus de détails</p>
                <p style="margin: 3px 0;">• Survolez les lignes pour les informations</p>
            </div>
        </div>
        '''
        carte.get_root().html.add_child(folium.Element(legende_html))
    
    def _ajouter_legende_multi_routes_amelioree(self, carte: folium.Map, couleurs_routes: Dict, route_choisie_nom: str):
        """
        Ajoute une légende améliorée pour la carte multi-routes
        
        Args:
            carte: Carte Folium
            couleurs_routes: Dictionnaire des couleurs des routes
            route_choisie_nom: Nom de la route choisie
        """
        legende_html = f'''
        <div style="position: fixed; 
                    bottom: 50px; 
                    left: 20px; 
                    width: 380px; 
                    background-color: white; 
                    border: 3px solid #34495e; 
                    z-index: 9999; 
                    font-size: 14px; 
                    padding: 25px; 
                    border-radius: 15px; 
                    box-shadow: 0 6px 25px rgba(0,0,0,0.15);
                    font-family: Arial, sans-serif;
                    max-height: 80vh;
                    overflow-y: auto;">
            <h4 style="margin-top: 0; 
                       color: #2c3e50; 
                       border-bottom: 3px solid #3498db; 
                       padding-bottom: 15px;
                       text-align: center;
                       font-size: 18px;">
                🗺️ LÉGENDE MULTI-ROUTES
            </h4>
            <div style="margin: 20px 0;">
        '''
        
        for nom_route, couleur in couleurs_routes.items():
            style_ligne = f'''
            padding: 12px 15px; 
            margin: 10px 0; 
            border-left: 5px solid {couleur}; 
            background: #f8f9fa; 
            border-radius: 8px;
            transition: all 0.3s ease;
            '''
            if nom_route == route_choisie_nom:
                style_ligne += '''
                font-weight: bold; 
                background: #e8f5e8; 
                border: 2px solid #27ae60;
                transform: scale(1.02);
                '''
            
            legende_html += f'''
            <div style="{style_ligne}">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <span style="color: {couleur}; font-size: 20px; margin-right: 12px;">●</span> 
                        <strong>{nom_route}</strong>
                    </div>
                    {"<span style='background: #27ae60; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold;'>🏆 CHOISIE</span>" if nom_route == route_choisie_nom else ""}
                </div>
            </div>
            '''
        
        legende_html += '''
            </div>
            <div style="margin-top: 20px; 
                        padding-top: 15px; 
                        border-top: 2px solid #ecf0f1; 
                        color: #7f8c8d; 
                        font-size: 13px;
                        background: #f8f9fa;
                        padding: 15px;
                        border-radius: 8px;">
                <p style="margin: 8px 0; font-weight: bold; color: #2c3e50;">🎯 Informations importantes:</p>
                <div style="margin: 8px 0;">
                    <span style="background: #3498db; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; margin-right: 8px;">LIGNE ÉPAISSE</span>
                    <span>Route choisie</span>
                </div>
                <div style="margin: 8px 0;">
                    <span style="background: #95a5a6; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; margin-right: 8px;">LIGNE FINE</span>
                    <span>Routes alternatives</span>
                </div>
                <div style="margin: 8px 0;">
                    <span style="background: #27ae60; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; margin-right: 8px;">🟢 DÉPART</span>
                    <span>Place de la Victoire (Kalamu)</span>
                </div>
                <div style="margin: 8px 0;">
                    <span style="background: #e74c3c; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; margin-right: 8px;">🔴 ARRIVÉE</span>
                    <span>Gare Centrale (Gombe)</span>
                </div>
                <div style="margin: 8px 0;">
                    <span style="background: #3498db; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; margin-right: 8px;">🔵 POINTS</span>
                    <span>Tous les points intermédiaires affichés</span>
                </div>
            </div>
            <div style="margin-top: 15px; text-align: center;">
                <p style="font-size: 12px; color: #7f8c8d; margin: 0;">
                    <i class="fas fa-mouse-pointer"></i> Cliquez sur les éléments pour plus d'informations
                </p>
            </div>
        </div>
        '''
        
        carte.get_root().html.add_child(folium.Element(legende_html))

# Instance globale du générateur de cartes
generateur_carte = GenerateurCarte()