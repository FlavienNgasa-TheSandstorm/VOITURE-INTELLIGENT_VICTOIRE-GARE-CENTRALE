"""
Service de géocodage utilisant l'API Nominatim d'OpenStreetMap - VERSION KINSHASA RÉELLE
"""
import requests
import time
import json
import os
from typing import Dict, List, Optional, Tuple

# Imports absolus
from core.etat import Point
from utils.config import config
from utils.helpers import calculer_distance_haversine

class ServiceGeocoding:
    """
    Service responsable du géocodage des adresses et lieux - KINSHASA RÉELLE
    """
    
    def __init__(self):
        self.cache_file = config.FICHIER_CACHE_GEOCODING
        self.cache = self._charger_cache()
        self.derniere_requete = 0
        self.delai_requete = config.NOMINATIM_DELAY
    
    def _charger_cache(self) -> Dict:
        """Charge le cache de géocodage depuis le fichier"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Erreur chargement cache: {e}")
        return {}
    
    def _sauvegarder_cache(self):
        """Sauvegarde le cache dans le fichier"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Erreur sauvegarde cache: {e}")
    
    def _respecter_delai_api(self):
        """Respecte le délai entre les requêtes API"""
        temps_actuel = time.time()
        temps_ecoule = temps_actuel - self.derniere_requete
        if temps_ecoule < self.delai_requete:
            time.sleep(self.delai_requete - temps_ecoule)
        self.derniere_requete = time.time()
    
    def _geocoder_requete_standard(self, lieu: str, ville: str, pays: str) -> Optional[Point]:
        """Effectue une requête de géocodage standard"""
        try:
            self._respecter_delai_api()
            
            query = f"{lieu}, {ville}, {pays}"
            headers = {
                'User-Agent': 'AgentVehicule/1.0 (projet_agent_vehicule)',
                'Accept-Language': 'fr'
            }
            
            params = {
                'q': query,
                'format': 'json',
                'limit': 1,
                'addressdetails': 1
            }
            
            print(f"🔍 Géocodage: {query}")
            response = requests.get(
                config.NOMINATIM_URL,
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data:
                resultat = data[0]
                point = Point(
                    nom=lieu,
                    latitude=float(resultat['lat']),
                    longitude=float(resultat['lon']),
                    type_point="geocode"
                )
                
                # Mettre en cache
                self.cache[f"{lieu}, {ville}, {pays}"] = point.to_dict()
                self._sauvegarder_cache()
                
                print(f"   ✅ Trouvé: {point.latitude:.4f}, {point.longitude:.4f}")
                return point
            else:
                print(f"   ❌ Lieu non trouvé: {query}")
                return None
                
        except Exception as e:
            print(f"   ❌ Erreur géocodage: {e}")
            return None

    def geocoder_lieu(self, lieu: str, ville: str = None, pays: str = None) -> Optional[Point]:
        """
        Géocode un lieu en coordonnées géographiques - KINSHASA RÉELLE
        
        Args:
            lieu: Le nom du lieu à géocoder
            ville: Ville pour améliorer la précision (défaut: Kinshasa)
            pays: Pays pour améliorer la précision (défaut: RDC)
            
        Returns:
            Point géocodé ou None en cas d'erreur
        """
        # Utiliser les valeurs par défaut de la configuration
        if ville is None:
            ville = config.VILLE_DEFAUT
        if pays is None:
            pays = config.PAYS_DEFAUT
        
        # Vérifier d'abord les points prédéfinis de Kinshasa
        point_predefini = self._verifier_points_predefinis_kinshasa(lieu)
        if point_predefini:
            print(f"📂 Utilisation point prédéfini: {lieu}")
            return point_predefini
        
        # Vérifier le cache d'abord
        cle_cache = f"{lieu}, {ville}, {pays}"
        if cle_cache in self.cache:
            cache_data = self.cache[cle_cache]
            print(f"📂 Utilisation cache: {lieu}")
            return Point.from_dict(cache_data)
        
        # ESSAI 1: Recherche normale
        point = self._geocoder_requete_standard(lieu, ville, pays)
        if point:
            return point
        
        # ESSAI 2: Recherche avec alias pour Kinshasa
        point_alias = self._recherche_alias_kinshasa(lieu, ville, pays)
        if point_alias:
            return point_alias
        
        return None
    
    def _verifier_points_predefinis_kinshasa(self, lieu: str) -> Optional[Point]:
        """Vérifie si le lieu fait partie des points prédéfinis de Kinshasa"""
        points_kinshasa = {
            "place de la victoire": Point("Place de la Victoire", -4.33787, 15.30553, "depart"),
            "victoire": Point("Place de la Victoire", -4.33787, 15.30553, "depart"),
            "rond point victoire": Point("Place de la Victoire", -4.33787, 15.30553, "depart"),
            "gare centrale": Point("Gare Centrale", -4.31600, 15.31300, "arrivee"),
            "gare": Point("Gare Centrale", -4.31600, 15.31300, "arrivee"),
            "marché central": Point("Marché Central", -4.32500, 15.31000, "intermediaire"),
            "stade des martyrs": Point("Stade des Martyrs", -4.33200, 15.30800, "intermediaire"),
            "université de kinshasa": Point("Université de Kinshasa", -4.41500, 15.30300, "intermediaire"),
            "hôpital général de kinshasa": Point("Hôpital Général de Kinshasa", -4.32200, 15.31100, "intermediaire"),
            "palais du peuple": Point("Palais du Peuple", -4.31800, 15.31200, "intermediaire"),
            "tour de l'échangeur": Point("Tour de l'Échangeur", -4.33500, 15.30600, "intermediaire"),
            "avenue de la justice": Point("Avenue de la Justice", -4.32000, 15.31100, "intermediaire"),
            "boulevard du 30 juin": Point("Boulevard du 30 Juin", -4.32800, 15.30900, "intermediaire"),
            "avenue des aviateurs": Point("Avenue des Aviateurs", -4.32200, 15.30800, "intermediaire"),
            "place du marché": Point("Place du Marché", -4.32600, 15.31000, "intermediaire"),
            "carrefour forescom": Point("Carrefour Forescom", -4.33000, 15.30700, "intermediaire"),
            "avenue de la libération": Point("Avenue de la Libération", -4.31900, 15.31200, "intermediaire"),
            "immeuble sozacom": Point("Immeuble Sozacom", -4.31700, 15.31300, "intermediaire")
        }
        
        lieu_min = lieu.lower().strip()
        return points_kinshasa.get(lieu_min)

    def _recherche_alias_kinshasa(self, lieu: str, ville: str, pays: str) -> Optional[Point]:
        """Recherche avec des alias spécifiques à Kinshasa"""
        alias_kinshasa = {
            "place de la victoire": ["victoire", "rond point victoire", "rond-point victoire"],
            "gare centrale": ["gare", "station centrale", "gare routière"],
            "marché central": ["grand marché", "marché", "central market"],
            "stade des martyrs": ["stade", "martyrs stadium", "stade martyrs"]
        }
        
        lieu_min = lieu.lower().strip()
        
        for point_principal, alias_list in alias_kinshasa.items():
            if lieu_min in alias_list:
                print(f"   🔄 Utilisation alias: {point_principal} pour {lieu}")
                return self.geocoder_lieu(point_principal, ville, pays)
        
        return None
    
    def geocoder_plusieurs_lieux(self, lieux: List[str]) -> List[Point]:
        """
        Géocode plusieurs lieux en une seule opération
        
        Args:
            lieux: Liste des noms de lieux à géocoder
            
        Returns:
            Liste des points géocodés
        """
        points = []
        for lieu in lieux:
            point = self.geocoder_lieu(lieu)
            if point:
                points.append(point)
            time.sleep(0.5)  # Délai supplémentaire entre les géocodages
        
        return points
    
    def rechercher_points_proches(self, point_reference: Point, rayon_km: float = 2.0) -> List[Point]:
        """
        Recherche des points d'intérêt près d'un point de référence
        
        Args:
            point_reference: Point central de recherche
            rayon_km: Rayon de recherche en kilomètres
            
        Returns:
            Liste des points d'intérêt trouvés
        """
        try:
            self._respecter_delai_api()
            
            headers = {
                'User-Agent': 'AgentVehicule/1.0 (projet_agent_vehicule)',
                'Accept-Language': 'fr'
            }
            
            params = {
                'format': 'json',
                'lat': point_reference.latitude,
                'lon': point_reference.longitude,
                'radius': rayon_km * 1000,  # Conversion en mètres
                'limit': 10,
                'q': '[amenity=bus_station]|[amenity=taxi]|[public_transport=stop_position]'
            }
            
            print(f"🔍 Recherche points proches de {point_reference.nom}")
            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            points_trouves = []
            
            for item in data:
                point = Point(
                    nom=item.get('display_name', 'Point inconnu').split(',')[0],
                    latitude=float(item['lat']),
                    longitude=float(item['lon']),
                    type_point=item.get('type', 'inconnu')
                )
                points_trouves.append(point)
            
            print(f"   ✅ {len(points_trouves)} points trouvés")
            return points_trouves
            
        except Exception as e:
            print(f"   ❌ Erreur recherche points proches: {e}")
            return []
    
    def obtenir_adresse_inverse(self, latitude: float, longitude: float) -> Optional[str]:
        """
        Géocodage inverse : coordonnées → adresse
        
        Args:
            latitude: Latitude du point
            longitude: Longitude du point
            
        Returns:
            Adresse formatée ou None
        """
        try:
            self._respecter_delai_api()
            
            headers = {
                'User-Agent': 'AgentVehicule/1.0 (projet_agent_vehicule)',
                'Accept-Language': 'fr'
            }
            
            params = {
                'format': 'json',
                'lat': latitude,
                'lon': longitude,
                'zoom': 18,
                'addressdetails': 1
            }
            
            response = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('display_name')
            
        except Exception as e:
            print(f"❌ Erreur géocodage inverse: {e}")
            return None
    
    def verifier_connectivite(self) -> bool:
        """
        Vérifie la connectivité avec le service Nominatim
        
        Returns:
            True si connecté, False sinon
        """
        try:
            headers = {
                'User-Agent': 'AgentVehicule/1.0 (projet_agent_vehicule)'
            }
            
            params = {
                'q': 'Kinshasa',
                'format': 'json',
                'limit': 1
            }
            
            response = requests.get(
                config.NOMINATIM_URL,
                params=params,
                headers=headers,
                timeout=5
            )
            return response.status_code == 200
            
        except:
            return False

# Instance globale du service
service_geocoding = ServiceGeocoding()