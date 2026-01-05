import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pickle
import re
from nltk.corpus import stopwords

class SpamDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔮 Détecteur de Spam - ML")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Couleurs
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2196F3"
        self.spam_color = "#f44336"
        self.ham_color = "#4CAF50"
        self.text_color = "#333333"
        
        self.root.configure(bg=self.bg_color)
        
        # Charger le modèle
        self.load_model()
        
        # Créer l'interface
        self.create_widgets()
        
        # Exemples de messages
        self.examples = [
            "Congratulations! You won a free iPhone! Click here now!",
            "Hey, are we still meeting for lunch tomorrow?",
            "URGENT! Your account will be closed! Verify now!",
            "Thanks for your help yesterday. See you next week!"
        ]
        self.current_example = 0
    
    def load_model(self):
        """Charge le modèle et le vectorizer"""
        try:
            with open('models/spam_detector.pkl', 'rb') as f:
                self.model = pickle.load(f)
            
            with open('models/vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            self.stop_words = set(stopwords.words('english'))
            
            print("✅ Modèle chargé avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le modèle:\n{str(e)}")
            self.root.destroy()
    
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        
        # En-tête
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔮 Détecteur de Spam avec Machine Learning",
            font=("Arial", 20, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Instructions
        instruction_label = tk.Label(
            main_frame,
            text="📧 Entrez votre message email ci-dessous pour l'analyser :",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        instruction_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Zone de texte
        text_frame = tk.Frame(main_frame, bg=self.bg_color)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            height=10,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Boutons
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=15)
        
        self.analyze_button = tk.Button(
            button_frame,
            text="🔍 Analyser le Message",
            command=self.analyze_message,
            font=("Arial", 12, "bold"),
            bg=self.primary_color,
            fg="white",
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tk.Button(
            button_frame,
            text="🗑️ Effacer",
            command=self.clear_text,
            font=("Arial", 12),
            bg="#757575",
            fg="white",
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.example_button = tk.Button(
            button_frame,
            text="💡 Exemple",
            command=self.load_example,
            font=("Arial", 12),
            bg="#FF9800",
            fg="white",
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.example_button.pack(side=tk.LEFT, padx=5)
        
        # Frame de résultats
        self.result_frame = tk.Frame(main_frame, bg="white", relief=tk.SOLID, borderwidth=1)
        self.result_frame.pack(fill=tk.BOTH, pady=10)
        
        result_title = tk.Label(
            self.result_frame,
            text="📊 Résultat de l'Analyse",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=self.text_color
        )
        result_title.pack(pady=10)
        
        # Label de résultat principal
        self.result_label = tk.Label(
            self.result_frame,
            text="En attente d'analyse...",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#757575"
        )
        self.result_label.pack(pady=10)
        
        # Frame pour les probabilités
        prob_frame = tk.Frame(self.result_frame, bg="white")
        prob_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # HAM probability
        ham_frame = tk.Frame(prob_frame, bg="white")
        ham_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            ham_frame,
            text="✅ HAM (Non-Spam):",
            font=("Arial", 11),
            bg="white",
            width=20,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.ham_progress = ttk.Progressbar(
            ham_frame,
            length=300,
            mode='determinate',
            style="HAM.Horizontal.TProgressbar"
        )
        self.ham_progress.pack(side=tk.LEFT, padx=10)
        
        self.ham_label = tk.Label(
            ham_frame,
            text="0%",
            font=("Arial", 11, "bold"),
            bg="white",
            fg=self.ham_color,
            width=8
        )
        self.ham_label.pack(side=tk.LEFT)
        
        # SPAM probability
        spam_frame = tk.Frame(prob_frame, bg="white")
        spam_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            spam_frame,
            text="🚨 SPAM:",
            font=("Arial", 11),
            bg="white",
            width=20,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.spam_progress = ttk.Progressbar(
            spam_frame,
            length=300,
            mode='determinate',
            style="SPAM.Horizontal.TProgressbar"
        )
        self.spam_progress.pack(side=tk.LEFT, padx=10)
        
        self.spam_label = tk.Label(
            spam_frame,
            text="0%",
            font=("Arial", 11, "bold"),
            bg="white",
            fg=self.spam_color,
            width=8
        )
        self.spam_label.pack(side=tk.LEFT)
        
        # Configurer les styles des barres de progression
        style = ttk.Style()
        style.theme_use('default')
        style.configure("HAM.Horizontal.TProgressbar", background=self.ham_color)
        style.configure("SPAM.Horizontal.TProgressbar", background=self.spam_color)
        
        # Footer
        footer_label = tk.Label(
            self.root,
            text="🤖 Powered by Machine Learning (Naive Bayes) | Python & Scikit-learn",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#757575"
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)
    
    def clean_text(self, text):
        """Nettoie le texte"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        words = text.split()
        words = [word for word in words if word not in self.stop_words]
        return ' '.join(words)
    
    def analyze_message(self):
        """Analyse le message et affiche les résultats"""
        message = self.text_area.get("1.0", tk.END).strip()
        
        if not message:
            messagebox.showwarning("Attention", "Veuillez entrer un message à analyser!")
            return
        
        try:
            # Nettoyer et vectoriser
            cleaned = self.clean_text(message)
            vectorized = self.vectorizer.transform([cleaned])
            
            # Prédire
            prediction = self.model.predict(vectorized)[0]
            probabilities = self.model.predict_proba(vectorized)[0]
            
            ham_prob = probabilities[0] * 100
            spam_prob = probabilities[1] * 100
            
            # Mettre à jour l'interface
            if prediction == 1:  # SPAM
                self.result_label.config(
                    text="🚨 SPAM DÉTECTÉ !",
                    fg=self.spam_color
                )
            else:  # HAM
                self.result_label.config(
                    text="✅ MESSAGE LÉGITIME",
                    fg=self.ham_color
                )
            
            # Mettre à jour les barres de progression
            self.ham_progress['value'] = ham_prob
            self.spam_progress['value'] = spam_prob
            
            self.ham_label.config(text=f"{ham_prob:.1f}%")
            self.spam_label.config(text=f"{spam_prob:.1f}%")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'analyse:\n{str(e)}")
    
    def clear_text(self):
        """Efface le texte et réinitialise les résultats"""
        self.text_area.delete("1.0", tk.END)
        self.result_label.config(
            text="En attente d'analyse...",
            fg="#757575"
        )
        self.ham_progress['value'] = 0
        self.spam_progress['value'] = 0
        self.ham_label.config(text="0%")
        self.spam_label.config(text="0%")
    
    def load_example(self):
        """Charge un exemple de message"""
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", self.examples[self.current_example])
        self.current_example = (self.current_example + 1) % len(self.examples)


def main():
    root = tk.Tk()
    app = SpamDetectorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()