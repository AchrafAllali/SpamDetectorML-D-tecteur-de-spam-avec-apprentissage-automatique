# views/templates.py
"""
Templates de pages prédéfinis
"""
import tkinter as tk
from config.styles import StyleManager
from .components.modern_components import ModernCard, ModernButton

class DashboardTemplate:
    """Template pour les pages de tableau de bord"""
    
    @staticmethod
    def create_header(parent, title, subtitle="", actions=None):
        """Crée un en-tête de page"""
        header = tk.Frame(parent, bg=StyleManager.get_color('background'))
        
        # Titre
        title_frame = tk.Frame(header, bg=StyleManager.get_color('background'))
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(title_frame, text=title,
                font=("Segoe UI", 24, "bold"),
                bg=StyleManager.get_color('background'),
                fg=StyleManager.get_color('text_primary')).pack(anchor=tk.W)
        
        if subtitle:
            tk.Label(title_frame, text=subtitle,
                    font=("Segoe UI", 12),
                    bg=StyleManager.get_color('background'),
                    fg=StyleManager.get_color('text_secondary')).pack(anchor=tk.W, pady=(5, 0))
        
        # Actions
        if actions:
            actions_frame = tk.Frame(header, bg=StyleManager.get_color('background'))
            actions_frame.pack(side=tk.RIGHT)
            
            for action in actions:
                btn = ModernButton(actions_frame, 
                                  text=action['text'],
                                  icon=action.get('icon'),
                                  variant=action.get('variant', 'primary'),
                                  command=action['command'])
                btn.pack(side=tk.LEFT, padx=(5, 0))
        
        return header
    
    @staticmethod
    def create_metric_grid(parent, metrics):
        """Crée une grille de métriques"""
        grid_frame = tk.Frame(parent, bg=StyleManager.get_color('background'))
        
        for i, metric in enumerate(metrics):
            row = i // 3
            col = i % 3
            
            card = ModernCard(grid_frame,
                             title=metric['title'],
                             subtitle=metric.get('subtitle', ''),
                             icon=metric.get('icon'),
                             variant='elevated')
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Valeur
            tk.Label(card.content_frame, text=str(metric['value']),
                    font=("Segoe UI", 32, "bold"),
                    bg=StyleManager.get_color('surface'),
                    fg=StyleManager.get_color('text_primary')).pack()
            
            # Variation si présente
            if 'change' in metric:
                change_text = f"{metric['change']:+.1f}%"
                change_color = StyleManager.get_color('success') if metric['change'] >= 0 else StyleManager.get_color('danger')
                tk.Label(card.content_frame, text=change_text,
                        font=("Segoe UI", 11),
                        bg=StyleManager.get_color('surface'),
                        fg=change_color).pack()
            
            # Configurer le grid
            grid_frame.grid_columnconfigure(col, weight=1)
            grid_frame.grid_rowconfigure(row, weight=1)
        
        return grid_frame


class FormTemplate:
    """Template pour les formulaires"""
    
    @staticmethod
    def create_form(parent, fields):
        """Crée un formulaire à partir d'une liste de champs"""
        form_frame = ModernCard(parent, variant='elevated')
        
        inputs = {}
        for field in fields:
            # Créer le champ
            if field['type'] == 'text':
                input_widget = ModernInput(form_frame.content_frame,
                                          label=field['label'],
                                          placeholder=field.get('placeholder', ''))
            elif field['type'] == 'textarea':
                # À implémenter
                pass
            elif field['type'] == 'select':
                # À implémenter
                pass
            
            input_widget.pack(fill=tk.X, pady=(0, 15))
            inputs[field['name']] = input_widget
        
        return form_frame, inputs
    
    @staticmethod
    def create_form_actions(parent, actions):
        """Crée les boutons d'actions d'un formulaire"""
        actions_frame = tk.Frame(parent, bg=StyleManager.get_color('background'))
        
        for i, action in enumerate(reversed(actions)):
            btn = ModernButton(actions_frame,
                              text=action['text'],
                              icon=action.get('icon'),
                              variant=action.get('variant', 'primary'),
                              command=action['command'])
            btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        return actions_frame