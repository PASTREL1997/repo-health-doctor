"""
Модуль для расчёта Repo Health Score.

Базируется на результатах проверок и присваивает балл от 0 до 100.
"""

from typing import Dict


class HealthScorer:
    """Класс для расчёта здоровья репозитория."""

    # Весовые коэффициенты для различных критериев
    WEIGHTS = {
        'required_files': 30,  # 30 баллов за обязательные файлы
        'readme_quality': 25,  # 25 баллов за качество README
        'documentation': 20,   # 20 баллов за документацию
        'github_setup': 15,    # 15 баллов за GitHub конфиг
        'security': 10,        # 10 баллов за безопасность
    }

    def __init__(self):
        """Инициализация скорера."""
        self.total_weight = sum(self.WEIGHTS.values())

    def calculate_score(self, check_results: Dict) -> int:
        """
        Рассчитать общий балл здоровья репозитория.

        Args:
            check_results: Результаты проверок от RepositoryChecker

        Returns:
            Балл от 0 до 100
        """
        score = 0

        # 1. Обязательные файлы (30 баллов)
        required_score = self._score_required_files(check_results)
        score += required_score

        # 2. Качество README (25 баллов)
        readme_score = self._score_readme(check_results)
        score += readme_score

        # 3. Документация (20 баллов)
        doc_score = self._score_documentation(check_results)
        score += doc_score

        # 4. GitHub конфигурация (15 баллов)
        github_score = self._score_github_setup(check_results)
        score += github_score

        # 5. Безопасность (10 баллов)
        security_score = self._score_security(check_results)
        score += security_score

        # Убедимся, что балл в пределах 0-100
        return min(max(score, 0), 100)

    def _score_required_files(self, check_results: Dict) -> int:
        """Подсчитать баллы за обязательные файлы."""
        required = check_results.get('required_files', {})
        found = sum(1 for v in required.values() if v)
        total = len(required)

        if total == 0:
            return 0

        # Все файлы найдены = 30 баллов
        # За каждый файл = 10 баллов
        percentage = found / total
        return int(self.WEIGHTS['required_files'] * percentage)

    def _score_readme(self, check_results: Dict) -> int:
        """Подсчитать баллы за качество README."""
        readme = check_results.get('readme', {})

        # README не существует = 0 баллов
        if not readme.get('exists'):
            return 0

        # Подсчитываем критерии
        criteria_met = 0
        max_criteria = 5

        if readme.get('has_title'):
            criteria_met += 1
        if readme.get('has_installation'):
            criteria_met += 1
        if readme.get('has_usage'):
            criteria_met += 1
        if readme.get('has_examples'):
            criteria_met += 1
        if readme.get('length', 0) >= 100:
            criteria_met += 1

        # За каждый критерий 5 баллов
        return int(self.WEIGHTS['readme_quality'] * (criteria_met / max_criteria))

    def _score_documentation(self, check_results: Dict) -> int:
        """Подсчитать баллы за документацию."""
        recommended = check_results.get('recommended_files', {})

        # CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md
        doc_files = ['CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'SECURITY.md']
        found = sum(1 for f in doc_files if recommended.get(f))

        # За каждый файл документации 6-7 баллов
        return int(self.WEIGHTS['documentation'] * (found / len(doc_files)))

    def _score_github_setup(self, check_results: Dict) -> int:
        """Подсчитать баллы за GitHub конфигурацию."""
        github = check_results.get('github_files', {})

        github_items = list(github.values())
        if not github_items:
            return 0

        found = sum(1 for v in github_items if v)
        return int(self.WEIGHTS['github_setup'] * (found / len(github_items)))

    def _score_security(self, check_results: Dict) -> int:
        """Подсчитать баллы за безопасность."""
        env = check_results.get('env_files', {})
        warnings = check_results.get('warnings', [])

        # .env файл в репозитории - штраф
        if env.get('.env'):
            return 0

        # Если есть другие проблемы безопасности
        security_warnings = [w for w in warnings if 'sec' in w.lower()]

        if security_warnings:
            return int(self.WEIGHTS['security'] * 0.5)

        # Всё хорошо
        return self.WEIGHTS['security']

    def get_score_level(self, score: int) -> str:
        """
        Получить уровень здоровья по баллам.

        Args:
            score: Балл от 0 до 100

        Returns:
            Текстовое описание уровня
        """
        if score >= 90:
            return "🟢 Отличный"
        elif score >= 75:
            return "🟡 Хороший"
        elif score >= 50:
            return "🟠 Средний"
        elif score >= 25:
            return "🔴 Плохой"
        else:
            return "🔴 Критический"

    def get_score_emoji(self, score: int) -> str:
        """Получить emoji для балла."""
        if score >= 90:
            return "🟢"
        elif score >= 75:
            return "🟡"
        elif score >= 50:
            return "🟠"
        else:
            return "🔴"
