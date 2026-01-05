# utils/auto_updater.py
"""
Mise à jour automatique de l'interface
"""
import tkinter as tk
import logging
from config.config_manager import config_manager

logger = logging.getLogger(__name__)

class AutoUpdater:
    """Met à jour automatiquement l'interface quand les paramètres changent"""
    
    def __init__(self):
        self.widgets_to_update = {}
    
    def register_widget(self, widget_type, widget, setting_key):
        """Enregistre un widget pour mise à jour automatique"""
        if setting_key not in self.widgets_to_update:
            self.widgets_to_update[setting_key] = []
        
        self.widgets_to_update[setting_key].append((widget_type, widget))
        
        # S'abonner aux changements
        config_manager.register_callback(setting_key, 
                                        lambda value, w=widget, t=widget_type: 
                                        self.update_widget(t, w, setting_key, value))
    
    def update_widget(self, widget_type, widget, setting_key, value):
        """Met à jour un widget spécifique"""
        try:
            if widget_type == 'label':
                if setting_key == 'language':
                    # Les labels seront mis à jour via TranslationManager
                    pass
                elif setting_key == 'font_size':
                    current_font = widget.cget('font')
                    # Extraire la famille de police et garder le style
                    font_parts = current_font.split()
                    if len(font_parts) >= 2:
                        font_family = font_parts[0]
                        new_font = (font_family, int(value))
                        widget.config(font=new_font)
            
            elif widget_type == 'button':
                # Similaire aux labels
                pass
                
            logger.debug(f"🔄 Widget {widget_type} mis à jour pour {setting_key}: {value}")
            
        except Exception as e:
            logger.error(f"❌ Erreur mise à jour widget: {e}")