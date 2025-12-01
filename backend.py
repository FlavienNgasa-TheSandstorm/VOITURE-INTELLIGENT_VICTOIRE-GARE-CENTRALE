from flask import Flask, render_template
import os

app = Flask(__name__, static_folder='.', template_folder='.')

# Routes simples
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulation')
def simulation():
    return render_template('simulation.html')

@app.route('/apropos')
def apropos():
    return render_template('apropos.html')

# Servir les fichiers statiques
@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    print("🚀 Serveur Agent Véhicule - Version Simplifiée")
    print("📍 http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')