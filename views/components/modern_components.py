# views/components/modern_components.py
"""
Composants UI modernes et stylés
"""
import tkinter as tk
from tkinter import ttk
import logging
from config.styles import StyleManager

logger = logging.getLogger(__name__)

class ModernButton(tk.Button):
    """Bouton moderne avec styles avancés"""
    
    def __init__(self, parent, text="", variant='primary', icon=None, command=None, **kwargs):
        super().__init__(parent, text="", **kwargs)
        
        # Stocker les propriétés
        self.variant = variant
        self.original_text = text
        self.icon = icon
        
        # Appliquer le style
        self.apply_style()
        
        # Mettre à jour le texte avec l'icône
        self.update_display_text()
        
        # Effet hover personnalisé
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        
        # Commande
        if command:
            self.config(command=command)
    
    def apply_style(self):
        """Applique le style au bouton"""
        # Récupérer les couleurs selon le variant
        if self.variant == 'primary':
            bg = StyleManager.get_color('primary')
            fg = 'white'
            self.hover_bg = StyleManager.lighten_color(bg, 0.1)
        elif self.variant == 'secondary':
            bg = StyleManager.get_color('secondary')
            fg = 'white'
            self.hover_bg = StyleManager.lighten_color(bg, 0.1)
        elif self.variant == 'success':
            bg = StyleManager.get_color('success')
            fg = 'white'
            self.hover_bg = StyleManager.lighten_color(bg, 0.1)
        elif self.variant == 'danger':
            bg = StyleManager.get_color('danger')
            fg = 'white'
            self.hover_bg = StyleManager.lighten_color(bg, 0.1)
        elif self.variant == 'outline':
            bg = 'transparent'
            fg = StyleManager.get_color('primary')
            self.hover_bg = StyleManager.get_color('hover')
        else:
            bg = StyleManager.get_color('surface')
            fg = StyleManager.get_color('text_primary')
            self.hover_bg = StyleManager.get_color('hover')
        
        # Stocker la couleur originale
        self.original_bg = bg
        self.original_fg = fg
        
        # Appliquer la configuration
        self.config(
            bg=bg,
            fg=fg,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=10,
            cursor='hand2',
            activebackground=self.hover_bg,
            activeforeground=fg
        )
        
        # Si outline, ajouter une bordure
        if self.variant == 'outline':
            self.config(
                borderwidth=1,
                relief='solid',
                highlightbackground=StyleManager.get_color('primary'),
                highlightcolor=StyleManager.get_color('primary'),
                highlightthickness=1
            )
    
    def update_display_text(self):
        """Met à jour le texte avec l'icône"""
        display_text = self.original_text
        
        if self.icon:
            icon_char = StyleManager.get_icon(self.icon)
            display_text = f"{icon_char} {self.original_text}" if self.original_text else icon_char
        
        self.config(text=display_text)
    
    def _on_enter(self, event):
        """Effet hover"""
        try:
            current_bg = self.cget('bg')
            if current_bg != self.hover_bg:
                self.config(bg=self.hover_bg)
        except Exception as e:
            logger.error(f"Erreur effet hover: {e}")
    
    def _on_leave(self, event):
        """Fin de l'effet hover"""
        try:
            self.config(bg=self.original_bg)
        except Exception as e:
            logger.error(f"Erreur effet leave: {e}")
    
    def _on_press(self, event):
        """Effet de clic"""
        self.config(relief='sunken')
    
    def _on_release(self, event):
        """Fin de l'effet de clic"""
        self.config(relief='flat' if self.variant != 'outline' else 'solid')
    
    def set_variant(self, variant):
        """Change le variant du bouton"""
        self.variant = variant
        self.apply_style()
        self.update_display_text()


class ModernCard(tk.Frame):
    """Card moderne avec ombres et coins arrondis"""
    
    def __init__(self, parent, title="", subtitle="", icon=None, variant='default', **kwargs):
        super().__init__(parent, **kwargs)
        
        # Appliquer le style de base
        StyleManager.apply_style(self, 'card', variant)
        
        # Header
        self.header_frame = tk.Frame(self, bg=self.cget('bg'))
        self.header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        if icon:
            icon_label = tk.Label(self.header_frame, 
                                 text=StyleManager.get_icon(icon),
                                 font=("Segoe UI", 24),
                                 bg=self.cget('bg'))
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Titre et sous-titre
        title_frame = tk.Frame(self.header_frame, bg=self.cget('bg'))
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        if title:
            self.title_label = tk.Label(title_frame, text=title,
                                       font=("Segoe UI", 16, "bold"),
                                       bg=self.cget('bg'),
                                       fg=StyleManager.get_color('text_primary'))
            self.title_label.pack(anchor=tk.W)
        
        if subtitle:
            self.subtitle_label = tk.Label(title_frame, text=subtitle,
                                          font=("Segoe UI", 11),
                                          bg=self.cget('bg'),
                                          fg=StyleManager.get_color('text_secondary'))
            self.subtitle_label.pack(anchor=tk.W)
        
        # Content area
        self.content_frame = tk.Frame(self, bg=self.cget('bg'))
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    def add_content(self, widget, **kwargs):
        """Ajoute du contenu à la card"""
        widget.pack(in_=self.content_frame, **kwargs)


class ModernInput(tk.Frame):
    """Champ de saisie moderne avec label et validation"""
    
    def __init__(self, parent, label="", placeholder="", variant='default', **kwargs):
        super().__init__(parent, bg=StyleManager.get_color('background'), **kwargs)
        
        # Label
        if label:
            self.label = tk.Label(self, text=label,
                                 font=("Segoe UI", 11, "bold"),
                                 bg=self.cget('bg'),
                                 fg=StyleManager.get_color('text_primary'))
            self.label.pack(anchor=tk.W, pady=(0, 5))
        
        # Frame pour le champ de saisie avec bordure
        input_frame = tk.Frame(self, bg=StyleManager.get_color('surface'),
                              highlightbackground=StyleManager.get_color('border'),
                              highlightthickness=1,
                              highlightcolor=StyleManager.get_color('primary'))
        input_frame.pack(fill=tk.X)
        
        # Champ de saisie
        self.entry = tk.Entry(input_frame, 
                             font=("Segoe UI", 11),
                             bg=StyleManager.get_color('surface'),
                             fg=StyleManager.get_color('text_primary'),
                             borderwidth=0,
                             relief='flat',
                             insertbackground=StyleManager.get_color('primary'))
        self.entry.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Placeholder
        self.placeholder = placeholder
        if placeholder and not self.entry.get():
            self.entry.insert(0, placeholder)
            self.entry.config(fg=StyleManager.get_color('text_secondary'))
        
        # Événements
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        
        # Validation
        self.validation_callback = None
    
    def _on_focus_in(self, event):
        """Quand le champ reçoit le focus"""
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=StyleManager.get_color('text_primary'))
        
        # Animer la bordure
        self.master.config(highlightbackground=StyleManager.get_color('primary'),
                          highlightcolor=StyleManager.get_color('primary'))
    
    def _on_focus_out(self, event):
        """Quand le champ perd le focus"""
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=StyleManager.get_color('text_secondary'))
        
        self.master.config(highlightbackground=StyleManager.get_color('border'),
                          highlightcolor=StyleManager.get_color('border'))
    
    def get_value(self):
        """Récupère la valeur"""
        value = self.entry.get()
        return None if value == self.placeholder else value
    
    def set_value(self, value):
        """Définit la valeur"""
        self.entry.delete(0, tk.END)
        if value:
            self.entry.insert(0, value)
            self.entry.config(fg=StyleManager.get_color('text_primary'))
    
    def set_validation(self, callback):
        """Définit une fonction de validation"""
        self.validation_callback = callback
        self.entry.bind("<KeyRelease>", self._validate)
    
    def _validate(self, event):
        """Valide la saisie"""
        if self.validation_callback:
            value = self.get_value()
            is_valid, message = self.validation_callback(value)
            
            if is_valid:
                self.master.config(highlightbackground=StyleManager.get_color('success'))
            else:
                self.master.config(highlightbackground=StyleManager.get_color('danger'))


class ModernTable(ttk.Treeview):
    """Table moderne avec tri et style"""
    
    def __init__(self, parent, columns, show_headers=True, **kwargs):
        # Style pour Treeview
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurer le style
        style.configure("Modern.Treeview",
                       background=StyleManager.get_color('surface'),
                       foreground=StyleManager.get_color('text_primary'),
                       fieldbackground=StyleManager.get_color('surface'),
                       borderwidth=0,
                       font=("Segoe UI", 10))
        
        style.configure("Modern.Treeview.Heading",
                       background=StyleManager.get_color('background'),
                       foreground=StyleManager.get_color('text_primary'),
                       font=("Segoe UI", 11, "bold"),
                       relief='flat')
        
        style.map("Modern.Treeview",
                 background=[('selected', StyleManager.get_color('primary_light'))],
                 foreground=[('selected', 'white')])
        
        super().__init__(parent, columns=columns, show='headings', 
                        style="Modern.Treeview", **kwargs)
        
        # Configurer les colonnes
        for col in columns:
            self.heading(col, text=col.replace('_', ' ').title())
            self.column(col, width=100, anchor='w')
        
        # Barre de défilement moderne
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.yview)
        self.configure(yscrollcommand=scrollbar.set)
        
        # Alternance des couleurs de lignes
        self.tag_configure('oddrow', background=StyleManager.get_color('hover'))
        self.tag_configure('evenrow', background=StyleManager.get_color('surface'))
    
    def add_row(self, values, tags=()):
        """Ajoute une ligne avec alternance de couleurs"""
        row_id = self.insert('', 'end', values=values, tags=tags)
        
        # Alternance des couleurs
        if len(self.get_children()) % 2 == 0:
            self.item(row_id, tags=('evenrow',))
        else:
            self.item(row_id, tags=('oddrow',))
        
        return row_id


class ProgressRing(tk.Canvas):
    """Anneau de progression circulaire"""
    
    def __init__(self, parent, size=100, thickness=10, **kwargs):
        super().__init__(parent, width=size, height=size, 
                        highlightthickness=0, bg=StyleManager.get_color('background'), **kwargs)
        
        self.size = size
        self.thickness = thickness
        self.center = size // 2
        self.radius = (size - thickness) // 2
        
        self.progress = 0
        self.color = StyleManager.get_color('primary')
        self.bg_color = StyleManager.get_color('hover')
        
        self.draw_background()
        self.draw_progress()
    
    def draw_background(self):
        """Dessine l'anneau de fond"""
        self.create_oval(self.center - self.radius, self.center - self.radius,
                        self.center + self.radius, self.center + self.radius,
                        outline=self.bg_color, width=self.thickness)
    
    def draw_progress(self):
        """Dessine la progression"""
        if hasattr(self, 'progress_arc'):
            self.delete(self.progress_arc)
        
        if self.progress > 0:
            angle = 360 * self.progress / 100
            self.progress_arc = self.create_arc(self.center - self.radius, self.center - self.radius,
                                               self.center + self.radius, self.center + self.radius,
                                               start=90, extent=-angle,
                                               outline=self.color, width=self.thickness,
                                               style='arc')
    
    def set_progress(self, value):
        """Définit la valeur de progression (0-100)"""
        self.progress = max(0, min(100, value))
        self.draw_progress()