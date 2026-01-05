# services/prediction_service.py
"""
Service de prédiction
"""
import logging
from datetime import datetime
from models.ml_model import MLModel
from database.db_manager import DatabaseManager
from config.settings import APP_INFO

logger = logging.getLogger(__name__)

class PredictionService:
    """Service pour gérer les prédictions"""
    
    def __init__(self):
        """Initialise le service de prédiction"""
        self.ml_model = MLModel()
        self.db_manager = DatabaseManager()
        self.predictions_cache = []
        
        # Charger le modèle
        if not self.ml_model.load_model():
            logger.error("❌ Impossible de charger le modèle ML")
            raise Exception("Modèle ML non disponible")
        
        logger.info("✅ PredictionService initialisé")
    
    def predict(self, message, save_to_db=True):
        """
        Effectue une prédiction
        
        Args:
            message (str): Message à analyser
            save_to_db (bool): Sauvegarder dans la DB
            
        Returns:
            dict: Résultat de la prédiction
        """
        try:
            # Valider le message
            if not message or len(message.strip()) == 0:
                logger.warning("⚠️ Message vide")
                return None
            
            # Prédiction
            result = self.ml_model.predict(message)
            
            if result is None:
                logger.error("❌ Prédiction échouée")
                return None
            
            # Enrichir le résultat
            result['timestamp'] = datetime.now().isoformat()
            result['original_message'] = message
            result['model_version'] = APP_INFO['version']
            
            # Sauvegarder dans la DB
            if save_to_db:
                self.db_manager.add_prediction(
                    message=message,
                    cleaned_message=result['cleaned_message'],
                    prediction=result['prediction'],
                    confidence=result['confidence'],
                    ham_prob=result['probabilities']['ham'],
                    spam_prob=result['probabilities']['spam'],
                    model_version=APP_INFO['version']
                )
            
            # Cache
            self.predictions_cache.append(result)
            if len(self.predictions_cache) > 100:
                self.predictions_cache.pop(0)
            
            logger.info(f"✅ Prédiction: {'SPAM' if result['is_spam'] else 'HAM'}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la prédiction: {e}")
            self.db_manager.log_error('prediction_error', str(e))
            return None
    
    def predict_batch(self, messages, save_to_db=True):
        """
        Prédictions pour plusieurs messages
        
        Args:
            messages (list): Liste de messages
            save_to_db (bool): Sauvegarder dans la DB
            
        Returns:
            list: Liste de résultats
        """
        results = []
        for msg in messages:
            result = self.predict(msg, save_to_db)
            if result:
                results.append(result)
        
        logger.info(f"✅ Batch de {len(results)} prédictions effectuées")
        return results
    
    def get_recent_predictions(self, limit=10):
        """
        Récupère les prédictions récentes
        
        Args:
            limit (int): Nombre de prédictions
            
        Returns:
            list: Liste de prédictions
        """
        return self.db_manager.get_predictions(limit=limit)
    
    def get_model_info(self):
        """Retourne les informations du modèle"""
        return self.ml_model.get_model_info()