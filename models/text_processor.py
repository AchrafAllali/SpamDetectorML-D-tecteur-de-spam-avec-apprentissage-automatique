# models/text_processor.py
"""
Module de prétraitement de texte
"""
import re
import nltk
from nltk.corpus import stopwords
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    """Classe pour le prétraitement de texte"""
    
    def __init__(self, language='english'):
        """Initialise le processeur de texte"""
        self.language = language
        try:
            self.stop_words = set(stopwords.words(language))
            logger.info(f"✅ Stopwords chargés ({language})")
        except LookupError:
            logger.warning("⚠️ Stopwords non trouvés, téléchargement...")
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words(language))
    
    def clean_text(self, text):
        """
        Nettoie un texte pour le ML
        
        Args:
            text (str): Texte brut
            
        Returns:
            str: Texte nettoyé
        """
        if not text or not isinstance(text, str):
            logger.warning("⚠️ Texte vide ou invalide")
            return ""
        
        try:
            # Conversion en minuscules
            text = text.lower()
            
            # Suppression des URLs
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
            
            # Suppression des emails
            text = re.sub(r'\S+@\S+', '', text)
            
            # Suppression des caractères spéciaux et chiffres
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            
            # Suppression des espaces multiples
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Suppression des stopwords
            words = text.split()
            words = [word for word in words if word not in self.stop_words and len(word) > 2]
            
            cleaned = ' '.join(words)
            
            logger.debug(f"Texte nettoyé: '{text[:50]}...' -> '{cleaned[:50]}...'")
            return cleaned
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage: {e}")
            return text
    
    def clean_batch(self, texts):
        """
        Nettoie plusieurs textes
        
        Args:
            texts (list): Liste de textes
            
        Returns:
            list: Liste de textes nettoyés
        """
        return [self.clean_text(text) for text in texts]
    
    def get_word_count(self, text):
        """Compte les mots dans un texte"""
        return len(text.split())
    
    def get_char_count(self, text):
        """Compte les caractères dans un texte"""
        return len(text)
    
    def extract_features(self, text):
        """
        Extrait des features du texte
        
        Returns:
            dict: Dictionnaire de features
        """
        return {
            'word_count': self.get_word_count(text),
            'char_count': self.get_char_count(text),
            'avg_word_length': len(text) / max(self.get_word_count(text), 1),
            'has_url': bool(re.search(r'http|www', text.lower())),
            'has_email': bool(re.search(r'\S+@\S+', text)),
            'has_numbers': bool(re.search(r'\d', text)),
            'uppercase_ratio': sum(1 for c in text if c.isupper()) / max(len(text), 1)
        }