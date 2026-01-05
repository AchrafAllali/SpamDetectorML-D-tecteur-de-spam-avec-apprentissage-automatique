import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Télécharger les stopwords (à faire une seule fois)
nltk.download('stopwords')

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(max_features=3000)
    
    def clean_text(self, text):
        """Nettoie un texte"""
        # Mettre en minuscules
        text = text.lower()
        
        # Supprimer les caractères spéciaux et chiffres
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Supprimer les espaces multiples
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Supprimer les stopwords
        words = text.split()
        words = [word for word in words if word not in self.stop_words]
        
        return ' '.join(words)
    
    def prepare_data(self, df):
        """Prépare le dataset complet"""
        # Nettoyer tous les messages
        print("🔄 Nettoyage des textes...")
        df['cleaned_message'] = df['message'].apply(self.clean_text)
        
        # Convertir les labels en 0 et 1
        df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})
        
        return df
    
    def vectorize(self, messages, fit=True):
        """Convertit les textes en vecteurs TF-IDF"""
        if fit:
            return self.vectorizer.fit_transform(messages)
        else:
            return self.vectorizer.transform(messages)
    
    def save_vectorizer(self, filename='models/vectorizer.pkl'):
        """Sauvegarde le vectorizer"""
        with open(filename, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"✅ Vectorizer sauvegardé : {filename}")


def main():
    # Charger le dataset
    print("📂 Chargement du dataset...")
    df = pd.read_csv('data/spam.csv', encoding='latin-1')
    df = df[['v1', 'v2']]
    df.columns = ['label', 'message']
    
    # Prétraitement
    preprocessor = TextPreprocessor()
    df = preprocessor.prepare_data(df)
    
    # Afficher des exemples
    print("\n=== Exemple de nettoyage ===")
    print("AVANT:", df['message'].iloc[0])
    print("APRÈS:", df['cleaned_message'].iloc[0])
    
    print("\nAVANT:", df['message'].iloc[100])
    print("APRÈS:", df['cleaned_message'].iloc[100])
    
    # Séparer features et labels
    X = df['cleaned_message']
    y = df['label_num']
    
    # Split train/test (80% train, 20% test)
    print("\n📊 Séparation train/test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"✅ Train set: {len(X_train)} messages")
    print(f"✅ Test set: {len(X_test)} messages")
    
    # Vectorisation TF-IDF
    print("\n🔢 Vectorisation TF-IDF...")
    X_train_tfidf = preprocessor.vectorize(X_train, fit=True)
    X_test_tfidf = preprocessor.vectorize(X_test, fit=False)
    
    print(f"✅ Shape X_train: {X_train_tfidf.shape}")
    print(f"✅ Shape X_test: {X_test_tfidf.shape}")
    
    # Créer le dossier models s'il n'existe pas
    import os
    os.makedirs('models', exist_ok=True)
    
    # Sauvegarder les données prétraitées
    print("\n💾 Sauvegarde des données...")
    with open('models/train_data.pkl', 'wb') as f:
        pickle.dump((X_train_tfidf, X_test_tfidf, y_train, y_test), f)
    
    # Sauvegarder le vectorizer
    preprocessor.save_vectorizer()
    
    print("\n✅ Prétraitement terminé avec succès!")
    print("📁 Fichiers créés:")
    print("   - models/train_data.pkl")
    print("   - models/vectorizer.pkl")


if __name__ == "__main__":
    main()