# services/statistics_service.py
"""
Service de statistiques
"""
import logging
from database.db_manager import DatabaseManager
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class StatisticsService:
    """Service pour gérer les statistiques"""
    
    def __init__(self):
        """Initialise le service de statistiques"""
        self.db_manager = DatabaseManager()
        logger.info("✅ StatisticsService initialisé")
    
    def get_global_statistics(self):
        """
        Récupère les statistiques globales
        
        Returns:
            dict: Statistiques globales
        """
        try:
            stats = self.db_manager.get_global_stats()
            
            # Calculer des métriques supplémentaires
            if stats.get('total_predictions', 0) > 0:
                stats['spam_percentage'] = (stats.get('total_spam', 0) / 
                                          stats['total_predictions']) * 100
                stats['ham_percentage'] = (stats.get('total_ham', 0) / 
                                         stats['total_predictions']) * 100
            else:
                stats['spam_percentage'] = 0
                stats['ham_percentage'] = 0
            
            logger.debug(f"Statistiques globales: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"❌ Erreur stats globales: {e}")
            return {}
    
    def get_daily_statistics(self, days=7):
        """
        Récupère les statistiques par jour
        
        Args:
            days (int): Nombre de jours
            
        Returns:
            list: Statistiques journalières
        """
        try:
            stats = self.db_manager.get_statistics(days=days)
            logger.debug(f"Statistiques sur {days} jours récupérées")
            return stats
        except Exception as e:
            logger.error(f"❌ Erreur stats journalières: {e}")
            return []
    
    def get_trend_analysis(self, days=7):
        """
        Analyse les tendances
        
        Args:
            days (int): Période d'analyse
            
        Returns:
            dict: Analyse des tendances
        """
        try:
            daily_stats = self.get_daily_statistics(days)
            
            if not daily_stats:
                return {'trend': 'stable', 'change': 0}
            
            # Calculer la tendance
            recent = daily_stats[:days//2]
            older = daily_stats[days//2:]
            
            recent_avg_spam = (sum(s.get('spam_count', 0) for s in recent) / 
                              len(recent) if recent else 0)
            older_avg_spam = (sum(s.get('spam_count', 0) for s in older) / 
                             len(older) if older else 0)
            
            change = ((recent_avg_spam - older_avg_spam) / 
                     max(older_avg_spam, 1)) * 100
            
            if change > 10:
                trend = 'increasing'
            elif change < -10:
                trend = 'decreasing'
            else:
                trend = 'stable'
            
            return {
                'trend': trend,
                'change': round(change, 2),
                'recent_avg': round(recent_avg_spam, 2),
                'older_avg': round(older_avg_spam, 2)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse de tendance: {e}")
            return {'trend': 'unknown', 'change': 0}
    
    def export_statistics(self, output_path, format='csv'):
        """
        Exporte les statistiques
        
        Args:
            output_path (str): Chemin de sortie
            format (str): Format d'export
            
        Returns:
            bool: Succès de l'export
        """
        try:
            if format == 'csv':
                return self.db_manager.export_to_csv(output_path)
            else:
                logger.warning(f"⚠️ Format non supporté: {format}")
                return False
        except Exception as e:
            logger.error(f"❌ Erreur export: {e}")
            return False