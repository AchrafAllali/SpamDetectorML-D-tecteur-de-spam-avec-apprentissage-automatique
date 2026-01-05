# main.py
"""
Point d'entrée de l'application
Spam Detector Pro v2.0
"""
import sys
import logging
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

# IMPORTANT: Charger le config_manager AVANT tout
from config.config_manager import config_manager
print(f"🔧 Configuration chargée: {len(config_manager.user_settings)} paramètres")

from utils.logger import setup_logger
from views.main_window import MainWindow
from config.settings import APP_INFO

# Configurer le logger
logger = setup_logger()

def main():
    """Fonction principale"""
    try:
        logger.info("="*60)
        logger.info(f"🚀 Démarrage de {APP_INFO['name']} v{APP_INFO['version']}")
        logger.info(f"🔧 Paramètres: {len(config_manager.user_settings)} chargés")
        logger.info("="*60)
        
        # Créer et lancer l'application
        app = MainWindow()
        
        logger.info("✅ Application lancée avec succès")
        
        # Boucle principale
        app.mainloop()
        
    except Exception as e:
        logger.critical(f"❌ ERREUR CRITIQUE: {e}", exc_info=True)
        import tkinter.messagebox as mb
        mb.showerror(
            "Erreur Critique",
            f"Une erreur critique est survenue:\n\n{str(e)}\n\n"
            "Consultez les logs pour plus de détails."
        )
        sys.exit(1)
    
    finally:
        logger.info("="*60)
        logger.info("👋 Application terminée")
        logger.info("="*60)

if __name__ == "__main__":
    main()