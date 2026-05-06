"""
Тесты для модуля scoring.py
"""

import pytest
from repo_doctor.scoring import HealthScorer


@pytest.fixture
def scorer():
    """Создать объект HealthScorer для тестирования."""
    return HealthScorer()


@pytest.fixture
def basic_check_results():
    """Базовые результаты проверок."""
    return {
        'required_files': {
            'README.md': True,
            'LICENSE': True,
            '.gitignore': True,
        },
        'recommended_files': {
            'CONTRIBUTING.md': True,
            'SECURITY.md': False,
            'CODE_OF_CONDUCT.md': False,
            '.env.example': False,
        },
        'github_files': {
            '.github/workflows': False,
            '.github/ISSUE_TEMPLATE': False,
            '.github/pull_request_template.md': False,
        },
        'project_files': {},
        'env_files': {'.env': False},
        'readme': {
            'exists': True,
            'has_title': True,
            'has_installation': True,
            'has_usage': True,
            'has_examples': True,
            'length': 500,
            'issues': [],
        },
        'issues': [],
        'warnings': [],
        'suggestions': [],
    }


def test_calculate_score_perfect(scorer, basic_check_results):
    """Тест: идеальный репозиторий."""
    # Добавить все рекомендуемые файлы
    basic_check_results['recommended_files'] = {
        'CONTRIBUTING.md': True,
        'SECURITY.md': True,
        'CODE_OF_CONDUCT.md': True,
        '.env.example': True,
    }
    # Добавить GitHub файлы
    basic_check_results['github_files'] = {
        '.github/workflows': True,
        '.github/ISSUE_TEMPLATE': True,
        '.github/pull_request_template.md': True,
    }

    score = scorer.calculate_score(basic_check_results)

    assert score == 100


def test_calculate_score_minimal(scorer):
    """Тест: минимальный репозиторий (только обязательные файлы)."""
    results = {
        'required_files': {
            'README.md': True,
            'LICENSE': True,
            '.gitignore': True,
        },
        'recommended_files': {
            'CONTRIBUTING.md': False,
            'SECURITY.md': False,
            'CODE_OF_CONDUCT.md': False,
            '.env.example': False,
        },
        'github_files': {
            '.github/workflows': False,
            '.github/ISSUE_TEMPLATE': False,
            '.github/pull_request_template.md': False,
        },
        'project_files': {},
        'env_files': {'.env': False},
        'readme': {
            'exists': True,
            'has_title': True,
            'has_installation': False,
            'has_usage': False,
            'has_examples': False,
            'length': 50,
        },
        'issues': [],
        'warnings': [],
        'suggestions': [],
    }

    score = scorer.calculate_score(results)

    # Должен быть < 50, потому что README неполный и нет документации
    assert score < 50


def test_calculate_score_no_readme(scorer):
    """Тест: репозиторий без README."""
    results = {
        'required_files': {
            'README.md': False,
            'LICENSE': True,
            '.gitignore': True,
        },
        'recommended_files': {
            'CONTRIBUTING.md': False,
            'SECURITY.md': False,
            'CODE_OF_CONDUCT.md': False,
            '.env.example': False,
        },
        'github_files': {
            '.github/workflows': False,
            '.github/ISSUE_TEMPLATE': False,
            '.github/pull_request_template.md': False,
        },
        'project_files': {},
        'env_files': {'.env': False},
        'readme': {
            'exists': False,
        },
        'issues': [],
        'warnings': [],
        'suggestions': [],
    }

    score = scorer.calculate_score(results)

    assert score < 70


def test_calculate_score_with_env_file(scorer):
    """Тест: репозиторий с небезопасным .env файлом."""
    results = {
        'required_files': {
            'README.md': True,
            'LICENSE': True,
            '.gitignore': True,
        },
        'recommended_files': {
            'CONTRIBUTING.md': True,
            'SECURITY.md': True,
            'CODE_OF_CONDUCT.md': True,
            '.env.example': True,
        },
        'github_files': {
            '.github/workflows': True,
            '.github/ISSUE_TEMPLATE': True,
            '.github/pull_request_template.md': True,
        },
        'project_files': {},
        'env_files': {'.env': True},  # Опасно!
        'readme': {
            'exists': True,
            'has_title': True,
            'has_installation': True,
            'has_usage': True,
            'has_examples': True,
            'length': 500,
        },
        'issues': [],
        'warnings': ['Found .env file'],
        'suggestions': [],
    }

    score = scorer.calculate_score(results)

    # Даже при остальном идеальном состоянии, .env file должен снизить балл
    assert score < 100


def test_score_level_excellent(scorer):
    """Тест: уровень "Отличный"."""
    level = scorer.get_score_level(95)
    assert "Отличный" in level


def test_score_level_good(scorer):
    """Тест: уровень "Хороший"."""
    level = scorer.get_score_level(80)
    assert "Хороший" in level


def test_score_level_medium(scorer):
    """Тест: уровень "Средний"."""
    level = scorer.get_score_level(60)
    assert "Средний" in level


def test_score_level_poor(scorer):
    """Тест: уровень "Плохой"."""
    level = scorer.get_score_level(30)
    assert "Плохой" in level


def test_score_level_critical(scorer):
    """Тест: уровень "Критический"."""
    level = scorer.get_score_level(10)
    assert "Критический" in level


def test_score_emoji(scorer):
    """Тест: получение emoji для баллов."""
    assert scorer.get_score_emoji(95) == "🟢"
    assert scorer.get_score_emoji(80) == "🟡"
    assert scorer.get_score_emoji(60) == "🟠"
    assert scorer.get_score_emoji(30) == "🔴"


def test_score_bounds(scorer, basic_check_results):
    """Тест: балл не выходит за границы 0-100."""
    # Даже с некорректными данными, балл должен быть 0-100
    score = scorer.calculate_score(basic_check_results)

    assert score >= 0
    assert score <= 100
