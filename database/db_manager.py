# database/db_manager.py
"""
Gestionnaire de base de données SQLite
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import logging
from config.settings import DATABASE_CONFIG

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path=None):
        """Initialise la connexion à la base de données"""
        self.db_path = db_path or DATABASE_CONFIG['db_path']
        self.conn = None
        self.cursor = None
        self._create_tables()
    
    def connect(self):
        """Établit la connexion à la base de données"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            logger.info(f"✅ Connexion à la base de données établie: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"❌ Erreur de connexion à la base de données: {e}")
            raise
    
    def close(self):
        """Ferme la connexion à la base de données"""
        if self.conn:
            self.conn.close()
            logger.info("✅ Connexion à la base de données fermée")
    
    def _create_tables(self):
        """Crée les tables si elles n'existent pas"""
        self.connect()
        
        # Table des prédictions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                cleaned_message TEXT,
                prediction INTEGER NOT NULL,
                confidence REAL NOT NULL,
                ham_probability REAL NOT NULL,
                spam_probability REAL NOT NULL,
                model_version TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des statistiques
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                total_predictions INTEGER DEFAULT 0,
                spam_count INTEGER DEFAULT 0,
                ham_count INTEGER DEFAULT 0,
                avg_confidence REAL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des modèles
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version TEXT NOT NULL UNIQUE,
                algorithm TEXT NOT NULL,
                accuracy REAL NOT NULL,
                precision_score REAL NOT NULL,
                recall_score REAL NOT NULL,
                f1_score REAL NOT NULL,
                training_date DATETIME NOT NULL,
                is_active INTEGER DEFAULT 0,
                metadata TEXT
            )
        ''')
        
        # Table de configuration
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des logs d'erreurs
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS error_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                stack_trace TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        logger.info("✅ Tables de la base de données créées/vérifiées")
    
    def add_prediction(self, message, cleaned_message, prediction, 
                      confidence, ham_prob, spam_prob, model_version='2.0.0'):
        """Ajoute une prédiction à l'historique"""
        try:
            self.connect()
            self.cursor.execute('''
                INSERT INTO predictions 
                (message, cleaned_message, prediction, confidence, 
                 ham_probability, spam_probability, model_version)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (message, cleaned_message, prediction, confidence, 
                  ham_prob, spam_prob, model_version))
            self.conn.commit()
            
            # Mettre à jour les statistiques
            self._update_daily_stats()
            
            logger.info(f"✅ Prédiction enregistrée: {prediction}")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"❌ Erreur lors de l'enregistrement: {e}")
            return None
        finally:
            self.close()
    
    def get_predictions(self, limit=50, offset=0):
        """Récupère l'historique des prédictions"""
        try:
            self.connect()
            self.cursor.execute('''
                SELECT * FROM predictions 
                ORDER BY timestamp DESC 
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            results = self.cursor.fetchall()
            return [dict(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"❌ Erreur lors de la récupération: {e}")
            return []
        finally:
            self.close()
    
    def get_statistics(self, days=7):
        """Récupère les statistiques sur N jours"""
        try:
            self.connect()
            self.cursor.execute('''
                SELECT 
                    DATE(timestamp) as date,
                    COUNT(*) as total,
                    SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) as spam_count,
                    SUM(CASE WHEN prediction = 0 THEN 1 ELSE 0 END) as ham_count,
                    AVG(confidence) as avg_confidence
                FROM predictions
                WHERE timestamp >= DATE('now', '-' || ? || ' days')
                GROUP BY DATE(timestamp)
                ORDER BY date DESC
            ''', (days,))
            results = self.cursor.fetchall()
            return [dict(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"❌ Erreur statistiques: {e}")
            return []
        finally:
            self.close()
    
    def get_global_stats(self):
        """Récupère les statistiques globales"""
        try:
            self.connect()
            self.cursor.execute('''
                SELECT 
                    COUNT(*) as total_predictions,
                    SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) as total_spam,
                    SUM(CASE WHEN prediction = 0 THEN 1 ELSE 0 END) as total_ham,
                    AVG(confidence) as avg_confidence,
                    AVG(CASE WHEN prediction = 1 THEN confidence ELSE NULL END) as avg_spam_confidence,
                    AVG(CASE WHEN prediction = 0 THEN confidence ELSE NULL END) as avg_ham_confidence
                FROM predictions
            ''')
            result = self.cursor.fetchone()
            return dict(result) if result else {}
        except sqlite3.Error as e:
            logger.error(f"❌ Erreur stats globales: {e}")
            return {}
        finally:
            self.close()
    
    def _update_daily_stats(self):
        """Met à jour les statistiques du jour"""
        try:
            today = datetime.now().date()
            self.cursor.execute('''
                INSERT OR REPLACE INTO statistics (date, total_predictions, spam_count, ham_count, avg_confidence)
                SELECT 
                    DATE('now') as date,
                    COUNT(*) as total,
                    SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) as spam,
                    SUM(CASE WHEN prediction = 0 THEN 1 ELSE 0 END) as ham,
                    AVG(confidence) as avg_conf
                FROM predictions
                WHERE DATE(timestamp) = DATE('now')
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"❌ Erreur mise à jour stats: {e}")
    
    def add_model_info(self, version, algorithm, accuracy, precision, 
                      recall, f1, metadata=None):
        """Enregistre les informations d'un modèle"""
        try:
            self.connect()
            self.cursor.execute('''
                INSERT INTO models 
                (version, algorithm, accuracy, precision_score, recall_score, 
                 f1_score, training_date, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (version, algorithm, accuracy, precision, recall, f1,
                  datetime.now(), json.dumps(metadata) if metadata else None))
            self.conn.commit()
            logger.info(f"✅ Modèle {version} enregistré")
            return True
        except sqlite3.Error as e:
            logger.error(f"❌ Erreur enregistrement modèle: {e}")
            return False
        finally:
            self.close()
    
    def log_error(self, error_type, error_message, stack_trace=None):
        """Enregistre une erreur"""
        try:
            self.connect()
            self.cursor.execute('''
                INSERT INTO error_logs (error_type, error_message, stack_trace)
                VALUES (?, ?, ?)
            ''', (error_type, error_message, stack_trace))
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"❌ Erreur lors du log d'erreur: {e}")
        finally:
            self.close()
    
    def export_to_csv(self, output_path, days=30):
        """Exporte les prédictions en CSV"""
        import csv
        try:
            predictions = self.get_predictions(limit=10000)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                if predictions:
                    writer = csv.DictWriter(f, fieldnames=predictions[0].keys())
                    writer.writeheader()
                    writer.writerows(predictions)
            
            logger.info(f"✅ Export CSV créé: {output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur export CSV: {e}")
            return False
    
    def clear_old_data(self, days=90):
        """Supprime les données plus anciennes que N jours"""
        try:
            self.connect()
            self.cursor.execute('''
                DELETE FROM predictions 
                WHERE timestamp < DATE('now', '-' || ? || ' days')
            ''', (days,))
            deleted = self.cursor.rowcount
            self.conn.commit()
            logger.info(f"✅ {deleted} anciennes prédictions supprimées")
            return deleted
        except sqlite3.Error as e:
            logger.error(f"❌ Erreur nettoyage: {e}")
            return 0
        finally:
            self.close()