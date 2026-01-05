# views/history_tab.py
"""
Onglet d'historique des prédictions
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
from datetime import datetime

from config.settings import get_colors
from .components import ScrollableFrame

logger = logging.getLogger(__name__)

class HistoryTab(tk.Frame):
    """Onglet d'historique"""
    
    def __init__(self, parent, prediction_service, **kwargs):
        super().__init__(parent, bg=get_colors()['bg'], **kwargs)
        
        self.prediction_service = prediction_service
        self.predictions = []
        self.filtered_predictions = []
        self.filter_type = "all"  # all, spam, ham
        
        self.create_widgets()
        self.load_history()
    
    def create_widgets(self):
        """Crée les widgets"""
        
        # Container principal
        main_container = tk.Frame(self, bg=get_colors()['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # En-tête
        header = tk.Frame(main_container, bg=get_colors()['bg'])
        header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header,
            text="📋 Historique des Analyses",
            font=("Arial", 18, "bold"),
            bg=get_colors()['bg'],
            fg=get_colors()['text']
        ).pack(side=tk.LEFT)
        
        # Boutons d'action
        tk.Button(
            header,
            text="🔄 Actualiser",
            command=self.load_history,
            font=("Arial", 10),
            bg=get_colors()['primary'],
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        tk.Button(
            header,
            text="📥 Exporter",
            command=self.export_history,
            font=("Arial", 10),
            bg=get_colors()['success'],
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        tk.Button(
            header,
            text="🗑️ Effacer",
            command=self.clear_history,
            font=("Arial", 10),
            bg=get_colors()['danger'],
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.RIGHT)
        
        # Barre de filtres
        filter_frame = tk.Frame(main_container, bg=get_colors()['bg'])
        filter_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            filter_frame,
            text="Filtrer par :",
            font=("Arial", 10),
            bg=get_colors()['bg'],
            fg=get_colors()['text']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Boutons de filtre
        self.filter_buttons = {}
        
        for filter_type, label, color in [
            ('all', '📊 Tout', get_colors()['primary']),
            ('spam', '🚨 SPAM', get_colors()['danger']),
            ('ham', '✅ HAM', get_colors()['success'])
        ]:
            btn = tk.Button(
                filter_frame,
                text=label,
                command=lambda ft=filter_type: self.apply_filter(ft),
                font=("Arial", 10),
                bg=color if filter_type == 'all' else get_colors()['bg'],
                fg="white" if filter_type == 'all' else get_colors()['text'],
                padx=15,
                pady=8,
                relief=tk.FLAT if filter_type == 'all' else tk.RAISED,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=(0, 5))
            self.filter_buttons[filter_type] = (btn, color)
        
        # Compteur
        self.count_label = tk.Label(
            filter_frame,
            text="0 résultats",
            font=("Arial", 10),
            bg=get_colors()['bg'],
            fg=get_colors()['secondary']
        )
        self.count_label.pack(side=tk.RIGHT)
        
        # Zone de liste avec scroll
        list_frame = tk.Frame(main_container, bg="white", relief=tk.SOLID, borderwidth=1)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable container
        self.scrollable = ScrollableFrame(list_frame)
        self.scrollable.pack(fill=tk.BOTH, expand=True)
        
        # Message si vide
        self.empty_message = tk.Label(
            self.scrollable.scrollable_frame,
            text="📭 Aucune analyse dans l'historique\n\nCommencez par analyser un message dans l'onglet 'Analyse'",
            font=("Arial", 12),
            bg="white",
            fg=get_colors()['secondary'],
            justify=tk.CENTER
        )
    
    def load_history(self):
        """Charge l'historique"""
        try:
            logger.info("🔄 Chargement de l'historique...")
            
            # Récupérer les prédictions
            self.predictions = self.prediction_service.get_recent_predictions(limit=100)
            
            # Appliquer le filtre actuel
            self.apply_filter(self.filter_type)
            
            logger.info(f"✅ {len(self.predictions)} prédictions chargées")
            
        except Exception as e:
            logger.error(f"❌ Erreur chargement historique: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du chargement:\n{str(e)}")
    
    def apply_filter(self, filter_type):
        """Applique un filtre"""
        self.filter_type = filter_type
        
        # Mettre à jour les boutons
        for ft, (btn, color) in self.filter_buttons.items():
            if ft == filter_type:
                btn.config(bg=color, fg="white", relief=tk.FLAT)
            else:
                btn.config(bg=get_colors()['bg'], fg=get_colors()['text'], relief=tk.RAISED)
        
        # Filtrer les prédictions
        if filter_type == 'all':
            self.filtered_predictions = self.predictions
        elif filter_type == 'spam':
            self.filtered_predictions = []
            for pred in self.predictions:
                # Vérifier plusieurs clés possibles
                prediction_value = pred.get('prediction')
                if prediction_value is None:
                    prediction_value = pred.get('is_spam', 0)
                if prediction_value == 1 or prediction_value == 'spam' or prediction_value is True:
                    self.filtered_predictions.append(pred)
        else:  # ham
            self.filtered_predictions = []
            for pred in self.predictions:
                # Vérifier plusieurs clés possibles
                prediction_value = pred.get('prediction')
                if prediction_value is None:
                    prediction_value = pred.get('is_spam', 1)
                if prediction_value == 0 or prediction_value == 'ham' or prediction_value is False:
                    self.filtered_predictions.append(pred)
        
        # Afficher
        self.display_predictions()
    
    def display_predictions(self):
        """Affiche les prédictions"""
        try:
            # Effacer le contenu actuel
            for widget in self.scrollable.scrollable_frame.winfo_children():
                widget.destroy()
            
            # Si vide
            if not self.filtered_predictions:
                self.empty_message.pack(expand=True, pady=50)
                self.count_label.config(text="0 résultats")
                return
            
            # Afficher chaque prédiction
            for i, pred in enumerate(self.filtered_predictions):
                try:
                    self.create_prediction_card(pred, i)
                except Exception as e:
                    logger.error(f"❌ Erreur création card {i}: {e}")
                    continue
            
            # Mettre à jour le compteur
            self.count_label.config(text=f"{len(self.filtered_predictions)} résultat(s)")
            
        except Exception as e:
            logger.error(f"❌ Erreur affichage: {e}")
    
    def create_prediction_card(self, prediction, index):
        """Crée une card pour une prédiction"""
        
        # Extraire les données avec des valeurs par défaut
        # Gérer différentes clés possibles
        prediction_value = prediction.get('prediction')
        if prediction_value is None:
            prediction_value = prediction.get('is_spam', 0)
        
        # Convertir en int si nécessaire
        if isinstance(prediction_value, bool):
            is_spam = 1 if prediction_value else 0
        elif isinstance(prediction_value, str):
            is_spam = 1 if prediction_value.lower() == 'spam' or prediction_value == '1' else 0
        else:
            try:
                is_spam = int(prediction_value)
            except:
                is_spam = 0
        
        # Extraire la confiance
        confidence = prediction.get('confidence', 0)
        if confidence is None:
            confidence = prediction.get('confidence_score', 0) or 0
        
        try:
            confidence_percent = float(confidence) * 100
        except:
            confidence_percent = 0
        
        # Extraire le message
        message = prediction.get('message', '')
        if not message:
            message = prediction.get('original_message', '')
            if not message:
                message = prediction.get('cleaned_message', 'Aucun message')
        
        # Extraire le timestamp
        timestamp = prediction.get('timestamp', 'N/A')
        if isinstance(timestamp, str):
            try:
                # Essayer différents formats
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S.%f']:
                    try:
                        dt = datetime.strptime(timestamp.split('.')[0], fmt)
                        timestamp_str = dt.strftime("%d/%m/%Y %H:%M")
                        break
                    except:
                        continue
                else:
                    timestamp_str = timestamp
            except:
                timestamp_str = str(timestamp)
        else:
            timestamp_str = str(timestamp)
        
        # Extraire la version du modèle
        model_version = prediction.get('model_version', 'N/A')
        if model_version is None:
            model_version = 'N/A'
        
        # Card container
        card = tk.Frame(
            self.scrollable.scrollable_frame,
            bg="white",
            relief=tk.RAISED,
            borderwidth=1
        )
        card.pack(fill=tk.X, padx=10, pady=5)
        
        # Couleur de bordure selon le type
        border_color = get_colors()['danger'] if is_spam == 1 else get_colors()['success']
        
        # Barre latérale colorée
        side_bar = tk.Frame(card, bg=border_color, width=5)
        side_bar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Contenu
        content = tk.Frame(card, bg="white")
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # En-tête
        header = tk.Frame(content, bg="white")
        header.pack(fill=tk.X)
        
        # Verdict
        verdict = "🚨 SPAM" if is_spam == 1 else "✅ HAM"
        tk.Label(
            header,
            text=verdict,
            font=("Arial", 12, "bold"),
            bg="white",
            fg=border_color
        ).pack(side=tk.LEFT)
        
        # Confiance
        tk.Label(
            header,
            text=f"{confidence_percent:.1f}%",
            font=("Arial", 11),
            bg="white",
            fg=get_colors()['secondary']
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Timestamp
        tk.Label(
            header,
            text=timestamp_str,
            font=("Arial", 9),
            bg="white",
            fg=get_colors()['secondary']
        ).pack(side=tk.RIGHT)
        
        # Message (tronqué)
        display_message = str(message)
        if len(display_message) > 100:
            display_message = display_message[:100] + "..."
        
        tk.Label(
            content,
            text=display_message,
            font=("Arial", 10),
            bg="white",
            fg=get_colors()['text'],
            wraplength=600,
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(5, 0))
        
        # Bouton détails
        details_btn = tk.Button(
            content,
            text="👁️ Voir détails",
            command=lambda p=prediction: self.show_details(p),
            font=("Arial", 9),
            bg=get_colors()['primary'],
            fg="white",
            padx=10,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        details_btn.pack(anchor=tk.E, pady=(5, 0))
    
    def show_details(self, prediction):
        """Affiche les détails d'une prédiction"""
        # Extraire les données
        prediction_value = prediction.get('prediction')
        if prediction_value is None:
            prediction_value = prediction.get('is_spam', 0)
        
        if isinstance(prediction_value, bool):
            is_spam = 1 if prediction_value else 0
        elif isinstance(prediction_value, str):
            is_spam = 1 if prediction_value.lower() == 'spam' or prediction_value == '1' else 0
        else:
            try:
                is_spam = int(prediction_value)
            except:
                is_spam = 0
        
        confidence = prediction.get('confidence', 0) or 0
        try:
            confidence_percent = float(confidence) * 100
        except:
            confidence_percent = 0
        
        # Probabilités
        ham_prob = prediction.get('ham_prob', 0)
        if ham_prob is None:
            ham_prob = prediction.get('ham_probability', 0) or 0
        
        spam_prob = prediction.get('spam_prob', 0)
        if spam_prob is None:
            spam_prob = prediction.get('spam_probability', 0) or 0
        
        try:
            ham_prob_percent = float(ham_prob) * 100
            spam_prob_percent = float(spam_prob) * 100
        except:
            ham_prob_percent = 0
            spam_prob_percent = 0
        
        message = prediction.get('message', '')
        if not message:
            message = prediction.get('original_message', '')
        
        timestamp = prediction.get('timestamp', 'N/A')
        model_version = prediction.get('model_version', 'N/A')
        
        details_window = tk.Toplevel(self)
        details_window.title("Détails de l'analyse")
        details_window.geometry("600x500")
        details_window.configure(bg="white")
        
        # En-tête
        header = tk.Frame(details_window, bg=get_colors()['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🔍 Détails de l'Analyse",
            font=("Arial", 16, "bold"),
            bg=get_colors()['primary'],
            fg="white"
        ).pack(pady=15)
        
        # Contenu scrollable
        scroll_frame = ScrollableFrame(details_window)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Verdict
        verdict = "🚨 SPAM DÉTECTÉ" if is_spam == 1 else "✅ MESSAGE LÉGITIME"
        verdict_color = get_colors()['danger'] if is_spam == 1 else get_colors()['success']
        
        tk.Label(
            scroll_frame.scrollable_frame,
            text=verdict,
            font=("Arial", 18, "bold"),
            bg="white",
            fg=verdict_color
        ).pack(pady=(0, 20))
        
        # Informations
        info_frame = tk.Frame(scroll_frame.scrollable_frame, bg="white")
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Confiance
        self.add_info_row(info_frame, "Confiance:", f"{confidence_percent:.2f}%")
        
        # Probabilités
        self.add_info_row(info_frame, "Prob. HAM:", f"{ham_prob_percent:.2f}%")
        self.add_info_row(info_frame, "Prob. SPAM:", f"{spam_prob_percent:.2f}%")
        
        # Timestamp
        self.add_info_row(info_frame, "Date/Heure:", timestamp)
        
        # Version du modèle
        self.add_info_row(info_frame, "Version:", model_version)
        
        # Séparateur
        tk.Frame(scroll_frame.scrollable_frame, bg="#e0e0e0", height=1).pack(fill=tk.X, pady=20)
        
        # Message original
        tk.Label(
            scroll_frame.scrollable_frame,
            text="Message Original:",
            font=("Arial", 12, "bold"),
            bg="white",
            fg=get_colors()['text']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        message_text = tk.Text(
            scroll_frame.scrollable_frame,
            height=10,
            font=("Arial", 10),
            bg="#f8f9fa",
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        message_text.pack(fill=tk.BOTH, expand=True)
        message_text.insert("1.0", message)
        message_text.config(state=tk.DISABLED)
        
        # Bouton fermer
        tk.Button(
            details_window,
            text="Fermer",
            command=details_window.destroy,
            font=("Arial", 11),
            bg=get_colors()['secondary'],
            fg="white",
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(pady=20)
    
    def add_info_row(self, parent, label, value):
        """Ajoute une ligne d'information"""
        row = tk.Frame(parent, bg="white")
        row.pack(fill=tk.X, pady=5)
        
        tk.Label(
            row,
            text=label,
            font=("Arial", 10, "bold"),
            bg="white",
            fg=get_colors()['text'],
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        tk.Label(
            row,
            text=value,
            font=("Arial", 10),
            bg="white",
            fg=get_colors()['secondary'],
            anchor=tk.W
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def export_history(self):
        """Exporte l'historique en CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                title="Exporter l'historique",
                defaultextension=".csv",
                filetypes=[("CSV", "*.csv"), ("Tous", "*.*")]
            )
            
            if filename:
                # Utiliser le service de stats pour l'export
                from services import StatisticsService
                stats_service = StatisticsService()
                
                if stats_service.export_statistics(filename, format='csv'):
                    messagebox.showinfo("Succès", f"Historique exporté:\n{filename}")
                    logger.info(f"✅ Export réussi: {filename}")
                else:
                    messagebox.showerror("Erreur", "Échec de l'export")
                    
        except Exception as e:
            logger.error(f"❌ Erreur export: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'export:\n{str(e)}")
    
    def clear_history(self):
        """Efface l'historique"""
        response = messagebox.askyesno(
            "Confirmation",
            "Êtes-vous sûr de vouloir effacer tout l'historique ?\n\n"
            "Cette action est irréversible."
        )
        
        if response:
            try:
                # Effacer via la base de données
                from database import DatabaseManager
                db = DatabaseManager()
                deleted = db.clear_old_data(days=0)  # Effacer tout
                
                self.predictions = []
                self.filtered_predictions = []
                self.display_predictions()
                
                messagebox.showinfo("Succès", f"Historique effacé ({deleted} entrées)")
                logger.info(f"✅ Historique effacé: {deleted} entrées")
                
            except Exception as e:
                logger.error(f"❌ Erreur effacement: {e}")
                messagebox.showerror("Erreur", f"Erreur:\n{str(e)}")