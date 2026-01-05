# services/__init__.py
"""
Package des services
"""
from .prediction_service import PredictionService
from .statistics_service import StatisticsService

__all__ = ['PredictionService', 'StatisticsService']