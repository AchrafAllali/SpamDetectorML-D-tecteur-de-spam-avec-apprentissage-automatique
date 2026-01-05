# config/__init__.py
"""
Package de configuration
"""
from .settings import *

__all__ = [
    'MODEL_CONFIG',
    'DATABASE_CONFIG',
    'LOGGING_CONFIG',
    'UI_CONFIG',
    'SECURITY_CONFIG',
    'APP_INFO',
    'get_colors',
    'get_translation'
]