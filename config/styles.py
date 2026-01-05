# config/styles.py
"""
Système de styles CSS-like pour Tkinter
"""
from .settings import get_colors
import tkinter as tk

class StyleManager:
    """Gestionnaire de styles CSS-like"""
    
    # Styles globaux
    GLOBAL_STYLES = {
        'font_family': 'Segoe UI',  # Police moderne
        'font_family_mono': 'Consolas',
        'border_radius': 8,
        'shadow_depth': 2,
        'transition_speed': 200,  # ms
    }
    
    # Palette de couleurs modernes
    COLOR_PALETTE = {
        # Thème clair
        'light': {
            'primary': '#4361ee',      # Bleu moderne
            'primary_light': '#4895ef',
            'primary_dark': '#3a0ca3',
            'secondary': '#7209b7',    # Violet
            'accent': '#f72585',       # Rose
            'success': '#4cc9f0',      # Cyan
            'warning': '#f8961e',      # Orange
            'danger': '#f94144',       # Rouge
            'info': '#577590',         # Bleu-gris
            'surface': '#ffffff',
            'background': '#f8f9fa',
            'text_primary': '#212529',
            'text_secondary': '#6c757d',
            'border': '#dee2e6',
            'hover': '#e9ecef',
            'shadow': 'rgba(0, 0, 0, 0.1)'
        },
        # Thème sombre
        'dark': {
            'primary': '#4361ee',
            'primary_light': '#4895ef',
            'primary_dark': '#3a0ca3',
            'secondary': '#9d4edd',
            'accent': '#f72585',
            'success': '#4cc9f0',
            'warning': '#f8961e',
            'danger': '#f94144',
            'info': '#577590',
            'surface': '#212529',
            'background': '#121212',
            'text_primary': '#f8f9fa',
            'text_secondary': '#adb5bd',
            'border': '#495057',
            'hover': '#343a40',
            'shadow': 'rgba(0, 0, 0, 0.3)'
        }
    }
    
    # Styles de composants
    COMPONENT_STYLES = {
        'button': {
            'default': {
                'font': ('Segoe UI', 11, 'normal'),
                'bg': '{primary}',
                'fg': 'white',
                'borderwidth': 0,
                'relief': 'flat',
                'padx': 20,
                'pady': 10,
                'cursor': 'hand2',
                'activebackground': '{primary_dark}',
                'activeforeground': 'white'
            },
            'primary': {
                'bg': '{primary}',
                'fg': 'white'
            },
            'secondary': {
                'bg': '{secondary}',
                'fg': 'white'
            },
            'success': {
                'bg': '{success}',
                'fg': 'white'
            },
            'danger': {
                'bg': '{danger}',
                'fg': 'white'
            },
            'outline': {
                'bg': 'transparent',
                'fg': '{primary}',
                'borderwidth': 2,
                'relief': 'solid'
            },
            'rounded': {
                'borderradius': 20
            }
        },
        
        'card': {
            'default': {
                'bg': '{surface}',
                'borderwidth': 1,
                'relief': 'flat',
                'highlightthickness': 0
            },
            'elevated': {
                'shadow': True,
                'borderradius': 12
            },
            'neumorphic': {
                'bg': '{background}',
                'borderwidth': 0,
                'highlightthickness': 0
            }
        },
        
        'input': {
            'default': {
                'font': ('Segoe UI', 11),
                'bg': '{surface}',
                'fg': '{text_primary}',
                'borderwidth': 1,
                'relief': 'solid',
                'insertbackground': '{primary}',
                'selectbackground': '{primary_light}',
                'selectforeground': 'white'
            },
            'rounded': {
                'borderradius': 8
            }
        },
        
        'label': {
            'default': {
                'font': ('Segoe UI', 11),
                'bg': 'transparent',
                'fg': '{text_primary}'
            },
            'title': {
                'font': ('Segoe UI', 24, 'bold')
            },
            'subtitle': {
                'font': ('Segoe UI', 16, 'semibold'),
                'fg': '{text_secondary}'
            },
            'caption': {
                'font': ('Segoe UI', 9),
                'fg': '{text_secondary}'
            }
        },
        
        'frame': {
            'default': {
                'bg': '{background}'
            },
            'surface': {
                'bg': '{surface}'
            }
        }
    }
    
    @classmethod
    def get_current_theme(cls):
        """Récupère le thème actuel"""
        from .config_manager import config_manager
        return config_manager.get_setting('theme', 'light')
    
    @classmethod
    def get_color(cls, color_name):
        """Récupère une couleur selon le thème"""
        theme = cls.get_current_theme()
        palette = cls.COLOR_PALETTE.get(theme, cls.COLOR_PALETTE['light'])
        return palette.get(color_name, color_name)
    
    @staticmethod
    def lighten_color(hex_color, factor=0.1):
        """
        Éclaircit une couleur hexadécimale.
        factor: 0.0 = pas de changement, 1.0 = blanc pur
        """
        try:
            # Nettoyer la couleur
            hex_color = hex_color.lstrip('#')
            
            # Convertir hex en RGB
            if len(hex_color) == 6:
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            elif len(hex_color) == 3:
                r, g, b = tuple(int(hex_color[i:i+1] * 2, 16) for i in (0, 1, 2))
            else:
                return hex_color
            
            # Éclaircir
            r = int(r + (255 - r) * factor)
            g = int(g + (255 - g) * factor)
            b = int(b + (255 - b) * factor)
            
            # S'assurer que les valeurs sont dans la plage 0-255
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            # Retourner en hex
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return hex_color
    
    @staticmethod
    def darken_color(hex_color, factor=0.1):
        """
        Assombrit une couleur hexadécimale.
        factor: 0.0 = pas de changement, 1.0 = noir pur
        """
        try:
            # Nettoyer la couleur
            hex_color = hex_color.lstrip('#')
            
            # Convertir hex en RGB
            if len(hex_color) == 6:
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            elif len(hex_color) == 3:
                r, g, b = tuple(int(hex_color[i:i+1] * 2, 16) for i in (0, 1, 2))
            else:
                return hex_color
            
            # Assombrir
            r = int(r * (1 - factor))
            g = int(g * (1 - factor))
            b = int(b * (1 - factor))
            
            # S'assurer que les valeurs sont dans la plage 0-255
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            # Retourner en hex
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return hex_color
    
    @classmethod
    def get_button_colors(cls, variant='primary'):
        """Récupère les couleurs pour un bouton selon son variant"""
        if variant == 'primary':
            bg = cls.get_color('primary')
            fg = 'white'
            hover_bg = cls.lighten_color(bg, 0.1)
        elif variant == 'secondary':
            bg = cls.get_color('secondary')
            fg = 'white'
            hover_bg = cls.lighten_color(bg, 0.1)
        elif variant == 'success':
            bg = cls.get_color('success')
            fg = 'white'
            hover_bg = cls.lighten_color(bg, 0.1)
        elif variant == 'danger':
            bg = cls.get_color('danger')
            fg = 'white'
            hover_bg = cls.lighten_color(bg, 0.1)
        elif variant == 'outline':
            bg = 'transparent'
            fg = cls.get_color('primary')
            hover_bg = cls.get_color('hover')
        else:
            bg = cls.get_color('surface')
            fg = cls.get_color('text_primary')
            hover_bg = cls.get_color('hover')
        
        return bg, fg, hover_bg
    
    @classmethod
    def apply_button_style(cls, widget, variant='primary', **kwargs):
        """Applique un style de bouton spécifique"""
        bg, fg, hover_bg = cls.get_button_colors(variant)
        
        # Configuration de base
        config = {
            'bg': bg,
            'fg': fg,
            'font': ('Segoe UI', 10),
            'relief': tk.FLAT,
            'borderwidth': 0,
            'padx': 20,
            'pady': 10,
            'cursor': 'hand2',
            'activebackground': hover_bg,
            'activeforeground': fg
        }
        
        # Si outline, ajouter une bordure
        if variant == 'outline':
            config.update({
                'borderwidth': 1,
                'relief': 'solid',
                'highlightbackground': cls.get_color('primary'),
                'highlightcolor': cls.get_color('primary'),
                'highlightthickness': 1
            })
        
        # Mettre à jour avec les kwargs fournis
        config.update(kwargs)
        
        widget.config(**config)
        return widget
    
    @classmethod
    def apply_style(cls, widget, component_type, style_variant='default', **kwargs):
        """Applique un style à un widget"""
        # Récupérer le style de base
        style_config = cls.COMPONENT_STYLES.get(component_type, {}).get(style_variant, {}).copy()
        
        # Appliquer les styles spéciaux
        special_styles = {}
        
        # Remplacer les variables de couleur
        for key, value in style_config.items():
            if isinstance(value, str) and value.startswith('{') and value.endswith('}'):
                color_name = value[1:-1]
                style_config[key] = cls.get_color(color_name)
        
        # Appliquer les styles Tkinter standards
        for key in ['font', 'bg', 'fg', 'borderwidth', 'relief', 'padx', 'pady', 
                   'cursor', 'activebackground', 'activeforeground', 'highlightthickness',
                   'insertbackground', 'selectbackground', 'selectforeground']:
            if key in style_config:
                widget.config(**{key: style_config[key]})
        
        # Appliquer les styles spéciaux (comme borderradius)
        if 'borderradius' in style_config:
            cls.apply_rounded_corners(widget, style_config['borderradius'])
        
        if style_config.get('shadow', False):
            cls.apply_shadow(widget)
        
        # Appliquer les styles supplémentaires
        if kwargs:
            widget.config(**kwargs)
        
        return widget
    
    @classmethod
    def apply_rounded_corners(cls, widget, radius=8):
        """Applique des coins arrondis à un widget (via Canvas)"""
        try:
            # Cette méthode nécessite de redessiner le widget dans un Canvas
            # Pour l'instant, on utilise une méthode simplifiée
            if hasattr(widget, 'config'):
                widget.config(highlightthickness=0)
        except:
            pass
    
    @classmethod
    def apply_shadow(cls, widget):
        """Applique une ombre à un widget"""
        # À implémenter avec un Canvas ou overlay
        pass
    
    @classmethod
    def create_gradient(cls, parent, color1, color2, direction='horizontal', **kwargs):
        """Crée un dégradé de couleur"""
        from tkinter import Canvas
        canvas = Canvas(parent, highlightthickness=0, **kwargs)
        
        def draw_gradient():
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            canvas.delete("all")
            
            if direction == 'horizontal':
                for i in range(width):
                    ratio = i / width
                    r = int(int(color1[1:3], 16) * (1 - ratio) + int(color2[1:3], 16) * ratio)
                    g = int(int(color1[3:5], 16) * (1 - ratio) + int(color2[3:5], 16) * ratio)
                    b = int(int(color1[5:7], 16) * (1 - ratio) + int(color2[5:7], 16) * ratio)
                    color = f'#{r:02x}{g:02x}{b:02x}'
                    canvas.create_line(i, 0, i, height, fill=color)
            else:  # vertical
                for i in range(height):
                    ratio = i / height
                    r = int(int(color1[1:3], 16) * (1 - ratio) + int(color2[1:3], 16) * ratio)
                    g = int(int(color1[3:5], 16) * (1 - ratio) + int(color2[3:5], 16) * ratio)
                    b = int(int(color1[5:7], 16) * (1 - ratio) + int(color2[5:7], 16) * ratio)
                    color = f'#{r:02x}{g:02x}{b:02x}'
                    canvas.create_line(0, i, width, i, fill=color)
        
        canvas.bind("<Configure>", lambda e: draw_gradient())
        return canvas
    
    @classmethod
    def create_neumorphic_effect(cls, parent, **kwargs):
        """Crée un effet néomorphique"""
        from tkinter import Frame
        
        frame = Frame(parent, **kwargs)
        frame.config(
            bg=cls.get_color('background'),
            highlightbackground=cls.get_color('hover'),
            highlightcolor=cls.get_color('hover'),
            highlightthickness=1,
            relief='flat'
        )
        return frame
    
    @classmethod
    def get_icon(cls, icon_name, size=24, color=None):
        """Récupère une icône (à implémenter avec FontAwesome)"""
        # Pour l'instant, on utilise des emojis
        icons = {
            'dashboard': '📊',
            'analysis': '🔍',
            'history': '📋',
            'settings': '⚙️',
            'spam': '🚨',
            'ham': '✅',
            'refresh': '🔄',
            'export': '📥',
            'trash': '🗑️',
            'save': '💾',
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'success': '✅',
            'add': '➕',
            'remove': '➖',
            'edit': '✏️',
            'search': '🔎',
            'filter': '🎛️',
            'stats': '📈',
            'user': '👤',
            'lock': '🔒',
            'unlock': '🔓',
            'download': '⬇️',
            'upload': '⬆️',
            'menu': '☰'
        }
        return icons.get(icon_name, '📋')
    
    @classmethod
    def animate_widget(cls, widget, property_name, start_value, end_value, duration=300):
        """Anime un widget (changement progressif d'une propriété)"""
        import time
        
        def animate(step, total_steps):
            if step <= total_steps:
                ratio = step / total_steps
                current_value = start_value + (end_value - start_value) * ratio
                
                if property_name == 'bg':
                    # Pour les couleurs, besoin d'interpolation
                    pass
                elif hasattr(widget, 'config'):
                    widget.config(**{property_name: current_value})
                
                widget.after(10, lambda: animate(step + 1, total_steps))
        
        total_steps = duration // 10
        animate(0, total_steps)