# views/analysis_tab.py
"""
Onglet d'analyse de messages
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import logging
from datetime import datetime

from config.settings import get_colors, get_translation
from .components import StatusIndicator

logger = logging.getLogger(__name__)

class AnalysisTab(tk.Frame):
    """Onglet pour analyser les messages"""
    
    def __init__(self, parent, prediction_service, **kwargs):
        super().__init__(parent, bg=get_colors()['bg'], **kwargs)
        
        self.prediction_service = prediction_service
        self.current_result = None
        
        # Exemples de messages
        self.examples = [
            "Congratulations! You've won a FREE iPhone 15! Click here to claim your prize now! Limited time offer!",
            "Hey, are we still meeting for lunch tomorrow at 12pm? Let me know if you need to reschedule.",
            "URGENT! Your bank account has been compromised. Verify your identity immediately by clicking this link!",
            "Thanks for your help with the project yesterday. I really appreciate it. See you at the meeting next week.",
            "Make $5000 per week working from home! No experience needed! Call now for this amazing opportunity!",
            "Hi Mom, just wanted to let you know I arrived safely. The flight was good. Talk to you later!",
        ]
        self.current_example_index = 0
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crée les widgets de l'onglet"""
        
        # Container principal
        main_container = tk.Frame(self, bg=get_colors()['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # === SECTION GAUCHE : SAISIE ===
        left_frame = tk.Frame(main_container, bg=get_colors()['bg'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # En-tête
        header = tk.Frame(left_frame, bg=get_colors()['bg'])
        header.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            header,
            text="📧 Analyser un Message",
            font=("Arial", 18, "bold"),
            bg=get_colors()['bg'],
            fg=get_colors()['text']
        ).pack(side=tk.LEFT)
        
        # Instructions
        instructions = tk.Label(
            left_frame,
            text="Entrez ou collez le message email à analyser ci-dessous :",
            font=("Arial", 11),
            bg=get_colors()['bg'],
            fg=get_colors()['secondary'],
            justify=tk.LEFT
        )
        instructions.pack(anchor=tk.W, pady=(0, 10))
        
        # Zone de texte avec frame
        text_frame = tk.Frame(left_frame, bg="white", relief=tk.SOLID, borderwidth=1)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Compteur de caractères
        self.char_count_label = tk.Label(
            text_frame,
            text="0 caractères",
            font=("Arial", 9),
            bg="white",
            fg=get_colors()['secondary']
        )
        self.char_count_label.pack(anchor=tk.E, padx=10, pady=5)
        
        # Zone de texte
        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            height=12,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.bind('<KeyRelease>', self.update_char_count)
        
        # Placeholder
        self.placeholder = "Exemple : Congratulations! You've won a prize..."
        self.text_area.insert("1.0", self.placeholder)
        self.text_area.config(fg=get_colors()['secondary'])
        
        # Gestion du placeholder
        self.text_area.bind("<FocusIn>", self.clear_placeholder)
        self.text_area.bind("<FocusOut>", self.restore_placeholder)
        
        # Boutons d'action
        buttons_frame = tk.Frame(left_frame, bg=get_colors()['bg'])
        buttons_frame.pack(fill=tk.X)
        
        # Bouton Analyser (principal)
        self.analyze_button = tk.Button(
            buttons_frame,
            text="🔍 Analyser le Message",
            command=self.analyze_message,
            font=("Arial", 12, "bold"),
            bg=get_colors()['primary'],
            fg="white",
            padx=30,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton Effacer
        tk.Button(
            buttons_frame,
            text="🗑️ Effacer",
            command=self.clear_text,
            font=("Arial", 11),
            bg=get_colors()['secondary'],
            fg="white",
            padx=20,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton Exemple
        tk.Button(
            buttons_frame,
            text="💡 Exemple",
            command=self.load_example,
            font=("Arial", 11),
            bg=get_colors()['warning'],
            fg="white",
            padx=20,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton Importer
        tk.Button(
            buttons_frame,
            text="📁 Importer",
            command=self.import_from_file,
            font=("Arial", 11),
            bg="#9C27B0",
            fg="white",
            padx=20,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT)
        
        # === SECTION DROITE : RÉSULTATS ===
        right_frame = tk.Frame(main_container, bg="white", relief=tk.RAISED, borderwidth=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # En-tête résultats
        result_header = tk.Frame(right_frame, bg="white")
        result_header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            result_header,
            text="🎯 Résultat de l'Analyse",
            font=("Arial", 16, "bold"),
            bg="white",
            fg=get_colors()['text']
        ).pack(anchor=tk.W)
        
        # Séparateur
        tk.Frame(right_frame, bg="#e0e0e0", height=1).pack(fill=tk.X, padx=20)
        
        # Container des résultats
        self.results_container = tk.Frame(right_frame, bg="white")
        self.results_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Message initial
        self.initial_message = tk.Label(
            self.results_container,
            text="👆 Entrez un message et cliquez sur\n'Analyser' pour voir les résultats",
            font=("Arial", 12),
            bg="white",
            fg=get_colors()['secondary'],
            justify=tk.CENTER
        )
        self.initial_message.pack(expand=True)
        
        # Frame pour les résultats (caché initialement)
        self.result_frame = tk.Frame(self.results_container, bg="white")
        
        # Verdict principal
        self.verdict_frame = tk.Frame(self.result_frame, bg="white")
        self.verdict_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.verdict_label = tk.Label(
            self.verdict_frame,
            text="",
            font=("Arial", 24, "bold"),
            bg="white"
        )
        self.verdict_label.pack()
        
        self.confidence_label = tk.Label(
            self.verdict_frame,
            text="",
            font=("Arial", 14),
            bg="white",
            fg=get_colors()['secondary']
        )
        self.confidence_label.pack(pady=(5, 0))
        
        # Séparateur
        tk.Frame(self.result_frame, bg="#e0e0e0", height=1).pack(fill=tk.X, pady=15)
        
        # Probabilités détaillées
        tk.Label(
            self.result_frame,
            text="Probabilités détaillées",
            font=("Arial", 12, "bold"),
            bg="white",
            fg=get_colors()['text']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # HAM probability
        ham_frame = tk.Frame(self.result_frame, bg="white")
        ham_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            ham_frame,
            text="✅ HAM (Légitime)",
            font=("Arial", 11),
            bg="white",
            width=18,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.ham_progress = ttk.Progressbar(
            ham_frame,
            length=200,
            mode='determinate',
            maximum=100
        )
        self.ham_progress.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.ham_label = tk.Label(
            ham_frame,
            text="0.0%",
            font=("Arial", 11, "bold"),
            bg="white",
            fg=get_colors()['success'],
            width=8
        )
        self.ham_label.pack(side=tk.LEFT)
        
        # SPAM probability
        spam_frame = tk.Frame(self.result_frame, bg="white")
        spam_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            spam_frame,
            text="🚨 SPAM",
            font=("Arial", 11),
            bg="white",
            width=18,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.spam_progress = ttk.Progressbar(
            spam_frame,
            length=200,
            mode='determinate',
            maximum=100
        )
        self.spam_progress.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.spam_label = tk.Label(
            spam_frame,
            text="0.0%",
            font=("Arial", 11, "bold"),
            bg="white",
            fg=get_colors()['danger'],
            width=8
        )
        self.spam_label.pack(side=tk.LEFT)
        
        # Séparateur
        tk.Frame(self.result_frame, bg="#e0e0e0", height=1).pack(fill=tk.X, pady=15)
        
        # Informations supplémentaires
        tk.Label(
            self.result_frame,
            text="📊 Informations",
            font=("Arial", 12, "bold"),
            bg="white",
            fg=get_colors()['text']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.info_text = tk.Text(
            self.result_frame,
            height=8,
            font=("Courier", 9),
            bg="#f8f9fa",
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        self.info_text.pack(fill=tk.X)
        self.info_text.config(state=tk.DISABLED)
        
        # Boutons d'action sur résultat
        action_buttons = tk.Frame(self.result_frame, bg="white")
        action_buttons.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(
            action_buttons,
            text="💾 Enregistrer",
            command=self.save_result,
            font=("Arial", 9),
            bg=get_colors()['success'],
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(
            action_buttons,
            text="📋 Copier",
            command=self.copy_result,
            font=("Arial", 9),
            bg=get_colors()['primary'],
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT)
    
    def clear_placeholder(self, event):
        """Efface le placeholder"""
        if self.text_area.get("1.0", tk.END).strip() == self.placeholder:
            self.text_area.delete("1.0", tk.END)
            self.text_area.config(fg=get_colors()['text'])
    
    def restore_placeholder(self, event):
        """Restaure le placeholder si vide"""
        if not self.text_area.get("1.0", tk.END).strip():
            self.text_area.insert("1.0", self.placeholder)
            self.text_area.config(fg=get_colors()['secondary'])
    
    def update_char_count(self, event=None):
        """Met à jour le compteur de caractères"""
        content = self.text_area.get("1.0", tk.END).strip()
        if content == self.placeholder:
            count = 0
        else:
            count = len(content)
        self.char_count_label.config(text=f"{count} caractères")
    
    def analyze_message(self):
        """Analyse le message"""
        try:
            # Récupérer le texte
            message = self.text_area.get("1.0", tk.END).strip()
            
            # Validation
            if not message or message == self.placeholder:
                messagebox.showwarning(
                    "Attention",
                    "Veuillez entrer un message à analyser !"
                )
                return
            
            # Désactiver le bouton pendant l'analyse
            self.analyze_button.config(state=tk.DISABLED, text="⏳ Analyse en cours...")
            self.update_idletasks()
            
            # Effectuer la prédiction
            result = self.prediction_service.predict(message)
            
            if result is None:
                messagebox.showerror(
                    "Erreur",
                    "Une erreur est survenue lors de l'analyse."
                )
                return
            
            # Afficher les résultats
            self.display_result(result)
            self.current_result = result
            
            logger.info(f"✅ Analyse effectuée : {'SPAM' if result['is_spam'] else 'HAM'}")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'analyse: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'analyse:\n{str(e)}")
            
        finally:
            # Réactiver le bouton
            self.analyze_button.config(state=tk.NORMAL, text="🔍 Analyser le Message")
    
    def display_result(self, result):
        """Affiche les résultats de l'analyse"""
        try:
            # Cacher le message initial
            self.initial_message.pack_forget()
            
            # Afficher le frame de résultats
            self.result_frame.pack(fill=tk.BOTH, expand=True)
            
            # Verdict
            if result['is_spam']:
                verdict_text = "🚨 SPAM DÉTECTÉ !"
                verdict_color = get_colors()['danger']
            else:
                verdict_text = "✅ MESSAGE LÉGITIME"
                verdict_color = get_colors()['success']
            
            self.verdict_label.config(text=verdict_text, fg=verdict_color)
            
            # Confiance
            confidence = result['confidence'] * 100
            self.confidence_label.config(
                text=f"Confiance : {confidence:.1f}%"
            )
            
            # Probabilités
            ham_prob = result['probabilities']['ham'] * 100
            spam_prob = result['probabilities']['spam'] * 100
            
            self.ham_progress['value'] = ham_prob
            self.ham_label.config(text=f"{ham_prob:.1f}%")
            
            self.spam_progress['value'] = spam_prob
            self.spam_label.config(text=f"{spam_prob:.1f}%")
            
            # Informations détaillées
            features = result.get('features', {})
            info_text = f"""Analyse détaillée :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Nombre de mots      : {features.get('word_count', 'N/A')}
- Nombre de caractères: {features.get('char_count', 'N/A')}
- Longueur moy. mots  : {features.get('avg_word_length', 0):.1f}
- Contient URL        : {'Oui' if features.get('has_url') else 'Non'}
- Contient email      : {'Oui' if features.get('has_email') else 'Non'}
- Contient chiffres   : {'Oui' if features.get('has_numbers') else 'Non'}
- Ratio majuscules    : {features.get('uppercase_ratio', 0)*100:.1f}%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Timestamp : {result.get('timestamp', 'N/A')}
Version   : {result.get('model_version', 'N/A')}
"""
            
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete("1.0", tk.END)
            self.info_text.insert("1.0", info_text)
            self.info_text.config(state=tk.DISABLED)
            
        except Exception as e:
            logger.error(f"❌ Erreur affichage résultats: {e}")
    
    def clear_text(self):
        """Efface le texte et les résultats"""
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", self.placeholder)
        self.text_area.config(fg=get_colors()['secondary'])
        
        # Cacher les résultats
        self.result_frame.pack_forget()
        self.initial_message.pack(expand=True)
        
        self.current_result = None
        self.update_char_count()
    
    def load_example(self):
        """Charge un exemple"""
        example = self.examples[self.current_example_index]
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", example)
        self.text_area.config(fg=get_colors()['text'])
        
        # Passer à l'exemple suivant
        self.current_example_index = (self.current_example_index + 1) % len(self.examples)
        
        self.update_char_count()
    
    def import_from_file(self):
        """Importe un message depuis un fichier"""
        try:
            filename = filedialog.askopenfilename(
                title="Sélectionner un fichier",
                filetypes=[
                    ("Fichiers texte", "*.txt"),
                    ("Tous les fichiers", "*.*")
                ]
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)
                self.text_area.config(fg=get_colors()['text'])
                
                self.update_char_count()
                logger.info(f"✅ Fichier importé: {filename}")
                
        except Exception as e:
            logger.error(f"❌ Erreur import fichier: {e}")
            messagebox.showerror("Erreur", f"Impossible d'importer le fichier:\n{str(e)}")
    
    def save_result(self):
        """Sauvegarde le résultat"""
        if not self.current_result:
            messagebox.showwarning("Attention", "Aucun résultat à sauvegarder")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                title="Enregistrer le résultat",
                defaultextension=".txt",
                filetypes=[("Fichiers texte", "*.txt")]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("=== RÉSULTAT DE L'ANALYSE ===\n\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write(f"Message:\n{self.current_result['original_message']}\n\n")
                    f.write(f"Verdict: {'SPAM' if self.current_result['is_spam'] else 'HAM'}\n")
                    f.write(f"Confiance: {self.current_result['confidence']*100:.2f}%\n\n")
                    f.write(f"Probabilités:\n")
                    f.write(f"  HAM:  {self.current_result['probabilities']['ham']*100:.2f}%\n")
                    f.write(f"  SPAM: {self.current_result['probabilities']['spam']*100:.2f}%\n")
                
                messagebox.showinfo("Succès", f"Résultat sauvegardé:\n{filename}")
                logger.info(f"✅ Résultat sauvegardé: {filename}")
                
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde:\n{str(e)}")
    
    def copy_result(self):
        """Copie le résultat dans le presse-papier"""
        if not self.current_result:
            messagebox.showwarning("Attention", "Aucun résultat à copier")
            return
        
        try:
            verdict = "SPAM" if self.current_result['is_spam'] else "HAM"
            confidence = self.current_result['confidence'] * 100
            
            result_text = f"Verdict: {verdict} (Confiance: {confidence:.1f}%)"
            
            self.clipboard_clear()
            self.clipboard_append(result_text)
            
            messagebox.showinfo("Succès", "Résultat copié dans le presse-papier!")
            logger.info("✅ Résultat copié")
            
        except Exception as e:
            logger.error(f"❌ Erreur copie: {e}")