import pickle
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    confusion_matrix,
    classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns

class SpamDetector:
    def __init__(self, model_type='naive_bayes'):
        """
        Initialise le détecteur de spam
        model_type: 'naive_bayes' ou 'logistic_regression'
        """
        if model_type == 'naive_bayes':
            self.model = MultinomialNB()
            self.model_name = "Naive Bayes"
        else:
            self.model = LogisticRegression(max_iter=1000)
            self.model_name = "Logistic Regression"
    
    def train(self, X_train, y_train):
        """Entraîne le modèle"""
        print(f"🚀 Entraînement du modèle {self.model_name}...")
        self.model.fit(X_train, y_train)
        print("✅ Entraînement terminé!")
    
    def evaluate(self, X_test, y_test):
        """Évalue le modèle"""
        print(f"\n📊 Évaluation du modèle {self.model_name}...")
        
        # Prédictions
        y_pred = self.model.predict(X_test)
        
        # Métriques
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print(f"\n{'='*50}")
        print(f"📈 RÉSULTATS - {self.model_name}")
        print(f"{'='*50}")
        print(f"🎯 Accuracy:  {accuracy*100:.2f}%")
        print(f"🎯 Precision: {precision*100:.2f}%")
        print(f"🎯 Recall:    {recall*100:.2f}%")
        print(f"🎯 F1-Score:  {f1*100:.2f}%")
        print(f"{'='*50}\n")
        
        # Rapport détaillé
        print("📋 Rapport de classification:")
        print(classification_report(y_test, y_pred, 
                                   target_names=['HAM', 'SPAM']))
        
        # Matrice de confusion
        self.plot_confusion_matrix(y_test, y_pred)
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
    
    def plot_confusion_matrix(self, y_test, y_pred):
        """Affiche la matrice de confusion"""
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['HAM', 'SPAM'],
                    yticklabels=['HAM', 'SPAM'])
        plt.title(f'Matrice de Confusion - {self.model_name}')
        plt.ylabel('Vraie classe')
        plt.xlabel('Classe prédite')
        plt.tight_layout()
        plt.savefig(f'models/confusion_matrix_{self.model_name.replace(" ", "_")}.png')
        print(f"✅ Matrice de confusion sauvegardée")
        plt.show()
    
    def save_model(self, filename='models/spam_detector.pkl'):
        """Sauvegarde le modèle"""
        with open(filename, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"✅ Modèle sauvegardé : {filename}")


def compare_models(X_train, X_test, y_train, y_test):
    """Compare Naive Bayes et Logistic Regression"""
    print("\n" + "="*60)
    print("🔬 COMPARAISON DES MODÈLES")
    print("="*60 + "\n")
    
    results = {}
    
    # Naive Bayes
    nb_detector = SpamDetector('naive_bayes')
    nb_detector.train(X_train, y_train)
    results['Naive Bayes'] = nb_detector.evaluate(X_test, y_test)
    nb_detector.save_model('models/spam_detector_nb.pkl')
    
    print("\n" + "-"*60 + "\n")
    
    # Logistic Regression
    lr_detector = SpamDetector('logistic_regression')
    lr_detector.train(X_train, y_train)
    results['Logistic Regression'] = lr_detector.evaluate(X_test, y_test)
    lr_detector.save_model('models/spam_detector_lr.pkl')
    
    # Afficher la comparaison
    print("\n" + "="*60)
    print("🏆 COMPARAISON FINALE")
    print("="*60)
    
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        for metric, value in metrics.items():
            print(f"  {metric.capitalize()}: {value*100:.2f}%")
    
    # Déterminer le meilleur modèle
    best_model = max(results.items(), key=lambda x: x[1]['accuracy'])
    print(f"\n🥇 Meilleur modèle: {best_model[0]} "
          f"(Accuracy: {best_model[1]['accuracy']*100:.2f}%)")
    
    return results


def main():
    print("="*60)
    print("🤖 ENTRAÎNEMENT DU MODÈLE DE DÉTECTION DE SPAM")
    print("="*60 + "\n")
    
    # Charger les données prétraitées
    print("📂 Chargement des données prétraitées...")
    with open('models/train_data.pkl', 'rb') as f:
        X_train, X_test, y_train, y_test = pickle.load(f)
    
    print(f"✅ Données chargées:")
    print(f"   - Train: {X_train.shape[0]} messages")
    print(f"   - Test: {X_test.shape[0]} messages")
    print(f"   - Features: {X_train.shape[1]}")
    
    # Option 1: Entraîner un seul modèle (Naive Bayes)
    print("\n" + "="*60)
    print("Option choisie: Naive Bayes")
    print("="*60)
    
    detector = SpamDetector('naive_bayes')
    detector.train(X_train, y_train)
    detector.evaluate(X_test, y_test)
    detector.save_model()
    
    # Option 2: Comparer les deux modèles (décommenter si souhaité)
    # compare_models(X_train, X_test, y_train, y_test)
    
    print("\n" + "="*60)
    print("✅ ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS!")
    print("="*60)
    print("\n📁 Fichiers créés:")
    print("   - models/spam_detector.pkl")
    print("   - models/confusion_matrix_Naive_Bayes.png")


if __name__ == "__main__":
    main()