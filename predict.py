import pickle
import re
from nltk.corpus import stopwords

class SpamPredictor:
    def __init__(self):
        """Charge le modèle et le vectorizer"""
        print("📂 Chargement du modèle...")
        
        # Charger le modèle
        with open('models/spam_detector.pkl', 'rb') as f:
            self.model = pickle.load(f)
        
        # Charger le vectorizer
        with open('models/vectorizer.pkl', 'rb') as f:
            self.vectorizer = pickle.load(f)
        
        # Stopwords
        self.stop_words = set(stopwords.words('english'))
        
        print("✅ Modèle chargé avec succès!\n")
    
    def clean_text(self, text):
        """Nettoie le texte (même fonction que preprocessing.py)"""
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
    
    def predict(self, message):
        """Prédit si un message est spam ou non"""
        # Nettoyer le message
        cleaned = self.clean_text(message)
        
        # Vectoriser
        vectorized = self.vectorizer.transform([cleaned])
        
        # Prédire
        prediction = self.model.predict(vectorized)[0]
        probability = self.model.predict_proba(vectorized)[0]
        
        # Résultat
        label = "🚨 SPAM" if prediction == 1 else "✅ HAM (Non-Spam)"
        confidence = probability[prediction] * 100
        
        return {
            'label': label,
            'is_spam': prediction == 1,
            'confidence': confidence,
            'probabilities': {
                'ham': probability[0] * 100,
                'spam': probability[1] * 100
            }
        }
    
    def predict_with_details(self, message):
        """Prédit et affiche les détails"""
        print("="*60)
        print("📧 MESSAGE À ANALYSER")
        print("="*60)
        print(f"{message[:200]}{'...' if len(message) > 200 else ''}")
        print()
        
        result = self.predict(message)
        
        print("="*60)
        print("🔍 RÉSULTAT DE L'ANALYSE")
        print("="*60)
        print(f"Prédiction: {result['label']}")
        print(f"Confiance:  {result['confidence']:.2f}%")
        print()
        print("Probabilités détaillées:")
        print(f"  📬 HAM (Non-Spam): {result['probabilities']['ham']:.2f}%")
        print(f"  🚨 SPAM:           {result['probabilities']['spam']:.2f}%")
        print("="*60 + "\n")
        
        return result


def test_examples():
    """Teste le modèle avec plusieurs exemples"""
    predictor = SpamPredictor()
    
    # Exemples de messages à tester
    test_messages = [
        # SPAM évidents
        {
            'title': 'SPAM - Offre gratuite',
            'message': 'Congratulations! You have won a free iPhone! Click here to claim your prize now! Limited time offer!'
        },
        {
            'title': 'SPAM - Argent facile',
            'message': 'Make money fast! Work from home and earn $5000 per week! No experience needed! Call now!'
        },
        {
            'title': 'SPAM - Loterie',
            'message': 'URGENT! You won the lottery! £1,000,000 waiting for you! Send your bank details to claim!'
        },
        
        # HAM (Non-spam)
        {
            'title': 'HAM - Message normal',
            'message': 'Hey, are we still meeting for lunch tomorrow at 12pm? Let me know if you need to reschedule.'
        },
        {
            'title': 'HAM - Professionnel',
            'message': 'The project deadline has been moved to next Friday. Please update your tasks accordingly.'
        },
        {
            'title': 'HAM - Personnel',
            'message': 'Thanks for your help yesterday! I really appreciate it. See you next week.'
        },
        
        # Cas ambigus
        {
            'title': 'AMBIGU - Promotion légitime',
            'message': 'Special offer from Amazon: 20% off on electronics this weekend. Check your account for details.'
        },
        {
            'title': 'AMBIGU - Newsletter',
            'message': 'Subscribe to our weekly newsletter and get exclusive deals delivered to your inbox!'
        }
    ]
    
    print("\n" + "🧪 TEST DU MODÈLE AVEC DIFFÉRENTS EXEMPLES ".center(60, "="))
    print()
    
    results = []
    for i, test in enumerate(test_messages, 1):
        print(f"\n{'─'*60}")
        print(f"TEST #{i}: {test['title']}")
        print(f"{'─'*60}")
        
        result = predictor.predict_with_details(test['message'])
        results.append({
            'title': test['title'],
            'result': result
        })
    
    # Résumé
    print("\n" + "📊 RÉSUMÉ DES TESTS ".center(60, "="))
    print()
    
    spam_detected = sum(1 for r in results if r['result']['is_spam'])
    ham_detected = len(results) - spam_detected
    
    print(f"Total de messages testés: {len(results)}")
    print(f"🚨 Détectés comme SPAM:   {spam_detected}")
    print(f"✅ Détectés comme HAM:    {ham_detected}")
    print()
    
    for r in results:
        emoji = "🚨" if r['result']['is_spam'] else "✅"
        print(f"{emoji} {r['title']}: {r['result']['confidence']:.1f}%")


def interactive_mode():
    """Mode interactif pour tester des messages personnalisés"""
    predictor = SpamPredictor()
    
    print("\n" + "🎮 MODE INTERACTIF ".center(60, "="))
    print("\nEntrez vos messages pour les analyser.")
    print("Tapez 'quit' ou 'exit' pour quitter.\n")
    
    while True:
        print("─"*60)
        message = input("📧 Entrez votre message: ")
        
        if message.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Au revoir!")
            break
        
        if not message.strip():
            print("⚠️  Message vide, veuillez réessayer.\n")
            continue
        
        print()
        predictor.predict_with_details(message)


def main():
    print("\n" + "="*60)
    print("🔮 SYSTÈME DE PRÉDICTION DE SPAM")
    print("="*60 + "\n")
    
    print("Choisissez un mode:")
    print("1. 🧪 Tester avec des exemples prédéfinis")
    print("2. 🎮 Mode interactif (entrer vos propres messages)")
    print("3. 🚀 Les deux")
    
    choice = input("\nVotre choix (1/2/3): ").strip()
    
    if choice == '1':
        test_examples()
    elif choice == '2':
        interactive_mode()
    elif choice == '3':
        test_examples()
        interactive_mode()
    else:
        print("❌ Choix invalide. Utilisation du mode test par défaut.")
        test_examples()


if __name__ == "__main__":
    main()