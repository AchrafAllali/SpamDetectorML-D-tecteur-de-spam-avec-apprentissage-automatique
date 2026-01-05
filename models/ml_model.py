# models/ml_model.py
"""
Module de gestion du modèle ML
"""
import pickle
import numpy as np
from pathlib import Path
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import logging

from config.settings import MODELS_DIR, MODEL_CONFIG
from .text_processor import TextProcessor

logger = logging.getLogger(__name__)

class MLModel:
    """Classe pour gérer le modèle de Machine Learning"""
    
    ALGORITHMS = {
        'naive_bayes': MultinomialNB,
        'logistic_regression': lambda: LogisticRegression(max_iter=1000),
        'svm': lambda: SVC(kernel='linear', probability=True)
    }
    
    def __init__(self, algorithm='naive_bayes'):
        """
        Initialise le modèle ML
        
        Args:
            algorithm (str): Type d'algorithme à utiliser
        """
        self.algorithm = algorithm
        self.model = None
        self.vectorizer = None
        self.text_processor = TextProcessor()
        self.is_trained = False
        self.metrics = {}
        
        logger.info(f"🤖 MLModel initialisé avec {algorithm}")
    
    def load_model(self, model_path=None, vectorizer_path=None):
        """
        Charge un modèle pré-entraîné
        
        Args:
            model_path (str): Chemin vers le modèle
            vectorizer_path (str): Chemin vers le vectorizer
        """
        try:
            model_path = model_path or MODELS_DIR / "spam_detector.pkl"
            vectorizer_path = vectorizer_path or MODELS_DIR / "vectorizer.pkl"
            
            # Charger le modèle
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            # Charger le vectorizer
            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            self.is_trained = True
            logger.info(f"✅ Modèle chargé depuis {model_path}")
            return True
            
        except FileNotFoundError as e:
            logger.error(f"❌ Fichier de modèle non trouvé: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement: {e}")
            return False
    
    def save_model(self, model_path=None, vectorizer_path=None):
        """
        Sauvegarde le modèle
        
        Args:
            model_path (str): Chemin de sauvegarde du modèle
            vectorizer_path (str): Chemin de sauvegarde du vectorizer
        """
        try:
            model_path = model_path or MODELS_DIR / "spam_detector.pkl"
            vectorizer_path = vectorizer_path or MODELS_DIR / "vectorizer.pkl"
            
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            with open(vectorizer_path, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            
            logger.info(f"✅ Modèle sauvegardé dans {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
    
    def train(self, X_train, y_train, X_test=None, y_test=None):
        """
        Entraîne le modèle
        
        Args:
            X_train: Données d'entraînement
            y_train: Labels d'entraînement
            X_test: Données de test (optionnel)
            y_test: Labels de test (optionnel)
        """
        try:
            logger.info(f"🚀 Début de l'entraînement ({self.algorithm})...")
            
            # Créer le vectorizer si nécessaire
            if self.vectorizer is None:
                self.vectorizer = TfidfVectorizer(
                    max_features=MODEL_CONFIG['max_features']
                )
                X_train_vec = self.vectorizer.fit_transform(X_train)
            else:
                X_train_vec = self.vectorizer.transform(X_train)
            
            # Créer et entraîner le modèle
            if self.algorithm in self.ALGORITHMS:
                algo_class = self.ALGORITHMS[self.algorithm]
                self.model = algo_class() if callable(algo_class) else algo_class
            else:
                logger.error(f"❌ Algorithme inconnu: {self.algorithm}")
                return False
            
            self.model.fit(X_train_vec, y_train)
            self.is_trained = True
            
            # Évaluer si données de test fournies
            if X_test is not None and y_test is not None:
                X_test_vec = self.vectorizer.transform(X_test)
                y_pred = self.model.predict(X_test_vec)
                
                self.metrics = {
                    'accuracy': accuracy_score(y_test, y_pred),
                    'precision': precision_score(y_test, y_pred),
                    'recall': recall_score(y_test, y_pred),
                    'f1': f1_score(y_test, y_pred)
                }
                
                logger.info(f"✅ Entraînement terminé - Accuracy: {self.metrics['accuracy']*100:.2f}%")
            else:
                logger.info("✅ Entraînement terminé")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'entraînement: {e}")
            return False
    
    def predict(self, message):
        """
        Prédit si un message est spam
        
        Args:
            message (str): Message à analyser
            
        Returns:
            dict: Résultat de la prédiction
        """
        if not self.is_trained:
            logger.error("❌ Modèle non entraîné")
            return None
        
        try:
            # Nettoyer le message
            cleaned = self.text_processor.clean_text(message)
            
            if not cleaned:
                logger.warning("⚠️ Message vide après nettoyage")
                return {
                    'prediction': 0,
                    'is_spam': False,
                    'confidence': 0.5,
                    'probabilities': {'ham': 0.5, 'spam': 0.5},
                    'cleaned_message': cleaned
                }
            
            # Vectoriser
            vectorized = self.vectorizer.transform([cleaned])
            
            # Prédire
            prediction = self.model.predict(vectorized)[0]
            probabilities = self.model.predict_proba(vectorized)[0]
            
            result = {
                'prediction': int(prediction),
                'is_spam': bool(prediction == 1),
                'confidence': float(probabilities[prediction]),
                'probabilities': {
                    'ham': float(probabilities[0]),
                    'spam': float(probabilities[1])
                },
                'cleaned_message': cleaned,
                'features': self.text_processor.extract_features(message)
            }
            
            logger.debug(f"Prédiction: {'SPAM' if result['is_spam'] else 'HAM'} "
                        f"({result['confidence']*100:.1f}%)")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la prédiction: {e}")
            return None
    
    def predict_batch(self, messages):
        """
        Prédit pour plusieurs messages
        
        Args:
            messages (list): Liste de messages
            
        Returns:
            list: Liste de résultats
        """
        return [self.predict(msg) for msg in messages]
    
    def get_metrics(self):
        """Retourne les métriques du modèle"""
        return self.metrics
    
    def get_model_info(self):
        """Retourne les informations du modèle"""
        return {
            'algorithm': self.algorithm,
            'is_trained': self.is_trained,
            'metrics': self.metrics,
            'max_features': MODEL_CONFIG['max_features']
        }