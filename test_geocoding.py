#!/usr/bin/env python3
"""
Tests pour le service de géocodage
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.geocoding import service_geocoding
from src.services.data_manager import gestionnaire_donnees

def test_geocoding_basique():
    """Test de géocodage basique"""
    print("🧪 Test de géocodage basique...")
    
    point = service_geocoding.geocoder_lieu("Rond Point Victoire", "Dakar")
    if point:
        print(f"✅ Rond Point Victoire: {point.latitude}, {point.longitude}")
    else:
        print("❌ Échec géocodage Rond Point Victoire")
    
    point = service_geocoding.geocoder_lieu("Gare Centrale", "Dakar")
    if point:
        print(f"✅ Gare Centrale: {point.latitude}, {point.longitude}")
    else:
        print("❌ Échec géocodage Gare Centrale")

def test_points_interet():
    """Test des points d'intérêt locaux"""
    print("\n🧪 Test des points d'intérêt...")
    
    points = gestionnaire_donnees.obtenir_points_interet()
    print(f"✅ {len(points)} points d'intérêt chargés")
    
    for point in points[:3]:  # Afficher les 3 premiers
        print(f"   📍 {point.nom}: {point.latitude}, {point.longitude}")

def test_connectivite():
    """Test de connectivité à l'API"""
    print("\n🧪 Test de connectivité...")
    
    if service_geocoding.verifier_connectivite():
        print("✅ Connecté à l'API Nominatim")
    else:
        print("❌ Impossible de se connecter à l'API Nominatim")

if __name__ == "__main__":
    print("🔬 TESTS SERVICE GÉOCODAGE")
    print("=" * 40)
    
    test_connectivite()
    test_geocoding_basique()
    test_points_interet()
    
    print("\n" + "=" * 40)
    print("✅ Tests terminés")