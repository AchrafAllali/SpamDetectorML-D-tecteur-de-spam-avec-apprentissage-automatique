# views/main_window.py
"""
Fenêtre principale de l'application
"""
import tkinter as tk
from tkinter import ttk
import logging

from config.settings import get_colors, APP_INFO, UI_CONFIG
from controllers import AppController
from .dashboard_tab import DashboardTab
from .analysis_tab import AnalysisTab
from .history_tab import HistoryTab
from .settings_tab import SettingsTab

logger = logging.getLogger(__name__)

class MainWindow(tk.Tk):
    """Fenêtre principale de l'application"""
    
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre
        self.title(f"{APP_INFO['name']} v{APP_INFO['version']}")
        self.geometry(UI_CONFIG['window_size'])
        self.configure(bg=get_colors()['bg'])
        
        # Icône (optionnel)
        try:
            # self.iconbitmap('icon.ico')  # Si vous avez une icône
            pass
        except:
            pass
        
        # Contrôleur
        self.controller = AppController()
        
        # Créer l'interface
        self.create_widgets()
        
        # Protocole de fermeture
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        logger.info("✅ Fenêtre principale créée")
    
    def create_widgets(self):
        """Crée les widgets de la fenêtre"""
        
        # En-tête
        self.create_header()
        
        # Notebook (onglets)
        self.create_tabs()
        
        # Barre de statut
        self.create_status_bar()
    
    def create_header(self):
        """Crée l'en-tête"""
        header = tk.Frame(self, bg=get_colors()['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Container
        container = tk.Frame(header, bg=get_colors()['primary'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        # Titre
        title_frame = tk.Frame(container, bg=get_colors()['primary'])
        title_frame.pack(side=tk.LEFT)
        
        self.title_label = tk.Label(
            title_frame,
            text=APP_INFO['name'],
            font=("Arial", 20, "bold"),
            bg=get_colors()['primary'],
            fg="white"
        )
        self.title_label.pack(anchor=tk.W)
        
        self.description_label = tk.Label(
            title_frame,
            text=APP_INFO['description'],
            font=("Arial", 10),
            bg=get_colors()['primary'],
            fg="white"
        )
        self.description_label.pack(anchor=tk.W)
        
        # Version
        self.version_label = tk.Label(
            container,
            text=f"v{APP_INFO['version']}",
            font=("Arial", 10),
            bg=get_colors()['primary'],
            fg="white"
        )
        self.version_label.pack(side=tk.RIGHT)
        
        # S'abonner aux changements de police
        from config.config_manager import config_manager
        config_manager.register_callback('font_size', self.update_font_sizes)
        
        # S'abonner aux changements de langue
        from utils.translations import translation_manager
        translation_widgets = {
            self.title_label: 'app_title',
            self.description_label: 'app_description'
        }
        translation_manager.update_ui_widgets(translation_widgets)
    
    def create_tabs(self):
        """Crée les onglets"""
        # Style du notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            'Custom.TNotebook',
            background=get_colors()['bg'],
            borderwidth=0
        )
        style.configure(
            'Custom.TNotebook.Tab',
            padding=[20, 10],
            font=('Arial', 11)
        )
        
        # Notebook
        self.notebook = ttk.Notebook(self, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Onglet Dashboard
        self.dashboard_tab = DashboardTab(
            self.notebook,
            self.controller.get_statistics_service()
        )
        self.notebook.add(self.dashboard_tab, text="📊 Dashboard")
        
        # Onglet Analyse
        self.analysis_tab = AnalysisTab(
            self.notebook,
            self.controller.get_prediction_service()
        )
        self.notebook.add(self.analysis_tab, text="📧 Analyse")
        
        # Onglet Historique
        self.history_tab = HistoryTab(
            self.notebook,
            self.controller.get_prediction_service()
        )
        self.notebook.add(self.history_tab, text="📋 Historique")
        
        # Onglet Paramètres
        self.settings_tab = SettingsTab(self.notebook)
        self.notebook.add(self.settings_tab, text="⚙️ Paramètres")
        
        # Binding pour refresh automatique
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def create_status_bar(self):
        """Crée la barre de statut"""
        status_bar = tk.Frame(self, bg=get_colors()['secondary'], height=30)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        status_bar.pack_propagate(False)
        
        # Status label
        self.status_label = tk.Label(
            status_bar,
            text="✅ Prêt",
            font=("Arial", 9),
            bg=get_colors()['secondary'],
            fg="white",
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, padx=15)
        
        # Infos modèle
        model_info = self.controller.get_prediction_service().get_model_info()
        
        tk.Label(
            status_bar,
            text=f"Modèle: {model_info.get('algorithm', 'N/A')}",
            font=("Arial", 9),
            bg=get_colors()['secondary'],
            fg="white"
        ).pack(side=tk.RIGHT, padx=15)
    
    def on_tab_changed(self, event):
        """Callback lors du changement d'onglet"""
        try:
            selected_tab = self.notebook.select()
            tab_index = self.notebook.index(selected_tab)
            
            # Refresh selon l'onglet
            if tab_index == 0:  # Dashboard
                self.dashboard_tab.refresh_data()
                self.update_status("Dashboard actualisé")
            elif tab_index == 2:  # Historique
                self.history_tab.load_history()
                self.update_status("Historique actualisé")
            
        except Exception as e:
            logger.error(f"❌ Erreur changement onglet: {e}")
    
    def update_status(self, message):
        """Met à jour la barre de statut"""
        self.status_label.config(text=f"✅ {message}")
        logger.info(f"Status: {message}")
    
    def on_closing(self):
        """Gestion de la fermeture"""
        if tk.messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
            logger.info("👋 Fermeture de l'application...")
            self.controller.shutdown()
            self.destroy()
    def update_font_sizes(self, font_size):
        """Met à jour les tailles de police"""
        try:
            # Mettre à jour les labels
            self.title_label.config(font=("Arial", int(font_size) + 9, "bold"))
            self.description_label.config(font=("Arial", int(font_size) - 1))
            self.version_label.config(font=("Arial", int(font_size) - 1))
            
            # Mettre à jour la barre de statut
            self.status_label.config(font=("Arial", int(font_size) - 2))
            
            logger.info(f"🔤 Taille police mise à jour: {font_size}")
        except Exception as e:
            logger.error(f"❌ Erreur mise à jour police: {e}")