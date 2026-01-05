# controllers/app_controller.py
"""
Contrôleur principal de l'application
"""
import logging
from services import PredictionService, StatisticsService

logger = logging.getLogger(__name__)

class AppController:
    """Contrôleur principal de l'application"""
    
    def __init__(self):
        """Initialise le contrôleur"""
        logger.info("🎮 Initialisation du contrôleur...")
        
        # Services
        self.prediction_service = PredictionService()
        self.statistics_service = StatisticsService()
        
        logger.info("✅ Contrôleur initialisé")
    
    def get_prediction_service(self):
        """Retourne le service de prédiction"""
        return self.prediction_service
    
    def get_statistics_service(self):
        """Retourne le service de statistiques"""
        return self.statistics_service
    
    def shutdown(self):
        """Arrêt propre de l'application"""
        logger.info("👋 Arrêt de l'application...")
        # Cleanup si nécessaire
        logger.info("✅ Application arrêtée")