# views/settings_tab.py
"""
Onglet des paramètres
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
import os
import json
import shutil
from pathlib import Path

from config.settings import get_colors, UI_CONFIG, APP_INFO, MODEL_CONFIG, DATABASE_CONFIG, LOGGING_CONFIG
from .components import ScrollableFrame
from config.config_manager import config_manager

logger = logging.getLogger(__name__)

class SettingsTab(tk.Frame):
    """Onglet des paramètres"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=get_colors()['bg'], **kwargs)
        
        self.settings_vars = {}
        self.translated_widgets = {}  # Pour stocker les widgets à traduire
        
        # S'abonner aux changements de langue
        config_manager.register_callback('language', self.on_language_changed)
        
        self.create_widgets()
    
    def on_language_changed(self, new_language):
        """Met à jour l'interface quand la langue change"""
        logger.info(f"🌐 Mise à jour interface pour langue: {new_language}")
        # Mettre à jour tous les textes de l'onglet
    
    def create_widgets(self):
        """Crée les widgets"""
        
        # Container principal avec scroll
        scroll_frame = ScrollableFrame(self)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        main_container = scroll_frame.scrollable_frame
        
        # En-tête
        header = tk.Frame(main_container, bg="white")
        header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header,
            text="⚙️ Paramètres",
            font=("Arial", 18, "bold"),
            bg="white",
            fg=get_colors()['text']
        ).pack(anchor=tk.W)
        
        # === SECTION APPARENCE ===
        self.create_section(main_container, "🎨 Apparence")
        appearance_frame = self.create_card(main_container)
        
        # Thème - Utiliser la valeur chargée ou la valeur par défaut
        current_theme = config_manager.get_setting('theme', UI_CONFIG['theme'])
        self.add_combobox_setting(
            appearance_frame,
            "Thème:",
            "theme",
            ["light", "dark"],
            current_theme
        )
        
        # Langue
        current_language = config_manager.get_setting('language', UI_CONFIG['language'])
        self.add_combobox_setting(
            appearance_frame,
            "Langue:",
            "language",
            ["fr", "en"],
            current_language
        )
        
        # Taille de police
        current_font_size = config_manager.get_setting('font_size', UI_CONFIG['font_size'])
        self.add_spinbox_setting(
            appearance_frame,
            "Taille de police:",
            "font_size",
            from_=8,
            to=16,
            value=current_font_size
        )
        
        # === SECTION MODÈLE ===
        self.create_section(main_container, "🤖 Modèle ML")
        model_frame = self.create_card(main_container)
        
        # Algorithme
        current_algorithm = config_manager.get_setting('algorithm', MODEL_CONFIG['algorithm'])
        self.add_combobox_setting(
            model_frame,
            "Algorithme:",
            "algorithm",
            ["naive_bayes", "logistic_regression", "svm", "random_forest"],
            current_algorithm
        )
        
        # Features
        current_max_features = config_manager.get_setting('max_features', MODEL_CONFIG['max_features'])
        self.add_spinbox_setting(
            model_frame,
            "Nombre de features:",
            "max_features",
            from_=1000,
            to=5000,
            increment=500,
            value=current_max_features
        )
        
        # Seuil minimum
        current_min_accuracy = config_manager.get_setting('min_accuracy', MODEL_CONFIG['min_accuracy'])
        self.add_scale_setting(
            model_frame,
            "Seuil de confiance min:",
            "min_accuracy",
            from_=0.5,
            to=1.0,
            value=float(current_min_accuracy),
            resolution=0.05
        )
        
        # === SECTION BASE DE DONNÉES ===
        self.create_section(main_container, "🗄️ Base de Données")
        db_frame = self.create_card(main_container)
        
        # Chemin DB
        db_info = tk.Frame(db_frame, bg="white")
        db_info.pack(fill=tk.X, pady=5)
        
        tk.Label(
            db_info,
            text="Chemin:",
            font=("Arial", 10, "bold"),
            bg="white",
            width=20,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        db_path = DATABASE_CONFIG.get('db_path', 'Non spécifié')
        if isinstance(db_path, Path):
            db_path = str(db_path)
            
        tk.Label(
            db_info,
            text=db_path,
            font=("Arial", 9),
            bg="white",
            fg=get_colors()['secondary'],
            anchor=tk.W
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Backup
        backup_frame = tk.Frame(db_frame, bg="white")
        backup_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            backup_frame,
            text="Backup automatique:",
            font=("Arial", 10, "bold"),
            bg="white",
            width=20,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        current_backup_enabled = config_manager.get_setting('backup_enabled', DATABASE_CONFIG.get('backup_enabled', True))
        backup_var = tk.BooleanVar(value=current_backup_enabled)
        tk.Checkbutton(
            backup_frame,
            variable=backup_var,
            bg="white",
            command=lambda: self.toggle_setting('backup_enabled', backup_var.get())
        ).pack(side=tk.LEFT)
        self.settings_vars['backup_enabled'] = backup_var
        
        # Boutons DB
        db_buttons = tk.Frame(db_frame, bg="white")
        db_buttons.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(
            db_buttons,
            text="🔄 Optimiser DB",
            command=self.optimize_db,
            font=("Arial", 9),
            bg=get_colors()['primary'],
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(
            db_buttons,
            text="💾 Backup maintenant",
            command=self.backup_now,
            font=("Arial", 9),
            bg=get_colors()['success'],
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(
            db_buttons,
            text="🗑️ Nettoyer anciennes données",
            command=self.clean_old_data,
            font=("Arial", 9),
            bg=get_colors()['danger'],
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT)
        
        # === SECTION INFORMATIONS ===
        self.create_section(main_container, "ℹ️ Informations")
        info_frame = self.create_card(main_container)
        
        for key, value in APP_INFO.items():
            row = tk.Frame(info_frame, bg="white")
            row.pack(fill=tk.X, pady=3)
            
            tk.Label(
                row,
                text=f"{key.replace('_', ' ').title()}:",
                font=("Arial", 10, "bold"),
                bg="white",
                width=20,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row,
                text=str(value),
                font=("Arial", 10),
                bg="white",
                fg=get_colors()['secondary'],
                anchor=tk.W
            ).pack(side=tk.LEFT)
        
        # === SECTION ACTIONS ===
        self.create_section(main_container, "🔧 Actions")
        actions_frame = self.create_card(main_container)
        
        tk.Button(
            actions_frame,
            text="💾 Enregistrer les paramètres",
            command=self.save_settings,
            font=("Arial", 11, "bold"),
            bg=get_colors()['success'],
            fg="white",
            padx=30,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(pady=5)
        
        tk.Button(
            actions_frame,
            text="🔄 Réinitialiser par défaut",
            command=self.reset_settings,
            font=("Arial", 11),
            bg=get_colors()['warning'],
            fg="white",
            padx=30,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(pady=5)
        
        tk.Button(
            actions_frame,
            text="🔁 Réentraîner le modèle",
            command=self.retrain_model,
            font=("Arial", 11),
            bg=get_colors()['primary'],
            fg="white",
            padx=30,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(pady=5)
        
        tk.Button(
            actions_frame,
            text="📋 Exporter logs",
            command=self.export_logs,
            font=("Arial", 11),
            bg=get_colors()['secondary'],
            fg="white",
            padx=30,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(pady=5)
    
    def create_section(self, parent, title):
        """Crée un titre de section"""
        tk.Label(
            parent,
            text=title,
            font=("Arial", 14, "bold"),
            bg="white",
            fg=get_colors()['text']
        ).pack(anchor=tk.W, pady=(20, 10))
    
    def create_card(self, parent):
        """Crée une card"""
        card = tk.Frame(parent, bg="white", relief=tk.RAISED, borderwidth=1)
        card.pack(fill=tk.X, pady=(0, 10), padx=10)
        
        container = tk.Frame(card, bg="white")
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        return container
    
    def add_combobox_setting(self, parent, label, key, values, current_value):
        """Ajoute un paramètre Combobox"""
        row = tk.Frame(parent, bg="white")
        row.pack(fill=tk.X, pady=5)
        
        tk.Label(
            row,
            text=label,
            font=("Arial", 10, "bold"),
            bg="white",
            width=20,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        var = tk.StringVar(value=str(current_value))
        combobox = ttk.Combobox(
            row,
            textvariable=var,
            values=values,
            state="readonly",
            width=25
        )
        combobox.pack(side=tk.LEFT, padx=(10, 0))
        
        self.settings_vars[key] = var
        
        return combobox
    
    def add_spinbox_setting(self, parent, label, key, from_, to, value, increment=1):
        """Ajoute un paramètre Spinbox"""
        row = tk.Frame(parent, bg="white")
        row.pack(fill=tk.X, pady=5)
        
        tk.Label(
            row,
            text=label,
            font=("Arial", 10, "bold"),
            bg="white",
            width=20,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        var = tk.StringVar(value=str(value))
        spinbox = ttk.Spinbox(
            row,
            textvariable=var,
            from_=from_,
            to=to,
            increment=increment,
            width=25
        )
        spinbox.pack(side=tk.LEFT, padx=(10, 0))
        
        self.settings_vars[key] = var
        
        return spinbox
    
    def add_scale_setting(self, parent, label, key, from_, to, value, resolution=0.01):
        """Ajoute un paramètre Scale"""
        row = tk.Frame(parent, bg="white")
        row.pack(fill=tk.X, pady=5)
        
        tk.Label(
            row,
            text=label,
            font=("Arial", 10, "bold"),
            bg="white",
            width=20,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        var = tk.DoubleVar(value=float(value))
        
        # Frame pour le scale et le label de valeur
        scale_frame = tk.Frame(row, bg="white")
        scale_frame.pack(side=tk.LEFT, padx=(10, 0))
        
        scale = tk.Scale(
            scale_frame,
            variable=var,
            from_=from_,
            to=to,
            resolution=resolution,
            orient=tk.HORIZONTAL,
            length=150,
            bg="white",
            highlightthickness=0
        )
        scale.pack(side=tk.LEFT)
        
        # Label pour afficher la valeur
        value_label = tk.Label(
            scale_frame,
            text=f"{float(value):.2f}",
            font=("Arial", 10),
            bg="white",
            width=8
        )
        value_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Mettre à jour le label quand le scale change
        def update_label(val):
            try:
                value_label.config(text=f"{float(val):.2f}")
            except:
                pass
        
        scale.config(command=update_label)
        
        self.settings_vars[key] = var
        
        return scale
    
    def toggle_setting(self, key, value):
        """Active/désactive un paramètre"""
        logger.info(f"{key}: {'activé' if value else 'désactivé'}")
    
    def optimize_db(self):
        """Optimise la base de données"""
        try:
            from database.db_manager import DatabaseManager
            db = DatabaseManager()
            db.optimize_database()
            
            messagebox.showinfo("Succès", "Base de données optimisée !")
            logger.info("✅ DB optimisée")
        except Exception as e:
            logger.error(f"❌ Erreur optimisation DB: {e}")
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def backup_now(self):
        """Crée un backup maintenant"""
        try:
            from database.db_manager import DatabaseManager
            db = DatabaseManager()
            backup_path = db.create_backup()
            
            if backup_path:
                messagebox.showinfo("Succès", f"Backup créé:\n{backup_path}")
                logger.info(f"✅ Backup créé: {backup_path}")
            else:
                messagebox.showwarning("Attention", "Échec de création du backup")
        except Exception as e:
            logger.error(f"❌ Erreur backup: {e}")
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def clean_old_data(self):
        """Nettoie les anciennes données"""
        current_language = config_manager.get_setting('language', 'fr')
        
        response = messagebox.askyesno(
            "Confirmation" if current_language == 'fr' else "Confirm",
            "Supprimer les données de plus de 90 jours ?" if current_language == 'fr' else "Delete data older than 90 days?"
        )
        
        if response:
            try:
                from database.db_manager import DatabaseManager
                db = DatabaseManager()
                deleted = db.clear_old_data(days=90)
                
                message = f"{deleted} entrées supprimées" if current_language == 'fr' else f"{deleted} entries deleted"
                messagebox.showinfo("Succès" if current_language == 'fr' else "Success", message)
                logger.info(f"✅ {deleted} entrées supprimées")
            except Exception as e:
                logger.error(f"❌ Erreur nettoyage: {e}")
                messagebox.showerror("Erreur" if current_language == 'fr' else "Error", f"Erreur: {str(e)}")
    
    def save_settings(self):
        """Sauvegarde les paramètres"""
        try:
            # Récupérer toutes les valeurs
            settings = {}
            
            for key, var in self.settings_vars.items():
                if isinstance(var, tk.StringVar):
                    value = var.get()
                    # Convertir les nombres si nécessaire
                    if key == 'font_size':
                        try:
                            value = int(value)
                        except:
                            value = 11
                    elif key == 'max_features':
                        try:
                            value = int(value)
                        except:
                            value = 3000
                    settings[key] = value
                elif isinstance(var, tk.IntVar):
                    settings[key] = var.get()
                elif isinstance(var, tk.DoubleVar):
                    settings[key] = var.get()
                elif isinstance(var, tk.BooleanVar):
                    settings[key] = var.get()
            
            # Sauvegarder avec le ConfigManager
            if config_manager.save_settings(settings):
                current_language = config_manager.get_setting('language', 'fr')
                
                title = "Succès" if current_language == 'fr' else "Success"
                message = "Paramètres sauvegardés !\n\nRedémarrez pour certains changements." if current_language == 'fr' else "Settings saved!\n\nRestart for some changes."
                
                messagebox.showinfo(title, message)
                logger.info(f"✅ Paramètres sauvegardés: {settings}")
            else:
                current_language = config_manager.get_setting('language', 'fr')
                title = "Erreur" if current_language == 'fr' else "Error"
                message = "Échec de la sauvegarde" if current_language == 'fr' else "Save failed"
                messagebox.showerror(title, message)
                
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde paramètres: {e}")
            current_language = config_manager.get_setting('language', 'fr')
            title = "Erreur" if current_language == 'fr' else "Error"
            message = f"Erreur: {str(e)}" if current_language == 'fr' else f"Error: {str(e)}"
            messagebox.showerror(title, message)
    
    def reset_settings(self):
        """Réinitialise les paramètres"""
        current_language = config_manager.get_setting('language', 'fr')
        
        response = messagebox.askyesno(
            "Confirmation" if current_language == 'fr' else "Confirm",
            "Réinitialiser tous les paramètres par défaut ?" if current_language == 'fr' else "Reset all settings to default?"
        )
        
        if response:
            try:
                if config_manager.reset_settings():
                    # Réinitialiser les variables d'interface
                    self.settings_vars['theme'].set('light')
                    self.settings_vars['language'].set('fr')
                    self.settings_vars['font_size'].set('11')
                    self.settings_vars['algorithm'].set('naive_bayes')
                    self.settings_vars['max_features'].set('3000')
                    self.settings_vars['min_accuracy'].set(0.95)
                    self.settings_vars['backup_enabled'].set(True)
                    
                    messagebox.showinfo(
                        "Info" if current_language == 'fr' else "Info", 
                        "Paramètres réinitialisés" if current_language == 'fr' else "Settings reset"
                    )
                    logger.info("✅ Paramètres réinitialisés")
                else:
                    messagebox.showerror(
                        "Erreur" if current_language == 'fr' else "Error",
                        "Échec de la réinitialisation" if current_language == 'fr' else "Reset failed"
                    )
                    
            except Exception as e:
                logger.error(f"❌ Erreur réinitialisation: {e}")
                messagebox.showerror(
                    "Erreur" if current_language == 'fr' else "Error", 
                    f"Erreur: {str(e)}" if current_language == 'fr' else f"Error: {str(e)}"
                )
    
    def retrain_model(self):
        """Réentraîne le modèle"""
        current_language = config_manager.get_setting('language', 'fr')
        
        response = messagebox.askyesno(
            "Confirmation" if current_language == 'fr' else "Confirm",
            "Réentraîner le modèle ML ?\n\nCela peut prendre quelques minutes." if current_language == 'fr' else "Retrain ML model?\n\nThis may take a few minutes."
        )
        
        if response:
            try:
                # TODO: Implémenter le réentraînement
                messagebox.showinfo(
                    "Info" if current_language == 'fr' else "Info",
                    "Fonctionnalité en développement" if current_language == 'fr' else "Feature in development"
                )
                logger.info("ℹ️ Réentraînement demandé")
            except Exception as e:
                logger.error(f"❌ Erreur réentraînement: {e}")
                messagebox.showerror(
                    "Erreur" if current_language == 'fr' else "Error",
                    f"Erreur: {str(e)}" if current_language == 'fr' else f"Error: {str(e)}"
                )
    
    def export_logs(self):
        """Exporte les logs"""
        try:
            current_language = config_manager.get_setting('language', 'fr')
            
            filename = filedialog.asksaveasfilename(
                title="Exporter les logs" if current_language == 'fr' else "Export logs",
                defaultextension=".log",
                filetypes=[("Log files", "*.log"), ("All files", "*.*")]
            )
            
            if filename:
                log_file = Path(LOGGING_CONFIG.get('log_file', 'app.log'))
                if log_file.exists():
                    shutil.copy2(log_file, filename)
                    messagebox.showinfo(
                        "Succès" if current_language == 'fr' else "Success",
                        f"Logs exportés:\n{filename}" if current_language == 'fr' else f"Logs exported:\n{filename}"
                    )
                    logger.info(f"✅ Logs exportés: {filename}")
                else:
                    messagebox.showwarning(
                        "Attention" if current_language == 'fr' else "Warning",
                        "Fichier de logs non trouvé" if current_language == 'fr' else "Log file not found"
                    )
                    
        except Exception as e:
            logger.error(f"❌ Erreur export logs: {e}")
            current_language = config_manager.get_setting('language', 'fr')
            messagebox.showerror(
                "Erreur" if current_language == 'fr' else "Error",
                f"Erreur: {str(e)}" if current_language == 'fr' else f"Error: {str(e)}"
            )