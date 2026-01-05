# utils/translations.py
"""
Gestion des traductions dynamiques
"""
import logging
from config.config_manager import config_manager

logger = logging.getLogger(__name__)

class TranslationManager:
    """Gère les traductions de l'interface"""
    
    def __init__(self):
        self.current_language = config_manager.get_setting('language', 'fr')
        self.translations = {}
        self.load_translations()
        
        # S'abonner aux changements de langue
        config_manager.register_callback('language', self.on_language_changed)
    
    def load_translations(self):
        """Charge les traductions depuis settings.py"""
        from config.settings import TRANSLATIONS
        self.translations = TRANSLATIONS
    
    def on_language_changed(self, new_language):
        """Callback quand la langue change"""
        logger.info(f"🌐 Changement de langue: {self.current_language} -> {new_language}")
        self.current_language = new_language
    
    def get(self, key, default=None):
        """Récupère une traduction"""
        lang = self.current_language
        if lang in self.translations and key in self.translations[lang]:
            return self.translations[lang][key]
        elif 'fr' in self.translations and key in self.translations['fr']:
            return self.translations['fr'][key]
        return default or key
    
    def update_ui_widgets(self, widgets_dict):
        """Met à jour les widgets UI avec les nouvelles traductions"""
        for widget, key in widgets_dict.items():
            try:
                if hasattr(widget, 'config'):
                    widget.config(text=self.get(key))
                elif hasattr(widget, 'set'):
                    widget.set(self.get(key))
                logger.debug(f"📝 Widget mis à jour: {key} -> {self.get(key)}")
            except Exception as e:
                logger.error(f"❌ Erreur mise à jour widget {key}: {e}")

# Instance globale
translation_manager = TranslationManager()