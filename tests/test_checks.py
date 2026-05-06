"""
Тесты для модуля checks.py
"""

import pytest
import tempfile
from pathlib import Path
from repo_doctor.checks import RepositoryChecker


@pytest.fixture
def temp_repo():
    """Создать временный репозиторий для тестирования."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_check_required_files_all_exist(temp_repo):
    """Тест: все обязательные файлы найдены."""
    # Создать обязательные файлы
    (temp_repo / 'README.md').touch()
    (temp_repo / 'LICENSE').touch()
    (temp_repo / '.gitignore').touch()

    checker = RepositoryChecker(temp_repo)
    required = checker.check_required_files()

    assert required['README.md'] is True
    assert required['LICENSE'] is True
    assert required['.gitignore'] is True


def test_check_required_files_missing(temp_repo):
    """Тест: обязательные файлы отсутствуют."""
    checker = RepositoryChecker(temp_repo)
    required = checker.check_required_files()

    assert required['README.md'] is False
    assert required['LICENSE'] is False
    assert required['.gitignore'] is False
    assert len(checker.issues) == 3


def test_check_recommended_files(temp_repo):
    """Тест: проверка рекомендуемых файлов."""
    (temp_repo / 'CONTRIBUTING.md').touch()

    checker = RepositoryChecker(temp_repo)
    recommended = checker.check_recommended_files()

    assert recommended['CONTRIBUTING.md'] is True
    assert recommended['SECURITY.md'] is False
    assert recommended['CODE_OF_CONDUCT.md'] is False


def test_check_env_files(temp_repo):
    """Тест: проверка на наличие .env файла."""
    checker = RepositoryChecker(temp_repo)
    env = checker.check_env_files()

    assert env['.env'] is False
    assert len(checker.warnings) == 0

    # Создать .env файл
    (temp_repo / '.env').touch()
    checker2 = RepositoryChecker(temp_repo)
    env2 = checker2.check_env_files()

    assert env2['.env'] is True
    assert len(checker2.warnings) > 0


def test_analyze_readme_complete(temp_repo):
    """Тест: анализ хорошего README."""
    readme_content = '''# My Project

## Installation

```bash
pip install my-project
```

## Usage

```bash
my-project --help
```

This is a complete README with all sections.
'''
    (temp_repo / 'README.md').write_text(readme_content, encoding='utf-8')

    checker = RepositoryChecker(temp_repo)
    readme = checker.analyze_readme()

    assert readme['exists'] is True
    assert readme['has_title'] is True
    assert readme['has_installation'] is True
    assert readme['has_usage'] is True
    assert readme['has_examples'] is True
    assert readme['length'] > 100


def test_analyze_readme_missing(temp_repo):
    """Тест: анализ отсутствующего README."""
    checker = RepositoryChecker(temp_repo)
    readme = checker.analyze_readme()

    assert readme['exists'] is False


def test_analyze_readme_incomplete(temp_repo):
    """Тест: анализ неполного README."""
    readme_content = '# Short'
    (temp_repo / 'README.md').write_text(readme_content, encoding='utf-8')

    checker = RepositoryChecker(temp_repo)
    readme = checker.analyze_readme()

    assert readme['exists'] is True
    assert readme['has_title'] is True
    assert readme['has_installation'] is False
    assert readme['has_usage'] is False
    assert readme['has_examples'] is False
    assert len(readme['issues']) > 0


def test_github_files_check(temp_repo):
    """Тест: проверка GitHub файлов."""
    # Создать GitHub директории
    github_dir = temp_repo / '.github'
    github_dir.mkdir()
    (github_dir / 'workflows').mkdir()

    checker = RepositoryChecker(temp_repo)
    github = checker.check_github_files()

    assert github['.github/workflows'] is True
    assert github['.github/ISSUE_TEMPLATE'] is False


def test_check_all_integration(temp_repo):
    """Интеграционный тест: полная проверка."""
    # Создать обязательные файлы
    (temp_repo / 'README.md').write_text('# Test\n\n## Installation\n\n## Usage\n```bash\ntest\n```\n')
    (temp_repo / 'LICENSE').touch()
    (temp_repo / '.gitignore').touch()

    checker = RepositoryChecker(temp_repo)
    results = checker.check_all()

    assert results['required_files']['README.md'] is True
    assert results['readme']['exists'] is True
    assert len(results['issues']) == 0
    assert len(results['suggestions']) > 0


def test_get_missing_files(temp_repo):
    """Тест: получение списка недостающих файлов."""
    (temp_repo / 'CONTRIBUTING.md').touch()

    checker = RepositoryChecker(temp_repo)
    checker.check_recommended_files()

    missing = checker.get_missing_files()

    assert 'CONTRIBUTING.md' not in missing
    assert 'SECURITY.md' in missing
    assert 'CODE_OF_CONDUCT.md' in missing


def test_get_summary(temp_repo):
    """Тест: получение сводки."""
    checker = RepositoryChecker(temp_repo)
    checker.check_all()

    summary = checker.get_summary()

    assert 'issues_count' in summary
    assert 'warnings_count' in summary
    assert 'suggestions_count' in summary
    assert summary['issues_count'] >= 0
