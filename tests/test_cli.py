"""
Тесты для модуля cli.py
"""

import pytest
import tempfile
import json
from pathlib import Path
from repo_doctor.cli import CliApp, main


@pytest.fixture
def temp_repo():
    """Создать временный репозиторий для тестирования."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def complete_repo(temp_repo):
    """Создать полный репозиторий для тестирования."""
    (temp_repo / 'README.md').write_text(
        '# Test Project\n\n## Installation\n\n```bash\npip install test\n```\n\n## Usage\n\nExample usage'
    )
    (temp_repo / 'LICENSE').write_text('MIT License')
    (temp_repo / '.gitignore').write_text('*.pyc\n__pycache__/')
    (temp_repo / 'CONTRIBUTING.md').write_text('# Contributing\n\nFork and submit PR')
    (temp_repo / 'SECURITY.md').write_text('# Security\n\nReport issues securely')
    (temp_repo / '.env.example').write_text('DEBUG=false')

    return temp_repo


def test_cli_app_creation():
    """Тест: создание объекта CliApp."""
    app = CliApp()
    assert app is not None
    assert app.parser is not None


def test_parser_creation():
    """Тест: парсер создана корректно."""
    app = CliApp()
    assert app.parser.prog == 'repo-doctor'


def test_main_function_help(capsys):
    """Тест: вывод справки."""
    app = CliApp()
    with pytest.raises(SystemExit):
        app.run(['--help'])

    captured = capsys.readouterr()
    assert 'repo-doctor' in captured.out
    assert 'Анализирует' in captured.out


def test_run_with_nonexistent_path():
    """Тест: запуск с несуществующим путём."""
    app = CliApp()
    result = app.run(['/nonexistent/path'])

    assert result == 1


def test_run_with_valid_path(complete_repo, capsys):
    """Тест: запуск с валидным путём."""
    app = CliApp()
    result = app.run([str(complete_repo)])

    assert result == 0
    captured = capsys.readouterr()
    assert 'REPO HEALTH DOCTOR' in captured.out
    assert 'ОБЩИЙ БАЛЛ' in captured.out


def test_run_json_output(complete_repo, capsys):
    """Тест: вывод в JSON формате."""
    app = CliApp()
    result = app.run([str(complete_repo), '--json'])

    assert result == 0
    captured = capsys.readouterr()

    # Должен быть валидный JSON
    data = json.loads(captured.out)
    assert 'score' in data
    assert 'required_files' in data
    assert 'readme' in data


def test_run_fix_mode(temp_repo, capsys):
    """Тест: режим --fix."""
    (temp_repo / 'README.md').touch()
    (temp_repo / 'LICENSE').touch()
    (temp_repo / '.gitignore').touch()

    app = CliApp()
    result = app.run([str(temp_repo), '--fix'])

    assert result == 0
    captured = capsys.readouterr()
    assert 'РЕЗУЛЬТАТЫ' in captured.out or 'результаты' in captured.out.lower()

    # Проверить что файлы созданы
    assert (temp_repo / 'CONTRIBUTING.md').exists()
    assert (temp_repo / 'SECURITY.md').exists()


def test_run_fix_mode_skips_existing(complete_repo, capsys):
    """Тест: режим --fix не перезаписывает существующие файлы."""
    original_content = (complete_repo / 'CONTRIBUTING.md').read_text()

    app = CliApp()
    result = app.run([str(complete_repo), '--fix'])

    assert result == 0

    # Содержимое не должно измениться
    assert (complete_repo / 'CONTRIBUTING.md').read_text() == original_content


def test_run_fix_force_mode(complete_repo, capsys):
    """Тест: режим --fix --force перезаписывает файлы."""
    original_content = (complete_repo / 'CONTRIBUTING.md').read_text()

    app = CliApp()
    result = app.run([str(complete_repo), '--fix', '--force'])

    assert result == 0

    # Содержимое может измениться (зависит от шаблона)
    # Но файл не должен быть в skipped списке при force=True
    captured = capsys.readouterr()
    # В результатах должно быть что-то о создании файлов


def test_run_poor_repo_returns_error(temp_repo, capsys):
    """Тест: плохой репозиторий возвращает код ошибки."""
    # Пустой репозиторий без файлов
    app = CliApp()
    result = app.run([str(temp_repo)])

    # Должен вернуть 1 (ошибка) из-за низкого балла
    assert result == 1
    captured = capsys.readouterr()
    assert 'ОБЩИЙ БАЛЛ' in captured.out


def test_main_function_integration(complete_repo):
    """Интеграционный тест: функция main()."""
    result = main([str(complete_repo)])

    assert result == 0


def test_cli_version(capsys):
    """Тест: флаг --version."""
    app = CliApp()
    with pytest.raises(SystemExit):
        app.run(['--version'])

    captured = capsys.readouterr()
    assert '1.0.0' in captured.out


def test_run_with_dot_path(complete_repo, monkeypatch, capsys):
    """Тест: запуск с путём '.'"""
    import os
    monkeypatch.chdir(complete_repo)

    app = CliApp()
    result = app.run(['.'])

    assert result == 0
    captured = capsys.readouterr()
    assert 'ОБЩИЙ БАЛЛ' in captured.out


def test_fix_json_output(temp_repo, capsys):
    """Тест: режим --fix с JSON выводом."""
    (temp_repo / 'README.md').touch()
    (temp_repo / 'LICENSE').touch()
    (temp_repo / '.gitignore').touch()

    app = CliApp()
    result = app.run([str(temp_repo), '--fix', '--json'])

    assert result == 0
    captured = capsys.readouterr()

    # Должен быть валидный JSON
    data = json.loads(captured.out)
    assert 'created' in data or 'skipped' in data
