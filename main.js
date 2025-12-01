// Navigation mobile
class Navigation {
    constructor() {
        this.navToggle = document.querySelector('.nav-toggle');
        this.navMenu = document.querySelector('.nav-menu');
        this.init();
    }

    init() {
        if (this.navToggle) {
            this.navToggle.addEventListener('click', () => this.toggleMenu());
        }

        // Fermer le menu en cliquant sur un lien
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => this.closeMenu());
        });

        // Fermer le menu en cliquant à l'extérieur
        document.addEventListener('click', (e) => {
            if (!this.navToggle.contains(e.target) && !this.navMenu.contains(e.target)) {
                this.closeMenu();
            }
        });
    }

    toggleMenu() {
        this.navMenu.classList.toggle('active');
        this.navToggle.classList.toggle('active');
    }

    closeMenu() {
        this.navMenu.classList.remove('active');
        this.navToggle.classList.remove('active');
    }
}

// Animations au défilement
class ScrollAnimations {
    constructor() {
        this.elements = document.querySelectorAll('.feature-card, .stat-card, .route-card');
        this.init();
    }

    init() {
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        this.elements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            this.observer.observe(el);
        });
    }
}

// Gestionnaire de thème
class ThemeManager {
    constructor() {
        this.themeToggle = document.createElement('button');
        this.init();
    }

    init() {
        this.createThemeToggle();
        this.loadTheme();
    }

    createThemeToggle() {
        this.themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        this.themeToggle.className = 'theme-toggle';
        this.themeToggle.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--secondary);
            color: white;
            border: none;
            cursor: pointer;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            box-shadow: var(--shadow);
        `;

        this.themeToggle.addEventListener('click', () => this.toggleTheme());
        document.body.appendChild(this.themeToggle);
    }

    toggleTheme() {
        document.body.classList.toggle('dark-theme');
        const isDark = document.body.classList.contains('dark-theme');
        this.themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
            this.themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        }
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    new Navigation();
    new ScrollAnimations();
    new ThemeManager();

    // Ajouter des styles pour le mode sombre
    const darkThemeStyles = `
        <style>
            body.dark-theme {
                background: #1a1a1a;
                color: #e0e0e0;
            }
            
            body.dark-theme .navbar {
                background: #2d2d2d;
            }
            
            body.dark-theme .feature-card,
            body.dark-theme .stat-card,
            body.dark-theme .route-card {
                background: #2d2d2d;
                color: #e0e0e0;
            }
            
            body.dark-theme .footer {
                background: #2d2d2d;
            }
        </style>
    `;
    document.head.insertAdjacentHTML('beforeend', darkThemeStyles);
});

// Gestion des erreurs globales
window.addEventListener('error', (e) => {
    console.error('Erreur globale:', e.error);
});

// Amélioration de l'UX pour les formulaires
document.addEventListener('DOMContentLoaded', () => {
    // Ajouter des indicateurs de chargement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Chargement...';
                submitBtn.disabled = true;
            }
        });
    });
});