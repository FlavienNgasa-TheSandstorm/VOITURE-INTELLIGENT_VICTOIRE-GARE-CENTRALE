class SimulationManager {
    constructor() {
        this.currentStrategy = 'rapide';
        this.isRunning = false;
        this.initializeEventListeners();
        this.chargerStatutFichiers();
    }

    initializeEventListeners() {
        // Gestion des stratégies
        document.querySelectorAll('.strategy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setStrategy(e.target.closest('.strategy-btn'));
            });
        });

        // Lancement de la simulation
        document.getElementById('lancerSimulation').addEventListener('click', () => {
            this.lancerSimulation();
        });
    }

    setStrategy(button) {
        document.querySelectorAll('.strategy-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        button.classList.add('active');
        this.currentStrategy = button.dataset.strategy;
        console.log(`🎯 Stratégie choisie: ${this.currentStrategy}`);
    }

    async chargerStatutFichiers() {
        try {
            const response = await fetch('/api/etat-fichiers');
            const data = await response.json();
            
            this.afficherStatutFichiers(data);
            this.mettreAJourLiens(data);
            
        } catch (error) {
            console.error('Erreur chargement statut:', error);
            this.afficherStatutFichiers({
                carte_itineraire: false,
                carte_multi_routes: false,
                rapports: []
            });
        }
    }

    afficherStatutFichiers(data) {
        const fileStatus = document.getElementById('fileStatus');
        
        const statuts = [
            {
                nom: 'Carte Itinéraire',
                disponible: data.carte_itineraire,
                icone: 'fa-route',
                description: 'Route optimale choisie'
            },
            {
                nom: 'Carte Multi-Routes', 
                disponible: data.carte_multi_routes,
                icone: 'fa-map-marked-alt',
                description: 'Comparaison des routes'
            },
            {
                nom: 'Rapports',
                disponible: data.nombre_rapports > 0,
                icone: 'fa-file-alt',
                description: `${data.nombre_rapports} rapport(s) généré(s)`
            }
        ];
        
        fileStatus.innerHTML = statuts.map(statut => `
            <div class="status-card ${statut.disponible ? 'available' : 'unavailable'}">
                <div class="status-icon">
                    <i class="fas ${statut.icone}"></i>
                </div>
                <h4>${statut.nom}</h4>
                <p>${statut.description}</p>
                <div class="status-indicator">
                    ${statut.disponible ? 
                        '<span style="color: #27ae60;"><i class="fas fa-check-circle"></i> Disponible</span>' : 
                        '<span style="color: #e74c3c;"><i class="fas fa-times-circle"></i> Non généré</span>'
                    }
                </div>
            </div>
        `).join('');
    }

    mettreAJourLiens(data) {
        const lienItineraire = document.getElementById('lienItineraire');
        const lienMultiRoutes = document.getElementById('lienMultiRoutes');
        
        if (data.carte_itineraire) {
            lienItineraire.classList.remove('btn-secondary');
            lienItineraire.classList.add('btn-primary');
            lienItineraire.innerHTML = '<i class="fas fa-external-link-alt"></i> Voir la Carte Itinéraire';
        } else {
            lienItineraire.classList.remove('btn-primary');
            lienItineraire.classList.add('btn-secondary');
            lienItineraire.innerHTML = '<i class="fas fa-clock"></i> En attente de génération';
            lienItineraire.removeAttribute('href');
        }
        
        if (data.carte_multi_routes) {
            lienMultiRoutes.classList.remove('btn-secondary');
            lienMultiRoutes.classList.add('btn-primary');
            lienMultiRoutes.innerHTML = '<i class="fas fa-external-link-alt"></i> Voir Toutes les Routes';
        } else {
            lienMultiRoutes.classList.remove('btn-primary');
            lienMultiRoutes.classList.add('btn-secondary');
            lienMultiRoutes.innerHTML = '<i class="fas fa-clock"></i> En attente de génération';
            lienMultiRoutes.removeAttribute('href');
        }
    }

    async lancerSimulation() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        const btn = document.getElementById('lancerSimulation');
        const texteOriginal = btn.innerHTML;
        
        // Désactiver le bouton et montrer le chargement
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Génération en cours...';
        btn.disabled = true;

        try {
            this.afficherNotification("🚀 Démarrage de la simulation...", 'info');
            
            const response = await this.appelerBackend();
            
            if (response.success) {
                this.afficherNotification("✅ Simulation terminée avec succès!", 'success');
                
                // Attendre 2 secondes puis recharger le statut
                setTimeout(() => {
                    this.chargerStatutFichiers();
                    this.afficherNotification("🗺️ Cartes générées! Cliquez sur les liens pour les visualiser.", 'success');
                }, 2000);
                
            } else {
                throw new Error(response.message || 'Erreur inconnue lors de la simulation');
            }
            
        } catch (error) {
            console.error('Erreur simulation:', error);
            this.afficherNotification(`❌ Erreur: ${error.message}`, 'error');
        } finally {
            this.isRunning = false;
            btn.innerHTML = texteOriginal;
            btn.disabled = false;
        }
    }

    async appelerBackend() {
        console.log(`📤 Envoi requête simulation avec stratégie: ${this.currentStrategy}`);
        
        const response = await fetch('/api/simulation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                strategie: this.currentStrategy
            })
        });

        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }

        const data = await response.json();
        console.log('📥 Réponse simulation:', data);
        return data;
    }

    afficherNotification(message, type = 'info') {
        // Supprimer les notifications existantes
        document.querySelectorAll('.notification-floating').forEach(n => n.remove());
        
        const notification = document.createElement('div');
        notification.className = `notification-floating notification-${type}`;
        
        const backgroundColor = type === 'error' ? '#e74c3c' : 
                              type === 'success' ? '#27ae60' : '#3498db';
        
        notification.innerHTML = `
            <div style="position: fixed; top: 100px; right: 20px; background: ${backgroundColor}; 
                       color: white; padding: 15px 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); 
                       z-index: 10000; max-width: 400px; font-size: 14px;">
                ${message}
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-suppression après 5 secondes
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    new SimulationManager();
    console.log('🚀 SimulationManager initialisé');
});