# views/dashboard_tab.py
"""
Onglet Dashboard moderne avec statistiques avancées
"""
import tkinter as tk
from tkinter import ttk, font
import logging
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.dates as mdates

from config.styles import StyleManager
from .components import ModernCard, ModernButton, ProgressRing, ScrollableFrame
from views.templates import DashboardTemplate

logger = logging.getLogger(__name__)

class DashboardTab(tk.Frame):
    """Onglet principal moderne avec statistiques et visualisations"""
    
    def __init__(self, parent, stats_service, **kwargs):
        super().__init__(parent, bg=StyleManager.get_color('background'), **kwargs)
        
        self.stats_service = stats_service
        self.metrics = {}
        self.charts = {}
        
        # Définir refresh_data
        self.refresh_data = self._refresh_data
        
        self.create_modern_interface()
        self._refresh_data()
    
    def create_modern_interface(self):
        """Crée une interface moderne et responsive"""
        
        # Container principal avec scroll
        scroll_frame = ScrollableFrame(self)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        main_container = tk.Frame(scroll_frame.scrollable_frame, 
                                 bg=StyleManager.get_color('background'))
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # ========== EN-TÊTE MODERNE ==========
        header = self.create_modern_header(main_container)
        header.pack(fill=tk.X, pady=(0, 40))
        
        # ========== SECTION MÉTRIQUES PRINCIPALES ==========
        metrics_section = self.create_metrics_section(main_container)
        metrics_section.pack(fill=tk.X, pady=(0, 40))
        
        # ========== SECTION VISUALISATIONS ==========
        visualizations_section = self.create_visualizations_section(main_container)
        visualizations_section.pack(fill=tk.BOTH, expand=True, pady=(0, 40))
        
        # ========== SECTION ANALYSE ==========
        analysis_section = self.create_analysis_section(main_container)
        analysis_section.pack(fill=tk.X, pady=(0, 30))
        
        # ========== PIED DE PAGE ==========
        footer = self.create_footer(main_container)
        footer.pack(fill=tk.X)
    
    def create_modern_header(self, parent):
        """Crée un en-tête moderne"""
        header_frame = tk.Frame(parent, bg=StyleManager.get_color('background'))
        
        # Titre principal avec icône
        title_frame = tk.Frame(header_frame, bg=StyleManager.get_color('background'))
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Icône et titre
        icon_label = tk.Label(title_frame, 
                             text="📊",
                             font=("Segoe UI", 36),
                             bg=StyleManager.get_color('background'),
                             fg=StyleManager.get_color('primary'))
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        text_frame = tk.Frame(title_frame, bg=StyleManager.get_color('background'))
        text_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.title_label = tk.Label(text_frame,
                                   text="Tableau de Bord Analytique",
                                   font=("Segoe UI", 24, "bold"),
                                   bg=StyleManager.get_color('background'),
                                   fg=StyleManager.get_color('text_primary'))
        self.title_label.pack(anchor=tk.W)
        
        self.subtitle_label = tk.Label(text_frame,
                                      text="Surveillance en temps réel des analyses de spam",
                                      font=("Segoe UI", 12),
                                      bg=StyleManager.get_color('background'),
                                      fg=StyleManager.get_color('text_secondary'))
        self.subtitle_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Actions rapides
        actions_frame = tk.Frame(header_frame, bg=StyleManager.get_color('background'))
        actions_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bouton d'actualisation
        self.refresh_btn = ModernButton(actions_frame,
                                       text="Actualiser",
                                       icon="refresh",
                                       variant="primary",
                                       command=self.refresh_data)
        self.refresh_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Indicateur de dernière mise à jour
        update_frame = tk.Frame(actions_frame, bg=StyleManager.get_color('background'))
        update_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20))
        
        self.last_update_icon = tk.Label(update_frame,
                                        text="🕒",
                                        font=("Segoe UI", 12),
                                        bg=StyleManager.get_color('background'),
                                        fg=StyleManager.get_color('text_secondary'))
        self.last_update_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        self.last_update_label = tk.Label(update_frame,
                                         text="Dernière mise à jour : --:--",
                                         font=("Segoe UI", 10),
                                         bg=StyleManager.get_color('background'),
                                         fg=StyleManager.get_color('text_secondary'))
        self.last_update_label.pack(side=tk.LEFT)
        
        return header_frame
    
    def create_metrics_section(self, parent):
        """Crée la section des métriques principales"""
        section_frame = tk.Frame(parent, bg=StyleManager.get_color('background'))
        
        # Titre de section
        section_header = tk.Frame(section_frame, bg=StyleManager.get_color('background'))
        section_header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(section_header,
                text="📈 Métriques Clés",
                font=("Segoe UI", 18, "bold"),
                bg=StyleManager.get_color('background'),
                fg=StyleManager.get_color('text_primary')).pack(side=tk.LEFT)
        
        # Grille de métriques (2x2)
        metrics_grid = tk.Frame(section_frame, bg=StyleManager.get_color('background'))
        metrics_grid.pack(fill=tk.X)
        
        # Métrique 1: Total Analyses
        self.metrics['total'] = self.create_metric_card(
            metrics_grid, 
            "Total Analyses", 
            "📊", 
            "0",
            StyleManager.get_color('primary'),
            row=0, col=0
        )
        
        # Métrique 2: Taux de Spam
        self.metrics['spam_rate'] = self.create_metric_card(
            metrics_grid, 
            "Taux de Spam", 
            "🚨", 
            "0%",
            StyleManager.get_color('danger'),
            row=0, col=1
        )
        
        # Métrique 3: Précision
        self.metrics['accuracy'] = self.create_metric_card(
            metrics_grid, 
            "Précision Moyenne", 
            "🎯", 
            "0%",
            StyleManager.get_color('success'),
            row=1, col=0
        )
        
        # Métrique 4: Dernière analyse
        self.metrics['recent'] = self.create_metric_card(
            metrics_grid, 
            "Analyses (24h)", 
            "⏱️", 
            "0",
            StyleManager.get_color('info'),
            row=1, col=1
        )
        
        # Configurer le grid
        for i in range(2):
            metrics_grid.grid_rowconfigure(i, weight=1, uniform="metric_row")
            metrics_grid.grid_columnconfigure(i, weight=1, uniform="metric_col")
        
        return section_frame
    
    def create_metric_card(self, parent, title, icon, value, color, row, col):
        """Crée une carte de métrique moderne"""
        card = ModernCard(parent,
                         title=title,
                         icon=None,  # On gère l'icône manuellement
                         variant='elevated')
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Contenu de la carte
        content = tk.Frame(card.content_frame, bg=StyleManager.get_color('surface'))
        content.pack(fill=tk.BOTH, expand=True)
        
        # Icône et valeur
        top_frame = tk.Frame(content, bg=StyleManager.get_color('surface'))
        top_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Icône
        icon_label = tk.Label(top_frame,
                             text=icon,
                             font=("Segoe UI", 24),
                             bg=StyleManager.get_color('surface'),
                             fg=color)
        icon_label.pack(side=tk.LEFT, padx=(20, 15))
        
        # Valeur
        value_frame = tk.Frame(top_frame, bg=StyleManager.get_color('surface'))
        value_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        value_label = tk.Label(value_frame,
                              text=value,
                              font=("Segoe UI", 28, "bold"),
                              bg=StyleManager.get_color('surface'),
                              fg=StyleManager.get_color('text_primary'))
        value_label.pack(anchor=tk.W)
        
        # Label de la valeur
        unit = "%" if "%" in value else ""
        value_text = tk.Label(value_frame,
                             text=title.split()[-1].lower() + unit,
                             font=("Segoe UI", 11),
                             bg=StyleManager.get_color('surface'),
                             fg=StyleManager.get_color('text_secondary'))
        value_text.pack(anchor=tk.W)
        
        # Barre de progression (si applicable)
        if "Taux" in title or "Précision" in title:
            progress_frame = tk.Frame(content, bg=StyleManager.get_color('surface'))
            progress_frame.pack(fill=tk.X, padx=20, pady=(15, 20))
            
            progress = ttk.Progressbar(progress_frame,
                                      length=200,
                                      mode='determinate',
                                      style="Modern.Horizontal.TProgressbar")
            progress.pack(fill=tk.X)
            
            # Configurer le style de la progressbar
            style = ttk.Style()
            style.configure("Modern.Horizontal.TProgressbar",
                           background=color,
                           troughcolor=StyleManager.get_color('hover'),
                           borderwidth=0,
                           thickness=6)
            
            return {'card': card, 'value_label': value_label, 'progress': progress}
        
        return {'card': card, 'value_label': value_label}
    
    def create_visualizations_section(self, parent):
        """Crée la section des visualisations"""
        section_frame = tk.Frame(parent, bg=StyleManager.get_color('background'))
        
        # Titre de section
        section_header = tk.Frame(section_frame, bg=StyleManager.get_color('background'))
        section_header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(section_header,
                text="📊 Visualisations",
                font=("Segoe UI", 18, "bold"),
                bg=StyleManager.get_color('background'),
                fg=StyleManager.get_color('text_primary')).pack(side=tk.LEFT)
        
        # Contrôles du graphique
        controls_frame = tk.Frame(section_header, bg=StyleManager.get_color('background'))
        controls_frame.pack(side=tk.RIGHT)
        
        tk.Label(controls_frame,
                text="Période :",
                font=("Segoe UI", 11),
                bg=StyleManager.get_color('background'),
                fg=StyleManager.get_color('text_secondary')).pack(side=tk.LEFT, padx=(0, 10))
        
        self.period_var = tk.StringVar(value="7 jours")
        period_combo = ttk.Combobox(controls_frame,
                                   textvariable=self.period_var,
                                   values=["7 jours", "14 jours", "30 jours", "90 jours"],
                                   state="readonly",
                                   width=12,
                                   font=("Segoe UI", 10))
        period_combo.pack(side=tk.LEFT)
        period_combo.bind("<<ComboboxSelected>>", lambda e: self._refresh_graph())
        
        # Conteneur pour graphiques
        charts_container = tk.Frame(section_frame, bg=StyleManager.get_color('background'))
        charts_container.pack(fill=tk.BOTH, expand=True)
        
        # Graphique principal (75% largeur) - Utilisation de grid pour un contrôle précis
        main_chart_frame = tk.Frame(charts_container, bg=StyleManager.get_color('background'))
        main_chart_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        # Configurer les proportions de colonnes
        charts_container.grid_columnconfigure(0, weight=3)  # Graphique principal (75%)
        charts_container.grid_columnconfigure(1, weight=1)  # Graphiques secondaires (25%)
        charts_container.grid_rowconfigure(0, weight=1)
        
        self.charts['main'] = self.create_chart_card(main_chart_frame, "Évolution des Analyses")
        
        # Graphiques secondaires (25% largeur) - CORRECTION ICI
        side_charts_frame = tk.Frame(charts_container, bg=StyleManager.get_color('background'))
        side_charts_frame.grid(row=0, column=1, sticky="nsew")
        
        # Anneau de progression pour répartition
        distribution_card = ModernCard(side_charts_frame,
                                      title="Répartition",
                                      subtitle="Spam vs Ham",
                                      variant='elevated')
        distribution_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        distribution_frame = tk.Frame(distribution_card.content_frame, 
                                     bg=StyleManager.get_color('surface'))
        distribution_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.charts['distribution'] = ProgressRing(distribution_frame, size=150, thickness=20)
        self.charts['distribution'].pack(expand=True)
        
        # Légende
        legend_frame = tk.Frame(distribution_frame, bg=StyleManager.get_color('surface'))
        legend_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Légende Spam
        spam_legend = tk.Frame(legend_frame, bg=StyleManager.get_color('surface'))
        spam_legend.pack(side=tk.LEFT, expand=True)
        
        tk.Label(spam_legend, text="●", 
                font=("Segoe UI", 16),
                fg=StyleManager.get_color('danger'),
                bg=StyleManager.get_color('surface')).pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(spam_legend, text="SPAM", 
                font=("Segoe UI", 10),
                fg=StyleManager.get_color('text_secondary'),
                bg=StyleManager.get_color('surface')).pack(side=tk.LEFT)
        
        # Légende Ham
        ham_legend = tk.Frame(legend_frame, bg=StyleManager.get_color('surface'))
        ham_legend.pack(side=tk.RIGHT, expand=True)
        
        tk.Label(ham_legend, text="●", 
                font=("Segoe UI", 16),
                fg=StyleManager.get_color('success'),
                bg=StyleManager.get_color('surface')).pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(ham_legend, text="HAM", 
                font=("Segoe UI", 10),
                fg=StyleManager.get_color('text_secondary'),
                bg=StyleManager.get_color('surface')).pack(side=tk.LEFT)
        
        return section_frame
    
    def create_chart_card(self, parent, title):
        """Crée une carte avec un graphique"""
        card = ModernCard(parent,
                         title=title,
                         subtitle="Cliquez pour interagir",
                         variant='elevated')
        card.pack(fill=tk.BOTH, expand=True)
        
        # Conteneur pour le graphique matplotlib
        chart_container = tk.Frame(card.content_frame, 
                                  bg=StyleManager.get_color('surface'))
        chart_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Créer la figure matplotlib
        fig = Figure(figsize=(8, 4), dpi=100, facecolor=StyleManager.get_color('surface'))
        ax = fig.add_subplot(111)
        
        # Style matplotlib selon le thème
        if StyleManager.get_current_theme() == 'dark':
            fig.patch.set_facecolor(StyleManager.get_color('surface'))
            ax.set_facecolor(StyleManager.get_color('surface'))
            ax.spines['bottom'].set_color(StyleManager.get_color('border'))
            ax.spines['left'].set_color(StyleManager.get_color('border'))
            ax.spines['top'].set_color(StyleManager.get_color('surface'))
            ax.spines['right'].set_color(StyleManager.get_color('surface'))
            ax.tick_params(colors=StyleManager.get_color('text_secondary'))
            ax.xaxis.label.set_color(StyleManager.get_color('text_primary'))
            ax.yaxis.label.set_color(StyleManager.get_color('text_primary'))
            ax.title.set_color(StyleManager.get_color('text_primary'))
        else:
            ax.set_facecolor('#f8f9fa')
        
        # Grid
        ax.grid(True, alpha=0.3, linestyle='--', color=StyleManager.get_color('border'))
        
        # Canvas Tkinter
        canvas = FigureCanvasTkAgg(fig, chart_container)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Barre d'outils de navigation
        toolbar = NavigationToolbar2Tk(canvas, chart_container)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        return {'card': card, 'fig': fig, 'ax': ax, 'canvas': canvas, 'toolbar': toolbar}
    
    def create_analysis_section(self, parent):
        """Crée la section d'analyse des tendances"""
        section_frame = tk.Frame(parent, bg=StyleManager.get_color('background'))
        
        # Titre de section
        section_header = tk.Frame(section_frame, bg=StyleManager.get_color('background'))
        section_header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(section_header,
                text="📈 Analyse des Tendances",
                font=("Segoe UI", 18, "bold"),
                bg=StyleManager.get_color('background'),
                fg=StyleManager.get_color('text_primary')).pack(side=tk.LEFT)
        
        # Carte d'analyse
        analysis_card = ModernCard(section_frame,
                                  title="Performance du Modèle",
                                  subtitle="Dernières 24 heures",
                                  variant='elevated')
        analysis_card.pack(fill=tk.X)
        
        # Contenu de l'analyse
        content = analysis_card.content_frame
        
        # Indicateurs en ligne
        indicators_frame = tk.Frame(content, bg=StyleManager.get_color('surface'))
        indicators_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Indicateur 1: Tendance
        trend_indicator = self.create_analysis_indicator(
            indicators_frame,
            "Tendance",
            "→",
            "Stable",
            StyleManager.get_color('info'),
            0
        )
        
        # Indicateur 2: Précision
        accuracy_indicator = self.create_analysis_indicator(
            indicators_frame,
            "Précision",
            "🎯",
            "0%",
            StyleManager.get_color('success'),
            1
        )
        
        # Indicateur 3: Vitesse
        speed_indicator = self.create_analysis_indicator(
            indicators_frame,
            "Vitesse",
            "⚡",
            "0 ms",
            StyleManager.get_color('warning'),
            2
        )
        
        # Indicateur 4: Volume
        volume_indicator = self.create_analysis_indicator(
            indicators_frame,
            "Volume",
            "📊",
            "0/h",
            StyleManager.get_color('primary'),
            3
        )
        
        return section_frame
    
    def create_analysis_indicator(self, parent, title, icon, value, color, column):
        """Crée un indicateur d'analyse"""
        indicator_frame = tk.Frame(parent, bg=StyleManager.get_color('surface'))
        indicator_frame.grid(row=0, column=column, padx=10, pady=5, sticky='nsew')
        
        parent.grid_columnconfigure(column, weight=1)
        
        # Icône
        icon_label = tk.Label(indicator_frame,
                             text=icon,
                             font=("Segoe UI", 20),
                             bg=StyleManager.get_color('surface'),
                             fg=color)
        icon_label.pack(pady=(0, 10))
        
        # Valeur
        value_label = tk.Label(indicator_frame,
                              text=value,
                              font=("Segoe UI", 18, "bold"),
                              bg=StyleManager.get_color('surface'),
                              fg=StyleManager.get_color('text_primary'))
        value_label.pack()
        
        # Titre
        title_label = tk.Label(indicator_frame,
                              text=title,
                              font=("Segoe UI", 11),
                              bg=StyleManager.get_color('surface'),
                              fg=StyleManager.get_color('text_secondary'))
        title_label.pack(pady=(5, 0))
        
        return {'frame': indicator_frame, 'value_label': value_label}
    
    def create_footer(self, parent):
        """Crée le pied de page avec des informations système"""
        footer_frame = tk.Frame(parent, bg=StyleManager.get_color('background'))
        
        # Informations système
        info_card = ModernCard(footer_frame,
                              title="Informations Système",
                              variant='outline')
        info_card.pack(fill=tk.X)
        
        info_content = tk.Frame(info_card.content_frame, bg=StyleManager.get_color('surface'))
        info_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Informations
        infos = [
            ("🖥️", "Statut", "🟢 Opérationnel"),
            ("🗄️", "Base de données", "Connectée"),
            ("🤖", "Modèle ML", "Chargé"),
            ("⏱️", "Dernier entraînement", "Il y a 7 jours")
        ]
        
        for icon, label, value in infos:
            info_row = tk.Frame(info_content, bg=StyleManager.get_color('surface'))
            info_row.pack(fill=tk.X, pady=5)
            
            tk.Label(info_row, text=icon,
                    font=("Segoe UI", 12),
                    bg=StyleManager.get_color('surface'),
                    fg=StyleManager.get_color('text_secondary')).pack(side=tk.LEFT, padx=(0, 10))
            
            tk.Label(info_row, text=label,
                    font=("Segoe UI", 10, "bold"),
                    bg=StyleManager.get_color('surface'),
                    fg=StyleManager.get_color('text_secondary'),
                    width=15,
                    anchor=tk.W).pack(side=tk.LEFT)
            
            tk.Label(info_row, text=value,
                    font=("Segoe UI", 10),
                    bg=StyleManager.get_color('surface'),
                    fg=StyleManager.get_color('text_primary')).pack(side=tk.LEFT)
        
        return footer_frame
    
    def _refresh_graph(self):
        """Actualise le graphique principal"""
        try:
            # Récupérer la période
            period_text = self.period_var.get()
            days = int(period_text.split()[0])  # "7 jours" -> 7
            
            # Récupérer les données
            daily_stats = self.stats_service.get_daily_statistics(days=days)
            
            if not daily_stats:
                logger.warning("⚠️ Pas de données pour le graphique")
                return
            
            # Préparer les données
            dates = []
            spam_counts = []
            ham_counts = []
            
            for stat in daily_stats:
                dates.append(datetime.strptime(stat['date'], '%Y-%m-%d'))
                spam_counts.append(stat.get('spam_count', 0))
                ham_counts.append(stat.get('ham_count', 0))
            
            # Nettoyer l'axe
            chart = self.charts['main']
            chart['ax'].clear()
            
            # Tracer les lignes avec style moderne
            chart['ax'].plot(dates, spam_counts, 
                           marker='o', 
                           markersize=6,
                           linewidth=2.5, 
                           color=StyleManager.get_color('danger'),
                           label='SPAM',
                           alpha=0.9)
            
            chart['ax'].plot(dates, ham_counts, 
                           marker='s', 
                           markersize=6,
                           linewidth=2.5, 
                           color=StyleManager.get_color('success'),
                           label='HAM',
                           alpha=0.9)
            
            # Configuration moderne
            chart['ax'].set_xlabel('Date', fontsize=11, fontweight='medium')
            chart['ax'].set_ylabel('Nombre de messages', fontsize=11, fontweight='medium')
            chart['ax'].set_title(f'Évolution sur {days} jours', fontsize=14, fontweight='bold', pad=15)
            
            # Légende stylée
            chart['ax'].legend(loc='upper left', framealpha=0.9, edgecolor=StyleManager.get_color('border'))
            
            # Format des dates
            chart['ax'].xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
            chart['ax'].xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days//7)))
            
            # Style selon le thème
            if StyleManager.get_current_theme() == 'dark':
                chart['ax'].set_facecolor(StyleManager.get_color('surface'))
                chart['fig'].patch.set_facecolor(StyleManager.get_color('surface'))
                chart['ax'].spines['bottom'].set_color(StyleManager.get_color('border'))
                chart['ax'].spines['left'].set_color(StyleManager.get_color('border'))
                chart['ax'].spines['top'].set_color(StyleManager.get_color('surface'))
                chart['ax'].spines['right'].set_color(StyleManager.get_color('surface'))
                chart['ax'].tick_params(colors=StyleManager.get_color('text_secondary'))
                chart['ax'].xaxis.label.set_color(StyleManager.get_color('text_primary'))
                chart['ax'].yaxis.label.set_color(StyleManager.get_color('text_primary'))
                chart['ax'].title.set_color(StyleManager.get_color('text_primary'))
            else:
                chart['ax'].set_facecolor('#f8f9fa')
            
            # Grid
            chart['ax'].grid(True, alpha=0.3, linestyle='--', color=StyleManager.get_color('border'))
            
            # Rotation des labels
            chart['fig'].autofmt_xdate(rotation=45)
            
            # CORRECTION : Utiliser tight_layout avec des paramètres
            try:
                chart['fig'].tight_layout(rect=[0, 0, 1, 0.95])  # Garde de l'espace pour le titre
            except Exception as layout_error:
                logger.warning(f"Note layout: {layout_error}")
                # Fallback: ajustement manuel
                chart['fig'].subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)
            
            # Redessiner
            chart['canvas'].draw()
            
            logger.info(f"✅ Graphique actualisé ({days} jours)")
            
        except Exception as e:
            logger.error(f"❌ Erreur actualisation graphique: {e}")
    
    def _refresh_data(self):
        """Actualise toutes les données du dashboard"""
        try:
            logger.info("🔄 Actualisation du dashboard...")
            
            # Désactiver le bouton pendant l'actualisation
            self.refresh_btn.config(state=tk.DISABLED)
            
            # Récupérer les stats
            global_stats = self.stats_service.get_global_statistics() or {}
            
            # Calculer les métriques
            total = global_stats.get('total_predictions', 0) or 0
            spam = global_stats.get('total_spam', 0) or 0
            ham = global_stats.get('total_ham', 0) or 0
            avg_conf = global_stats.get('avg_confidence', 0) or 0
            
            # Convertir en nombres avec gestion d'erreurs
            try:
                total_int = int(total)
                spam_int = int(spam)
                ham_int = int(ham)
                avg_conf_percent = float(avg_conf) * 100 if avg_conf else 0
            except (ValueError, TypeError) as conv_error:
                logger.warning(f"Erreur conversion données: {conv_error}")
                total_int = spam_int = ham_int = 0
                avg_conf_percent = 0
            
            # Calculer le taux de spam
            spam_rate = (spam_int / total_int * 100) if total_int > 0 else 0
            
            # Mettre à jour les métriques avec vérification
            if 'total' in self.metrics and 'value_label' in self.metrics['total']:
                self.metrics['total']['value_label'].config(text=f"{total_int:,}")
            
            if 'spam_rate' in self.metrics and 'value_label' in self.metrics['spam_rate']:
                spam_rate_text = f"{spam_rate:.1f}%" if spam_rate > 0 else "0%"
                self.metrics['spam_rate']['value_label'].config(text=spam_rate_text)
                if 'progress' in self.metrics['spam_rate']:
                    # Limiter à 100% maximum
                    progress_value = min(spam_rate, 100)
                    self.metrics['spam_rate']['progress']['value'] = progress_value
            
            if 'accuracy' in self.metrics and 'value_label' in self.metrics['accuracy']:
                accuracy_text = f"{avg_conf_percent:.1f}%" if avg_conf_percent > 0 else "0%"
                self.metrics['accuracy']['value_label'].config(text=accuracy_text)
                if 'progress' in self.metrics['accuracy']:
                    # Limiter à 100% maximum
                    progress_value = min(avg_conf_percent, 100)
                    self.metrics['accuracy']['progress']['value'] = progress_value
            
            if 'recent' in self.metrics and 'value_label' in self.metrics['recent']:
                # Récupérer les données des dernières 24h
                try:
                    daily_stats = self.stats_service.get_daily_statistics(days=1)
                    recent_count = daily_stats[0].get('total_count', 0) if daily_stats else 0
                except:
                    recent_count = min(total_int, 50)  # Fallback
                self.metrics['recent']['value_label'].config(text=f"{recent_count}")
            
            # Mettre à jour l'anneau de distribution
            if 'distribution' in self.charts:
                spam_percentage = spam_rate
                # Limiter à 100%
                spam_percentage = min(spam_percentage, 100)
                self.charts['distribution'].set_progress(spam_percentage)
            
            # Actualiser le graphique
            self._refresh_graph()
            
            # Mettre à jour le timestamp
            now = datetime.now().strftime("%H:%M:%S")
            self.last_update_label.config(text=f"Dernière mise à jour : {now}")
            
            # Animation du bouton d'actualisation
            self.animate_refresh_button()
            
            logger.info("✅ Dashboard actualisé avec succès")
            
        except Exception as e:
            logger.error(f"❌ Erreur actualisation dashboard: {e}")
            # Afficher un message d'erreur à l'utilisateur
            error_msg = f"Erreur lors de l'actualisation: {str(e)[:50]}..."
            self.last_update_label.config(text=error_msg, fg=StyleManager.get_color('danger'))
        finally:
            # Réactiver le bouton
            self.refresh_btn.config(state=tk.NORMAL)
    
    def animate_refresh_button(self):
        """Anime le bouton d'actualisation"""
        original_text = self.refresh_btn.cget('text')
        original_bg = self.refresh_btn.cget('bg')
        
        # Changer temporairement
        self.refresh_btn.config(text="✓ Actualisé", bg=StyleManager.get_color('success'))
        
        # Revenir après 2 secondes
        self.after(2000, lambda: self.refresh_btn.config(text=original_text, bg=original_bg))