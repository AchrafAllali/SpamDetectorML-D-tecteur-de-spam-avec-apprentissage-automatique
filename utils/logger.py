# utils/logger.py
"""
Configuration du système de logging
"""
import logging
import logging.handlers
from pathlib import Path
from config.settings import LOGGING_CONFIG, LOGS_DIR

def setup_logger(name='spam_detector'):
    """
    Configure le logger principal de l'application
    """
    # Créer le logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOGGING_CONFIG['level']))
    
    # Éviter la duplication des handlers
    if logger.handlers:
        return logger
    
    # Format des logs
    formatter = logging.Formatter(LOGGING_CONFIG['format'])
    
    # Handler pour fichier (avec rotation)
    file_handler = logging.handlers.RotatingFileHandler(
        LOGGING_CONFIG['log_file'],
        maxBytes=LOGGING_CONFIG['max_bytes'],
        backupCount=LOGGING_CONFIG['backup_count'],
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Handler pour console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Ajouter les handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("="*60)
    logger.info("🚀 Application démarrée")
    logger.info("="*60)
    
    return logger

# Logger global
app_logger = setup_logger()