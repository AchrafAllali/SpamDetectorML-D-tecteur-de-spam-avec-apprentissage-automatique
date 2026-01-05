# config/config_manager.py
"""
Gestionnaire de configuration
"""
import json
import logging
from pathlib import Path
from .settings import BASE_DIR, UI_CONFIG, MODEL_CONFIG, DATABASE_CONFIG, TRANSLATIONS

logger = logging.getLogger(__name__)

class ConfigManager:
    """Gère la configuration de l'application"""
    
    def __init__(self):
        self.user_settings_path = BASE_DIR / "config" / "user_settings.json"
        self.user_settings = {}
        self.callbacks = {}  # Pour les callbacks dynamiques
        self.load_settings()
    
    def load_settings(self):
        """Charge les paramètres depuis le fichier JSON"""
        try:
            if self.user_settings_path.exists():
                with open(self.user_settings_path, 'r', encoding='utf-8') as f:
                    self.user_settings = json.load(f)
                
                logger.info(f"✅ {len(self.user_settings)} paramètres chargés")
            else:
                logger.info("ℹ️ Aucun paramètre utilisateur trouvé")
                self.user_settings = {}
                
        except Exception as e:
            logger.error(f"❌ Erreur chargement paramètres: {e}")
            self.user_settings = {}
    
    def save_settings(self, settings):
        """Sauvegarde les paramètres dans le fichier JSON"""
        try:
            # Mettre à jour les paramètres actuels
            self.user_settings.update(settings)
            
            # Sauvegarder dans le fichier
            with open(self.user_settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.user_settings, f, indent=2, ensure_ascii=False)
            
            # Appliquer les changements dynamiquement
            self.apply_dynamic_settings(settings)
            
            logger.info(f"✅ {len(settings)} paramètres sauvegardés")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde paramètres: {e}")
            return False
    
    def apply_dynamic_settings(self, settings):
        """Applique certains paramètres dynamiquement (sans redémarrage)"""
        for key, value in settings.items():
            if key in ['language', 'font_size']:
                # Ces paramètres peuvent être appliqués dynamiquement
                UI_CONFIG[key] = value
                logger.info(f"🔧 {key} appliqué dynamiquement: {value}")
            
            # Appeler les callbacks enregistrés
            if key in self.callbacks:
                for callback in self.callbacks[key]:
                    callback(value)
    
    def register_callback(self, key, callback):
        """Enregistre un callback pour un paramètre spécifique"""
        if key not in self.callbacks:
            self.callbacks[key] = []
        self.callbacks[key].append(callback)
    
    def get_setting(self, key, default=None):
        """Récupère un paramètre"""
        return self.user_settings.get(key, default)
    
    def get_ui_config(self):
        """Récupère la configuration UI avec les paramètres utilisateur"""
        config = UI_CONFIG.copy()
        # Écraser avec les paramètres utilisateur
        for key in ['theme', 'language', 'font_size']:
            if key in self.user_settings:
                config[key] = self.user_settings[key]
        return config
    
    def get_model_config(self):
        """Récupère la configuration du modèle avec les paramètres utilisateur"""
        config = MODEL_CONFIG.copy()
        for key in ['algorithm', 'max_features', 'min_accuracy']:
            if key in self.user_settings:
                config[key] = self.user_settings[key]
        return config
    
    def reset_settings(self):
        """Réinitialise tous les paramètres"""
        try:
            if self.user_settings_path.exists():
                self.user_settings_path.unlink()
            
            self.user_settings = {}
            logger.info("✅ Paramètres réinitialisés")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur réinitialisation: {e}")
            return False

# Instance globale
config_manager = ConfigManager()