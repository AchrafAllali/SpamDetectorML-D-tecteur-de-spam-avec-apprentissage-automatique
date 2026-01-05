import pickle
import re
from nltk.corpus import stopwords

# Charger le modèle
with open('models/spam_detector.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

def is_spam(message):
    """Fonction simple pour tester rapidement"""
    # Nettoyer
    stop_words = set(stopwords.words('english'))
    text = re.sub(r'[^a-zA-Z\s]', '', message.lower())
    words = [w for w in text.split() if w not in stop_words]
    cleaned = ' '.join(words)
    
    # Prédire
    vec = vectorizer.transform([cleaned])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0][pred] * 100
    
    result = "SPAM" if pred == 1 else "HAM"
    print(f"📧 '{message[:50]}...'")
    print(f"🔍 {result} ({prob:.1f}% confiance)\n")
    
    return pred == 1

# Tests rapides
if __name__ == "__main__":
    print("🧪 TESTS RAPIDES\n" + "="*50 + "\n")
    
    is_spam("Congratulations! You won $1000!")
    is_spam("Hey, want to grab coffee later?")
    is_spam("URGENT! Your account will be closed!")
    is_spam("Meeting moved to 3pm tomorrow")