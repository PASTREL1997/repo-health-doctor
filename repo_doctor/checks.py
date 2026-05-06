"""
Модуль для проверки здоровья репозитория.

Содержит функции для проверки наличия важных файлов,
директорий и анализа содержимого README.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple


class RepositoryChecker:
    """Класс для проверки структуры и файлов репозитория."""

    # Обязательные файлы
    REQUIRED_FILES = {
        'README.md': 'README файл с описанием проекта',
        'LICENSE': 'Файл лицензии',
        '.gitignore': 'Git ignore файл',
    }

    # Рекомендуемые файлы
    RECOMMENDED_FILES = {
        'CONTRIBUTING.md': 'Гайд для контрибьюторов',
        'SECURITY.md': 'Политика безопасности',
        'CODE_OF_CONDUCT.md': 'Кодекс поведения',
        '.env.example': 'Пример файла окружения',
    }

    # Важные директории и файлы
    GITHUB_FILES = {
        '.github/workflows': 'GitHub Actions workflows',
        '.github/ISSUE_TEMPLATE': 'Шаблоны для issues',
        '.github/pull_request_template.md': 'Шаблон для pull requests',
    }

    # Файлы конфигурации проектов
    PROJECT_FILES = {
        'pyproject.toml': 'Python проект (Poetry/Setuptools)',
        'package.json': 'Node.js проект',
        'requirements.txt': 'Python зависимости',
        'Cargo.toml': 'Rust проект',
        'go.mod': 'Go проект',
    }

    def __init__(self, repo_path: str):
        """
        Инициализация проверки репозитория.

        Args:
            repo_path: Путь к репозиторию для проверки
        """
        self.repo_path = Path(repo_path).resolve()
        self.issues: List[str] = []
        self.warnings: List[str] = []
        self.suggestions: List[str] = []
        self.found_files: Dict[str, bool] = {}

    def check_all(self) -> Dict:
        """
        Выполнить все проверки репозитория.

        Returns:
            Словарь с результатами проверок
        """
        return {
            'required_files': self.check_required_files(),
            'recommended_files': self.check_recommended_files(),
            'github_files': self.check_github_files(),
            'project_files': self.check_project_files(),
            'env_files': self.check_env_files(),
            'readme': self.analyze_readme(),
            'issues': self.issues,
            'warnings': self.warnings,
            'suggestions': self.suggestions,
        }

    def check_required_files(self) -> Dict[str, bool]:
        """Проверить обязательные файлы."""
        result = {}
        for file_name, description in self.REQUIRED_FILES.items():
            file_path = self.repo_path / file_name
            exists = file_path.exists()
            result[file_name] = exists
            self.found_files[file_name] = exists

            if not exists:
                self.issues.append(f"❌ Отсутствует {description}: {file_name}")

        return result

    def check_recommended_files(self) -> Dict[str, bool]:
        """Проверить рекомендуемые файлы."""
        result = {}
        for file_name, description in self.RECOMMENDED_FILES.items():
            file_path = self.repo_path / file_name
            exists = file_path.exists()
            result[file_name] = exists
            self.found_files[file_name] = exists

            if not exists:
                self.suggestions.append(f"💡 Рекомендуется добавить: {description} ({file_name})")

        return result

    def check_github_files(self) -> Dict[str, bool]:
        """Проверить GitHub файлы и директории."""
        result = {}
        for file_name, description in self.GITHUB_FILES.items():
            file_path = self.repo_path / file_name
            exists = file_path.exists() and (file_path.is_dir() or file_path.is_file())
            result[file_name] = exists
            self.found_files[file_name] = exists

            if not exists:
                self.suggestions.append(f"💡 Рекомендуется добавить: {description}")

        return result

    def check_project_files(self) -> Dict[str, bool]:
        """Проверить файлы конфигурации проектов."""
        result = {}
        found_project_files = []

        for file_name, description in self.PROJECT_FILES.items():
            file_path = self.repo_path / file_name
            exists = file_path.exists()
            result[file_name] = exists

            if exists:
                found_project_files.append(description)

        if found_project_files:
            self.suggestions.append(f"✓ Обнаружен проект: {', '.join(found_project_files)}")

        return result

    def check_env_files(self) -> Dict[str, bool]:
        """Проверить наличие небезопасных файлов окружения."""
        result = {'.env': False}
        env_path = self.repo_path / '.env'

        if env_path.exists():
            result['.env'] = True
            self.warnings.append(
                "⚠️  Найден файл .env! Убедитесь, что он добавлен в .gitignore. "
                "Никогда не коммитьте секреты!"
            )

        return result

    def analyze_readme(self) -> Dict:
        """
        Проанализировать файл README.md.

        Returns:
            Словарь с результатами анализа README
        """
        result = {
            'exists': False,
            'has_title': False,
            'has_installation': False,
            'has_usage': False,
            'has_examples': False,
            'length': 0,
            'issues': [],
        }

        readme_path = self.repo_path / 'README.md'
        if not readme_path.exists():
            return result

        result['exists'] = True

        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                result['length'] = len(content)

            # Проверки содержимого README
            content_lower = content.lower()

            # Заголовок (# или # Project Name и т.д.)
            if content.startswith('#'):
                result['has_title'] = True
            else:
                result['issues'].append("README должен начинаться с заголовка (#)")

            # Секция установки
            if any(
                keyword in content_lower
                for keyword in ['## install', '## setup', '## требования', '## installation']
            ):
                result['has_installation'] = True
            else:
                result['issues'].append("README должен содержать секцию установки")

            # Секция использования
            if any(
                keyword in content_lower
                for keyword in ['## usage', '## использование', '## примеры', '## example']
            ):
                result['has_usage'] = True
            else:
                result['issues'].append("README должен содержать секцию использования")

            # Примеры команд
            if '```' in content or '`' in content:
                result['has_examples'] = True
            else:
                result['issues'].append("README должен содержать примеры кода")

            # Проверка длины
            if result['length'] < 100:
                result['issues'].append("README слишком короткий (менее 100 символов)")

        except Exception as e:
            result['issues'].append(f"Ошибка при чтении README: {str(e)}")

        return result

    def get_missing_files(self) -> List[str]:
        """Получить список недостающих рекомендуемых файлов."""
        missing = []
        for file_name in self.RECOMMENDED_FILES:
            if not self.found_files.get(file_name, False):
                missing.append(file_name)
        return missing

    def get_summary(self) -> Dict:
        """Получить краткую сводку проверок."""
        return {
            'issues_count': len(self.issues),
            'warnings_count': len(self.warnings),
            'suggestions_count': len(self.suggestions),
            'total_problems': len(self.issues) + len(self.warnings),
        }
