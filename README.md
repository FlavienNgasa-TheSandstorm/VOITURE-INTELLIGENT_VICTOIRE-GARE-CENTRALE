# VOITURE-INTELLIGENT_VICTOIRE-GARE-CENTRALE
Agent intelligent simulant un véhicule partant du Rond Point Victoire vers la Gare Centrale de Kinshasa. Système multi-stratégies analysant 5 routes alternatives avec géocodage OpenStreetMap, cartes interactives et rapports détaillés.

🚗 Agent Véhicule Intelligent - Kinshasa
Simulation d'un véhicule intelligent partant du Rond Point Victoire vers la Gare Centrale de Kinshasa avec analyse multi-routes et décision stratégique. Système agent-orienté avec visualisation cartographique et rapports détaillés.

🛠️ Technologies Utilisées
Langages
Python 3.8+ - Langage principal

HTML5/CSS3/JavaScript - Rapports et visualisations

YAML - Configuration avancée

JSON - Données structurées

Markdown - Documentation

Bibliothèques Principales
yaml
python:
  - folium: "Cartes interactives OpenStreetMap"
  - flask: "API Web et interface (extension prévue)"
  - requests: "Appels API Nominatim/Google Maps"
  - pyyaml: "Gestion de configuration YAML"
  - dataclasses: "Structures de données"
  - typing: "Annotations de type"
  - math: "Calculs géométriques"
  - time: "Gestion du temps"
  - json: "Manipulation JSON"
  - os/sys: "Système et chemins"
Services Externes
OpenStreetMap/Nominatim - Géocodage gratuit

Google Maps API - Option pour routing avancé

Folium - Cartographie interactive

📁 Structure du Projet
text
projet_agent_vehicule/
├── 📁 src/                      # Code source
│   ├── 🐍 core/                # Cœur de l'agent
│   ├── 🗺️ services/            # Services externes
│   ├── 🎨 visualization/       # Cartes et rapports
│   └── 🔧 utils/               # Utilitaires
├── 📁 data/                    # Données locales
├── 📁 tests/                   # Tests unitaires
├── 📁 docs/                    # Documentation
├── 📁 examples/                # Exemples d'utilisation
├── main.py                     # Point d'entrée
├── requirements.txt            # Dépendances Python
├── config.yaml                 # Configuration YAML (optionnel)
└── README.md                   # Ce fichier
🚀 Installation Rapide
Cloner le projet

bash
git clone <repository>
cd projet_agent_vehicule
Installer les dépendances

bash
pip install -r requirements.txt
Lancer l'agent

bash
python main.py [strategie]
🎯 Stratégies Disponibles
rapide - Priorité temps de trajet

economique - Priorité coûts

securise - Priorité sécurité

confort - Priorité confort

equilibre - Équilibre tous critères

📊 Fonctionnalités
✅ Système agent-orienté avec états

✅ Analyse multi-routes (5 alternatives)

✅ Géocodage OpenStreetMap

✅ Cartes interactives Folium

✅ Rapports HTML détaillés

✅ Simulation réaliste Kinshasa

✅ Configuration modulaire

🔧 Extensions Possibles
API Flask pour interface web

Google Maps API pour routing précis

Base de données pour historiques

Interface graphique avec Tkinter/PyQt

Système en temps réel avec WebSockets

📝 Exemple d'utilisation
bash
# Route la plus rapide (défaut)
python main.py

# Route économique
python main.py economique

# Route sécurisée
python main.py securise
📈 Résultats Générés
Carte interactive HTML - Visualisation du trajet

Carte multi-routes - Comparaison des alternatives

Rapport HTML complet - Statistiques détaillées

Sortie console - Logs d'exécution

🤝 Contribution
Ce projet est conçu comme une base modulable. Les extensions avec Flask pour une API REST et YAML pour une configuration avancée sont fortement encouragées.

📄 Licence
Projet éducatif - Libre d'utilisation et modification

💡 Note : Ce projet est spécifiquement adapté au contexte de Kinshasa, RDC, mais peut être facilement configuré pour d'autres villes.
