# views/components.py
"""
Composants UI réutilisables
"""
import tkinter as tk
from tkinter import ttk
import logging

logger = logging.getLogger(__name__)

class Card(tk.Frame):
    """Composant Card pour afficher des statistiques"""
    
    def __init__(self, parent, title, value, icon="📊", color="#2196F3", **kwargs):
        super().__init__(parent, bg="white", relief=tk.RAISED, borderwidth=1, **kwargs)
        
        self.color = color
        
        # Container
        container = tk.Frame(self, bg="white")
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Icône et titre
        header = tk.Frame(container, bg="white")
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=icon,
            font=("Arial", 24),
            bg="white"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            header,
            text=title,
            font=("Arial", 11),
            bg="white",
            fg="#757575"
        ).pack(side=tk.LEFT, anchor=tk.W)
        
        # Valeur
        self.value_label = tk.Label(
            container,
            text=str(value),
            font=("Arial", 28, "bold"),
            bg="white",
            fg=color
        )
        self.value_label.pack(pady=(10, 0), anchor=tk.W)
    
    def update_value(self, new_value):
        """Met à jour la valeur affichée"""
        self.value_label.config(text=str(new_value))


class ProgressCard(tk.Frame):
    """Card avec barre de progression"""
    
    def __init__(self, parent, title, value, max_value=100, color="#4CAF50", **kwargs):
        super().__init__(parent, bg="white", relief=tk.RAISED, borderwidth=1, **kwargs)
        
        self.max_value = max_value
        self.color = color
        
        container = tk.Frame(self, bg="white")
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Titre
        tk.Label(
            container,
            text=title,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#333333"
        ).pack(anchor=tk.W)
        
        # Valeur et pourcentage
        info_frame = tk.Frame(container, bg="white")
        info_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.value_label = tk.Label(
            info_frame,
            text=str(value),
            font=("Arial", 20, "bold"),
            bg="white",
            fg=color
        )
        self.value_label.pack(side=tk.LEFT)
        
        percentage = (value / max_value * 100) if max_value > 0 else 0
        self.percentage_label = tk.Label(
            info_frame,
            text=f"({percentage:.1f}%)",
            font=("Arial", 11),
            bg="white",
            fg="#757575"
        )
        self.percentage_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Barre de progression
        style = ttk.Style()
        style_name = f"Progressbar.{color}"
        style.configure(style_name, 
                       background=color, 
                       troughcolor='#e0e0e0',
                       borderwidth=0,
                       thickness=10)
        
        self.progress = ttk.Progressbar(
            container,
            length=200,
            mode='determinate',
            style=f"{style_name}.Horizontal.TProgressbar",
            maximum=max_value
        )
        self.progress['value'] = value
        self.progress.pack(fill=tk.X)
    
    def update_value(self, new_value):
        """Met à jour la valeur"""
        self.value_label.config(text=str(new_value))
        percentage = (new_value / self.max_value * 100) if self.max_value > 0 else 0
        self.percentage_label.config(text=f"({percentage:.1f}%)")
        self.progress['value'] = new_value


class StatusIndicator(tk.Frame):
    """Indicateur de status coloré"""
    
    STATUS_COLORS = {
        'success': '#4CAF50',
        'warning': '#FF9800',
        'error': '#f44336',
        'info': '#2196F3'
    }
    
    def __init__(self, parent, status='info', message="", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.config(bg=self.STATUS_COLORS.get(status, '#2196F3'))
        
        container = tk.Frame(self, bg=self.STATUS_COLORS.get(status, '#2196F3'))
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        self.message_label = tk.Label(
            container,
            text=message,
            font=("Arial", 10),
            bg=self.STATUS_COLORS.get(status, '#2196F3'),
            fg="white"
        )
        self.message_label.pack()
    
    def update_status(self, status, message):
        """Met à jour le status"""
        color = self.STATUS_COLORS.get(status, '#2196F3')
        self.config(bg=color)
        self.message_label.config(text=message, bg=color)


class ScrollableFrame(tk.Frame):
    """Frame scrollable"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Canvas et scrollbar
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            self._on_frame_configure
        )
        
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel binding
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Garder une référence au binding
        self._bind_id = None
    
    def _on_frame_configure(self, event=None):
        """Mettre à jour la région de défilement quand le frame change de taille"""
        if self.canvas.winfo_exists():
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Redimensionner le frame scrollable quand le canvas change de taille"""
        if self.canvas.winfo_exists():
            self.canvas.itemconfig(self.window_id, width=event.width)
    
    def _on_mousewheel(self, event):
        """Gestion du défilement avec la molette"""
        try:
            if self.canvas.winfo_exists():
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError as e:
            # Ignorer les erreurs si le widget n'existe plus
            if "invalid command name" not in str(e):
                logger.debug(f"Ignoré erreur molette: {e}")
    
    def add_widget(self, widget, **kwargs):
        """Ajoute un widget au frame scrollable"""
        widget.pack(in_=self.scrollable_frame, **kwargs)
    
    def clear(self):
        """Efface tous les widgets du frame scrollable"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def destroy(self):
        """Nettoyage propre du widget"""
        try:
            # Supprimer les bindings
            if self.canvas.winfo_exists():
                self.canvas.unbind("<MouseWheel>")
                self.canvas.unbind("<Configure>")
        except:
            pass
        
        # Détruire les enfants d'abord
        try:
            self.scrollable_frame.destroy()
        except:
            pass
            
        try:
            self.canvas.destroy()
        except:
            pass
            
        try:
            self.scrollbar.destroy()
        except:
            pass
        
        # Appeler le destroy du parent
        super().destroy()