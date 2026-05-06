"""
Repo Health Doctor - утилита для анализа здоровья Git-репозитория.

Позволяет оценить готовность репозитория к публикации,
выявить недостающие важные файлы и документацию.
"""

__version__ = '1.0.0'
__author__ = 'Repo Health Doctor Contributors'
__license__ = 'MIT'

from .checks import RepositoryChecker
from .scoring import HealthScorer
from .fixers import RepositoryFixer
from .report import ReportFormatter, FixerReportFormatter
from .cli import CliApp, main

__all__ = [
    'RepositoryChecker',
    'HealthScorer',
    'RepositoryFixer',
    'ReportFormatter',
    'FixerReportFormatter',
    'CliApp',
    'main',
]
