# config/settings.py
"""
Configuration centralisée de l'application
"""
import os
from pathlib import Path


# Chemins de base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"
DB_DIR = BASE_DIR / "database"
REPORTS_DIR = BASE_DIR / "reports"

# Créer les dossiers s'ils n'existent pas
for directory in [DATA_DIR, MODELS_DIR, LOGS_DIR, DB_DIR, REPORTS_DIR]:
    directory.mkdir(exist_ok=True)

# Configuration du modèle
MODEL_CONFIG = {
    'algorithm': 'naive_bayes',  # ou 'logistic_regression', 'svm'
    'max_features': 3000,
    'test_size': 0.2,
    'random_state': 42,
    'min_accuracy': 0.95  # Seuil minimum accepté
}

# Configuration de la base de données
DATABASE_CONFIG = {
    'db_path': DB_DIR / "spam_detector.db",
    'backup_enabled': True,
    'backup_interval': 24  # heures
}

# Configuration du logging
LOGGING_CONFIG = {
    'log_file': LOGS_DIR / "app.log",
    'max_bytes': 10 * 1024 * 1024,  # 10 MB
    'backup_count': 5,
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# Configuration de l'interface
UI_CONFIG = {
    'theme': 'light',  # 'light' ou 'dark'
    'language': 'fr',  # 'fr' ou 'en'
    'window_size': '900x750',
    'font_family': 'Arial',
    'font_size': 11
}

# Configuration des couleurs (thème clair)
COLORS_LIGHT = {
    'bg': '#f0f0f0',
    'primary': '#2196F3',
    'secondary': '#757575',
    'success': '#4CAF50',
    'danger': '#f44336',
    'warning': '#FF9800',
    'text': '#333333',
    'white': '#FFFFFF'
}

# Configuration des couleurs (thème sombre)
COLORS_DARK = {
    'bg': '#1e1e1e',
    'primary': '#2196F3',
    'secondary': '#9e9e9e',
    'success': '#66bb6a',
    'danger': '#ef5350',
    'warning': '#ffa726',
    'text': '#e0e0e0',
    'white': '#121212'
}

# Langues disponibles
TRANSLATIONS = {
    'fr': {
        'app_title': '🔮 Détecteur de Spam Professionnel',
        'analyze_btn': '🔍 Analyser',
        'clear_btn': '🗑️ Effacer',
        'example_btn': '💡 Exemple',
        'spam_detected': '🚨 SPAM DÉTECTÉ !',
        'ham_detected': '✅ MESSAGE LÉGITIME',
        'confidence': 'Confiance',
        'history': 'Historique',
        'statistics': 'Statistiques',
        'settings': 'Paramètres',
        'export': 'Exporter',
    },
    'en': {
        'app_title': '🔮 Professional Spam Detector',
        'analyze_btn': '🔍 Analyze',
        'clear_btn': '🗑️ Clear',
        'example_btn': '💡 Example',
        'spam_detected': '🚨 SPAM DETECTED!',
        'ham_detected': '✅ LEGITIMATE MESSAGE',
        'confidence': 'Confidence',
        'history': 'History',
        'statistics': 'Statistics',
        'settings': 'Settings',
        'export': 'Export',
    }
}

# Configuration de sécurité
SECURITY_CONFIG = {
    'max_message_length': 10000,  # Nombre max de caractères
    'rate_limit': 100,  # Analyses max par heure
    'enable_sanitization': True
}

# Configuration des exports
EXPORT_CONFIG = {
    'formats': ['csv', 'json', 'pdf'],
    'default_format': 'csv',
    'include_metadata': True
}

# Métadonnées de l'application
APP_INFO = {
    'name': 'Spam Detector Pro',
    'version': '2.0.0',
    'author': 'Achraf',
    'description': 'Système professionnel de détection de spam avec ML',
    'license': 'MIT'
}

# Mode développement
DEBUG = os.getenv('DEBUG', 'False') == 'True'

def get_colors():
    """Retourne les couleurs selon le thème actif"""
    return COLORS_DARK if UI_CONFIG['theme'] == 'dark' else COLORS_LIGHT

def get_translation(key):
    """Retourne la traduction selon la langue active"""
    lang = UI_CONFIG['language']
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)