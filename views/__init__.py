# views/__init__.py
"""
Package des vues
"""
from .main_window import MainWindow
from .dashboard_tab import DashboardTab
from .analysis_tab import AnalysisTab
from .history_tab import HistoryTab
from .settings_tab import SettingsTab

__all__ = [
    'MainWindow',
    'DashboardTab',
    'AnalysisTab',
    'HistoryTab',
    'SettingsTab'
]