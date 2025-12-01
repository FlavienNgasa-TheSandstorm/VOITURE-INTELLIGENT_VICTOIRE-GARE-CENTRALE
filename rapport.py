"""
Génération de rapports - VERSION KINSHASA DESIGN IMPECCABLE
"""
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import os

# Imports absolus
from utils.config import config
from utils.helpers import formater_duree, formater_distance

class GenerateurRapport:
    """
    Génère des rapports détaillés sur le voyage de l'agent
    Version avec design impeccable
    """
    
    def __init__(self):
        self.date_generation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.rapports_dir = "rapports"
        self._creer_dossier_rapports()
    
    def _creer_dossier_rapports(self):
        """Crée le dossier des rapports s'il n'existe pas"""
        os.makedirs(self.rapports_dir, exist_ok=True)
    
    def generer_rapport_complet(self, etat_agent, route_choisie=None, analyse_routes: Dict = None) -> str:
        """
        Génère un rapport complet du voyage avec design impeccable
        """
        print("   📝 Création du rapport détaillé avec design impeccable...")
        
        try:
            # Préparer les données du rapport
            donnees_rapport = self._preparer_donnees_rapport_premium(etat_agent, route_choisie, analyse_routes)
            
            # Générer le rapport HTML premium
            rapport_html = self._generer_rapport_html_premium(donnees_rapport)
            
            # Sauvegarder le rapport
            timestamp = int(time.time())
            nom_fichier = f"rapport_voyage_premium_{timestamp}.html"
            chemin_complet = os.path.join(self.rapports_dir, nom_fichier)
            
            with open(chemin_complet, 'w', encoding='utf-8') as f:
                f.write(rapport_html)
            
            print(f"   ✅ Rapport premium généré: {chemin_complet}")
            return chemin_complet
            
        except Exception as e:
            print(f"   ❌ Erreur génération rapport premium: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def _preparer_donnees_rapport_premium(self, etat_agent, route_choisie=None, analyse_routes: Dict = None) -> Dict[str, Any]:
        """
        Prépare les données pour le rapport premium
        """
        try:
            # Obtenir les statistiques de base
            stats = etat_agent.obtenir_statistiques() if hasattr(etat_agent, 'obtenir_statistiques') else {}
            
            # Préparer les données premium
            donnees = {
                "metadata": {
                    "ville": "Kinshasa",
                    "pays": "République Démocratique du Congo",
                    "date_generation": self.date_generation,
                    "agent_status": str(etat_agent.statut.value) if hasattr(etat_agent, 'statut') else "inconnu",
                    "route_choisie": self._get_route_choisie_nom(route_choisie),
                    "strategie": getattr(etat_agent, 'strategie', 'equilibre'),
                    "version_rapport": "3.0 - Premium"
                },
                "itineraire": {
                    "depart": "Place de la Victoire (Kalamu)",
                    "arrivee": "Gare Centrale (Gombe)",
                    "points_visites": self._get_points_visites_premium(etat_agent)
                },
                "statistiques": {
                    "distance_totale_km": float(stats.get("distance_totale_km", 0)),
                    "duree_totale_min": float(stats.get("duree_totale_min", 0)),
                    "nombre_trajets": int(stats.get("nombre_trajets", 0)),
                    "nombre_points_visites": len(self._get_points_visites_premium(etat_agent))
                },
                "trajets_detaille": self._preparer_trajets_detaille_premium(etat_agent),
                "analyse_routes": self._preparer_analyse_routes_premium(analyse_routes),
                "performance": self._calculer_metrics_performance_premium(stats)
            }
            
            # Ajouter les caractéristiques de la route choisie si disponibles
            if route_choisie and hasattr(route_choisie, 'caracteristiques'):
                donnees["route_choisie_caracteristiques"] = self._nettoyer_caracteristiques_premium(
                    route_choisie.caracteristiques
                )
            
            return donnees
            
        except Exception as e:
            print(f"   ❌ Erreur préparation données premium: {e}")
            return self._donnees_erreur_premium()
    
    def _get_points_visites_premium(self, etat_agent) -> List[str]:
        """Extrait la liste des points visités avec noms améliorés"""
        points_base = []
        if hasattr(etat_agent, 'historique_etats'):
            points_base = [str(point) for point in etat_agent.historique_etats]
        
        # Améliorer les noms des points principaux
        points_ameliore = []
        for point in points_base:
            if "victoire" in point.lower() or "echangeur" in point.lower():
                points_ameliore.append("Place de la Victoire (Kalamu)")
            elif "gare" in point.lower() and "centrale" in point.lower():
                points_ameliore.append("Gare Centrale (Gombe)")
            else:
                points_ameliore.append(point)
        
        return points_ameliore if points_ameliore else ["Place de la Victoire (Kalamu)", "Gare Centrale (Gombe)"]
    
    def _preparer_trajets_detaille_premium(self, etat_agent) -> List[Dict]:
        """Prépare les trajets détaillés premium"""
        trajets_detaille = []
        
        if not hasattr(etat_agent, 'trajets_effectues'):
            return trajets_detaille
        
        for i, trajet in enumerate(etat_agent.trajets_effectues):
            try:
                depart_nom = self._ameliorer_nom_point(trajet.depart.nom)
                arrivee_nom = self._ameliorer_nom_point(trajet.arrivee.nom)
                
                trajet_data = {
                    "segment": i + 1,
                    "depart": depart_nom,
                    "arrivee": arrivee_nom,
                    "distance_km": float(getattr(trajet, 'distance_km', 0)),
                    "duree_min": float(getattr(trajet, 'duree_estimee_min', 0))
                }
                trajets_detaille.append(trajet_data)
            except Exception as e:
                print(f"   ⚠️  Erreur trajet {i}: {e}")
                continue
        
        return trajets_detaille
    
    def _ameliorer_nom_point(self, nom_point: str) -> str:
        """Améliore le nom des points pour le rapport"""
        if "victoire" in nom_point.lower() or "echangeur" in nom_point.lower():
            return "Place de la Victoire"
        elif "gare" in nom_point.lower() and "centrale" in nom_point.lower():
            return "Gare Centrale"
        return nom_point
    
    def _preparer_analyse_routes_premium(self, analyse_routes: Dict) -> Dict:
        """Prépare une analyse premium des routes"""
        if not analyse_routes:
            return {}
        
        analyse_premium = {}
        for nom_route, data in analyse_routes.items():
            try:
                if isinstance(data, dict):
                    route_data = {
                        "score": float(data.get('score', 0)),
                        "distance_km": float(data.get('caracteristiques', {}).get('distance_km', 0)),
                        "temps_min": float(data.get('caracteristiques', {}).get('temps_estime_min', 0)),
                        "cout_usd": float(data.get('caracteristiques', {}).get('cout_essence_usd', data.get('caracteristiques', {}).get('cout_essence', 0))),
                        "embouteillages": float(data.get('caracteristiques', {}).get('niveau_embouteillage', 0)) * 100,
                        "securite": float(data.get('caracteristiques', {}).get('niveau_securite', 0)) * 100,
                        "confort": float(data.get('caracteristiques', {}).get('confort_route', 0)) * 100
                    }
                    analyse_premium[str(nom_route)] = route_data
            except Exception as e:
                print(f"   ⚠️  Erreur route {nom_route}: {e}")
                continue
        
        return analyse_premium
    
    def _calculer_metrics_performance_premium(self, stats: Dict) -> Dict:
        """Calcule des métriques de performance premium"""
        distance = stats.get("distance_totale_km", 0)
        duree = stats.get("duree_totale_min", 0)
        
        vitesse_moyenne = (distance / duree * 60) if duree > 0 else 0
        efficacite = min(distance / 10, 1.0)  # Normalisée
        
        return {
            "vitesse_moyenne_kmh": round(vitesse_moyenne, 1),
            "efficacite_parcours": round(efficacite, 2),
            "score_performance": round((vitesse_moyenne * efficacite) / 25, 2)
        }
    
    def _nettoyer_caracteristiques_premium(self, caracteristiques: Dict) -> Dict:
        """Nettoie les caractéristiques pour le rapport premium"""
        nettoyees = {}
        for key, value in caracteristiques.items():
            try:
                nettoyees[str(key)] = float(value)
            except (ValueError, TypeError):
                nettoyees[str(key)] = 0.0
        return nettoyees
    
    def _generer_rapport_html_premium(self, donnees: Dict[str, Any]) -> str:
        """
        Génère le rapport HTML avec design impeccable
        """
        try:
            # Générer les contenus premium
            contenu_header = self._generer_header_premium(donnees)
            contenu_stats = self._generer_stats_premium(donnees)
            contenu_analyse = self._generer_analyse_premium(donnees)
            contenu_itineraire = self._generer_itineraire_premium(donnees)
            contenu_trajets = self._generer_trajets_premium(donnees)
            
            html = self._creer_structure_html_premium(donnees, contenu_header, contenu_stats, contenu_analyse, contenu_itineraire, contenu_trajets)
            return html
            
        except Exception as e:
            print(f"   ❌ Erreur génération HTML premium: {e}")
            return self._html_erreur_premium(e)
    
    def _creer_structure_html_premium(self, donnees, header, stats, analyse, itineraire, trajets) -> str:
        """Crée la structure HTML premium"""
        
        return f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport Premium - Agent Véhicule Kinshasa</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #2c3e50;
            --secondary: #3498db;
            --success: #27ae60;
            --warning: #f39c12;
            --danger: #e74c3c;
            --light: #ecf0f1;
            --dark: #2c3e50;
            --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-success: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            --gradient-warning: linear-gradient(135deg, #f39c12 0%, #f1c40f 100%);
            --shadow: 0 10px 30px rgba(0,0,0,0.1);
            --shadow-hover: 0 15px 40px rgba(0,0,0,0.15);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            color: var(--dark);
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: var(--shadow);
            overflow: hidden;
            margin: 30px;
        }}
        
        .header-premium {{
            background: var(--gradient-primary);
            color: white;
            padding: 50px 40px;
            position: relative;
            overflow: hidden;
        }}
        
        .header-premium::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" opacity="0.1"><circle cx="50" cy="50" r="40" fill="white"/></svg>');
            background-size: 300px;
        }}
        
        .header-content {{
            position: relative;
            z-index: 2;
            text-align: center;
        }}
        
        .header-title {{
            font-size: 3em;
            font-weight: 700;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header-subtitle {{
            font-size: 1.4em;
            opacity: 0.9;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header-badges {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
            flex-wrap: wrap;
        }}
        
        .badge-premium {{
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
            padding: 12px 25px;
            border-radius: 25px;
            border: 1px solid rgba(255,255,255,0.3);
            font-weight: 500;
        }}
        
        .stats-grid-premium {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            padding: 40px;
            background: var(--light);
        }}
        
        .stat-card-premium {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            border-left: 5px solid var(--secondary);
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card-premium::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-primary);
        }}
        
        .stat-card-premium:hover {{
            transform: translateY(-10px);
            box-shadow: var(--shadow-hover);
        }}
        
        .stat-icon-premium {{
            font-size: 3em;
            margin-bottom: 20px;
            color: var(--secondary);
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .stat-number-premium {{
            font-size: 2.8em;
            font-weight: 700;
            margin: 15px 0;
            color: var(--primary);
        }}
        
        .stat-label-premium {{
            font-size: 1.1em;
            color: #7f8c8d;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .content-section {{
            padding: 40px;
        }}
        
        .section-title {{
            font-size: 2em;
            margin-bottom: 30px;
            color: var(--primary);
            border-bottom: 3px solid var(--secondary);
            padding-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .section-title i {{
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .routes-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
        }}
        
        .route-card-premium {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            border: 2px solid #e0e0e0;
            position: relative;
        }}
        
        .route-card-premium.gagnante {{
            border-color: var(--success);
            background: linear-gradient(135deg, #f8fff9 0%, #f0fff0 100%);
            box-shadow: 0 10px 30px rgba(39, 174, 96, 0.2);
        }}
        
        .route-card-premium:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
        }}
        
        .route-header-premium {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .route-nom-premium {{
            font-size: 1.4em;
            font-weight: 600;
            color: var(--primary);
            flex: 1;
        }}
        
        .route-score-premium {{
            background: var(--gradient-primary);
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 1.1em;
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        }}
        
        .route-stats-premium {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
        }}
        
        .route-stat-premium {{
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            transition: transform 0.2s ease;
        }}
        
        .route-stat-premium:hover {{
            transform: scale(1.05);
        }}
        
        .route-stat-valeur-premium {{
            font-size: 1.3em;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 5px;
        }}
        
        .route-stat-label-premium {{
            font-size: 0.9em;
            color: #7f8c8d;
            font-weight: 500;
        }}
        
        .progress-bar-premium {{
            width: 100%;
            height: 8px;
            background: #ecf0f1;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 8px;
        }}
        
        .progress-fill-premium {{
            height: 100%;
            background: var(--gradient-primary);
            border-radius: 10px;
            transition: width 1s ease-in-out;
        }}
        
        .itineraire-premium {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            border-left: 5px solid var(--secondary);
        }}
        
        .etape-premium {{
            display: flex;
            align-items: center;
            padding: 20px;
            margin: 10px 0;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-left: 4px solid var(--secondary);
        }}
        
        .etape-premium:hover {{
            transform: translateX(10px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        
        .etape-premium.depart {{ 
            border-left-color: var(--success);
            background: linear-gradient(135deg, #f8fff9 0%, white 100%);
        }}
        
        .etape-premium.arrivee {{ 
            border-left-color: var(--danger);
            background: linear-gradient(135deg, #fff8f8 0%, white 100%);
        }}
        
        .etape-numero-premium {{
            background: var(--secondary);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 20px;
            font-weight: 600;
            font-size: 1.1em;
            flex-shrink: 0;
        }}
        
        .etape-premium.depart .etape-numero-premium {{ 
            background: var(--success);
        }}
        
        .etape-premium.arrivee .etape-numero-premium {{ 
            background: var(--danger);
        }}
        
        .etape-nom-premium {{
            font-size: 1.1em;
            font-weight: 500;
            color: var(--primary);
        }}
        
        .table-premium {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: var(--shadow);
            border-radius: 10px;
            overflow: hidden;
        }}
        
        .table-premium th {{
            background: var(--gradient-primary);
            color: white;
            padding: 20px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.9em;
        }}
        
        .table-premium td {{
            padding: 18px 20px;
            border-bottom: 1px solid #ecf0f1;
            background: white;
        }}
        
        .table-premium tr:hover td {{
            background: #f8f9fa;
        }}
        
        .footer-premium {{
            text-align: center;
            padding: 40px;
            background: var(--primary);
            color: white;
            margin-top: 40px;
        }}
        
        .footer-premium p {{
            margin: 8px 0;
            opacity: 0.8;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                margin: 15px;
            }}
            
            .header-title {{
                font-size: 2.2em;
            }}
            
            .stats-grid-premium {{
                grid-template-columns: 1fr;
                padding: 25px;
            }}
            
            .routes-grid {{
                grid-template-columns: 1fr;
            }}
            
            .route-header-premium {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {header}
        
        <div class="stats-grid-premium">
            {stats}
        </div>
        
        <div class="content-section">
            <h2 class="section-title"><i class="fas fa-chart-bar"></i> Analyse Comparative des Routes</h2>
            <div class="routes-grid">
                {analyse}
            </div>
        </div>
        
        <div class="content-section">
            <h2 class="section-title"><i class="fas fa-route"></i> Itinéraire Complet</h2>
            {itineraire}
        </div>
        
        <div class="content-section">
            <h2 class="section-title"><i class="fas fa-list-ol"></i> Détail des Segments</h2>
            {trajets}
        </div>
        
        <div class="footer-premium">
            <p><i class="fas fa-robot"></i> Rapport généré automatiquement par l'Agent Véhicule Intelligent</p>
            <p>Version {donnees['metadata']['version_rapport']} | OpenStreetMap & Nominatim</p>
            <p>Kinshasa, République Démocratique du Congo</p>
        </div>
    </div>

    <script>
        // Animation des barres de progression
        document.addEventListener('DOMContentLoaded', function() {{
            const progressBars = document.querySelectorAll('.progress-fill-premium');
            progressBars.forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {{
                    bar.style.width = width;
                }}, 500);
            }});
            
            // Animation des cartes au défilement
            const observerOptions = {{
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            }};
            
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }}
                }});
            }}, observerOptions);
            
            // Observer les éléments animables
            document.querySelectorAll('.stat-card-premium, .route-card-premium, .etape-premium').forEach(el => {{
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(el);
            }});
        }});
    </script>
</body>
</html>
        """
    
    def _generer_header_premium(self, donnees: Dict[str, Any]) -> str:
        """Génère le header premium"""
        return f"""
        <div class="header-premium">
            <div class="header-content">
                <h1 class="header-title"><i class="fas fa-car"></i> RAPPORT DE VOYAGE PREMIUM</h1>
                <div class="header-subtitle">Agent Véhicule Intelligent - Système de Décision Multi-Routes</div>
                <div class="header-subtitle">Kinshasa, République Démocratique du Congo</div>
                <div class="header-badges">
                    <div class="badge-premium"><i class="fas fa-route"></i> {donnees['metadata']['route_choisie']}</div>
                    <div class="badge-premium"><i class="fas fa-chess-queen"></i> Stratégie: {donnees['metadata']['strategie']}</div>
                    <div class="badge-premium"><i class="fas fa-calendar"></i> {donnees['metadata']['date_generation']}</div>
                </div>
            </div>
        </div>
        """
    
    def _generer_stats_premium(self, donnees: Dict[str, Any]) -> str:
        """Génère les statistiques premium"""
        stats = donnees['statistiques']
        performance = donnees.get('performance', {})
        
        return f"""
        <div class="stat-card-premium">
            <div class="stat-icon-premium"><i class="fas fa-road"></i></div>
            <div class="stat-number-premium">{stats['distance_totale_km']:.1f} km</div>
            <div class="stat-label-premium">Distance Totale</div>
        </div>
        <div class="stat-card-premium">
            <div class="stat-icon-premium"><i class="fas fa-clock"></i></div>
            <div class="stat-number-premium">{formater_duree(stats['duree_totale_min'])}</div>
            <div class="stat-label-premium">Durée Totale</div>
        </div>
        <div class="stat-card-premium">
            <div class="stat-icon-premium"><i class="fas fa-map-marker-alt"></i></div>
            <div class="stat-number-premium">{stats['nombre_trajets']}</div>
            <div class="stat-label-premium">Segments</div>
        </div>
        <div class="stat-card-premium">
            <div class="stat-icon-premium"><i class="fas fa-tachometer-alt"></i></div>
            <div class="stat-number-premium">{performance.get('vitesse_moyenne_kmh', 0):.1f} km/h</div>
            <div class="stat-label-premium">Vitesse Moyenne</div>
        </div>
        """
    
    def _generer_analyse_premium(self, donnees: Dict[str, Any]) -> str:
        """Génère l'analyse premium des routes"""
        if not donnees.get('analyse_routes'):
            return """
            <div class="route-card-premium">
                <div class="route-header-premium">
                    <div class="route-nom-premium">Aucune analyse disponible</div>
                </div>
                <p>Les données d'analyse des routes ne sont pas disponibles.</p>
            </div>
            """
        
        contenu = ""
        route_choisie = donnees['metadata']['route_choisie']
        
        for nom_route, data in donnees['analyse_routes'].items():
            est_gagnante = nom_route == route_choisie
            classe = "route-card-premium gagnante" if est_gagnante else "route-card-premium"
            badge_gagnant = "<div style='background: #27ae60; color: white; padding: 8px 16px; border-radius: 15px; font-size: 0.9em; margin-left: 10px;'><i class='fas fa-trophy'></i> CHOISIE</div>" if est_gagnante else ""
            
            contenu += f"""
            <div class="{classe}">
                <div class="route-header-premium">
                    <div class="route-nom-premium">
                        {nom_route}
                        {badge_gagnant}
                    </div>
                    <div class="route-score-premium">Score: {data.get('score', 0):.3f}</div>
                </div>
                <div class="route-stats-premium">
                    <div class="route-stat-premium">
                        <div class="route-stat-valeur-premium">{formater_distance(data.get('distance_km', 0))}</div>
                        <div class="route-stat-label-premium">Distance</div>
                        <div class="progress-bar-premium">
                            <div class="progress-fill-premium" style="width: {min(data.get('distance_km', 0)/5*100, 100)}%"></div>
                        </div>
                    </div>
                    <div class="route-stat-premium">
                        <div class="route-stat-valeur-premium">{formater_duree(data.get('temps_min', 0))}</div>
                        <div class="route-stat-label-premium">Temps</div>
                        <div class="progress-bar-premium">
                            <div class="progress-fill-premium" style="width: {min(data.get('temps_min', 0)/30*100, 100)}%"></div>
                        </div>
                    </div>
                    <div class="route-stat-premium">
                        <div class="route-stat-valeur-premium">{data.get('cout_usd', 0):.2f} USD</div>
                        <div class="route-stat-label-premium">Coût</div>
                        <div class="progress-bar-premium">
                            <div class="progress-fill-premium" style="width: {min(data.get('cout_usd', 0)/3*100, 100)}%"></div>
                        </div>
                    </div>
                    <div class="route-stat-premium">
                        <div class="route-stat-valeur-premium">{data.get('embouteillages', 0):.1f}%</div>
                        <div class="route-stat-label-premium">Embouteillages</div>
                        <div class="progress-bar-premium">
                            <div class="progress-fill-premium" style="width: {data.get('embouteillages', 0)}%"></div>
                        </div>
                    </div>
                </div>
            </div>
            """
        
        return contenu
    
    def _generer_itineraire_premium(self, donnees: Dict[str, Any]) -> str:
        """Génère l'itinéraire premium"""
        points = donnees["itineraire"]["points_visites"]
        
        etapes_html = ""
        for i, point in enumerate(points):
            type_classe = "depart" if i == 0 else "arrivee" if i == len(points)-1 else ""
            icon = "🚗" if i == 0 else "🏁" if i == len(points)-1 else "📍"
            
            etapes_html += f"""
            <div class="etape-premium {type_classe}">
                <div class="etape-numero-premium">{icon}</div>
                <div class="etape-nom-premium">{point}</div>
            </div>
            """
        
        return f"""
        <div class="itineraire-premium">
            <h3 style="color: var(--primary); margin-bottom: 20px; font-size: 1.3em;">
                <i class="fas fa-route"></i> Parcours Complet - {len(points)} étapes
            </h3>
            {etapes_html}
        </div>
        """
    
    def _generer_trajets_premium(self, donnees: Dict[str, Any]) -> str:
        """Génère le tableau des trajets premium"""
        trajets = donnees['trajets_detaille']
        
        if not trajets:
            return "<p>Aucun détail de trajet disponible.</p>"
        
        lignes = ""
        for trajet in trajets:
            lignes += f"""
            <tr>
                <td>{trajet['segment']}</td>
                <td>{trajet['depart']}</td>
                <td>{trajet['arrivee']}</td>
                <td>{formater_distance(trajet['distance_km'])}</td>
                <td>{formater_duree(trajet['duree_min'])}</td>
            </tr>
            """
        
        return f"""
        <table class="table-premium">
            <thead>
                <tr>
                    <th>Segment</th>
                    <th>Départ</th>
                    <th>Arrivée</th>
                    <th>Distance</th>
                    <th>Durée</th>
                </tr>
            </thead>
            <tbody>
                {lignes}
            </tbody>
        </table>
        """
    
    # Méthodes utilitaires restantes...
    def _get_route_choisie_nom(self, route_choisie) -> str:
        if route_choisie and hasattr(route_choisie, 'nom'):
            return str(route_choisie.nom)
        return "Route Directe"
    
    def _donnees_erreur_premium(self) -> Dict[str, Any]:
        return {
            "metadata": {
                "ville": "Kinshasa", 
                "pays": "RDC",
                "date_generation": self.date_generation,
                "agent_status": "erreur",
                "route_choisie": "Inconnue",
                "strategie": "erreur",
                "version_rapport": "3.0 - Erreur"
            },
            "itineraire": {
                "depart": "Place de la Victoire (Kalamu)",
                "arrivee": "Gare Centrale (Gombe)", 
                "points_visites": ["Place de la Victoire (Kalamu)", "Gare Centrale (Gombe)"]
            },
            "statistiques": {
                "distance_totale_km": 0,
                "duree_totale_min": 0, 
                "nombre_trajets": 0,
                "nombre_points_visites": 2
            },
            "trajets_detaille": [],
            "analyse_routes": {},
            "performance": {"vitesse_moyenne_kmh": 0, "efficacite_parcours": 0, "score_performance": 0}
        }
    
    def _html_erreur_premium(self, erreur: Exception) -> str:
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Erreur Rapport</title></head>
        <body style="font-family: Arial; padding: 50px; text-align: center;">
            <h1 style="color: #e74c3c;">❌ Erreur lors de la génération du rapport</h1>
            <p>{str(erreur)}</p>
        </body>
        </html>
        """

# Instance globale
generateur_rapport = GenerateurRapport()