"""
Модуль для обработки командной строки.

Парсер аргументов и основная логика запуска приложения.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .checks import RepositoryChecker
from .scoring import HealthScorer
from .fixers import RepositoryFixer
from .report import ReportFormatter, FixerReportFormatter


class CliApp:
    """Главное приложение CLI."""

    def __init__(self):
        """Инициализация приложения."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Создать парсер аргументов командной строки.

        Returns:
            Объект ArgumentParser
        """
        parser = argparse.ArgumentParser(
            prog='repo-doctor',
            description='Анализирует здоровье локального Git-репозитория',
            epilog='Примеры:\n'
                   '  repo-doctor .                    # Проверить текущую папку\n'
                   '  repo-doctor /path/to/repo        # Проверить конкретную папку\n'
                   '  repo-doctor . --json              # Вывести результат в JSON\n'
                   '  repo-doctor . --fix               # Создать недостающие файлы\n'
                   '  repo-doctor . --fix --force       # Перезаписать существующие файлы\n',
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        parser.add_argument(
            'path',
            nargs='?',
            default='.',
            help='Путь к репозиторию (по умолчанию текущая папка)'
        )

        parser.add_argument(
            '--json',
            action='store_true',
            help='Вывести результат в JSON формате'
        )

        parser.add_argument(
            '--fix',
            action='store_true',
            help='Создать недостающие файлы (CONTRIBUTING.md, SECURITY.md и т.д.)'
        )

        parser.add_argument(
            '--force',
            action='store_true',
            help='При использовании с --fix перезаписать существующие файлы'
        )

        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s 1.0.0'
        )

        return parser

    def run(self, args: Optional[list] = None) -> int:
        """
        Запустить приложение.

        Args:
            args: Аргументы командной строки (для тестирования)

        Returns:
            Код выхода (0 = успех, 1 = ошибка)
        """
        try:
            parsed_args = self.parser.parse_args(args)

            # Проверить что путь существует
            repo_path = Path(parsed_args.path).resolve()
            if not repo_path.exists():
                print(f"❌ Ошибка: путь '{parsed_args.path}' не существует")
                return 1

            # Выполнить проверку репозитория
            checker = RepositoryChecker(repo_path)
            check_results = checker.check_all()

            # Рассчитать балл
            scorer = HealthScorer()
            score = scorer.calculate_score(check_results)

            # Если нужно создавать файлы
            if parsed_args.fix:
                return self._handle_fix(repo_path, parsed_args.force, parsed_args.json)

            # Вывести результаты
            return self._output_results(check_results, score, scorer, parsed_args.json)

        except KeyboardInterrupt:
            print("\n⏹️  Операция отменена пользователем")
            return 130
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {str(e)}")
            return 1

    def _output_results(
        self,
        check_results: dict,
        score: int,
        scorer: HealthScorer,
        use_json: bool = False
    ) -> int:
        """
        Вывести результаты проверки.

        Args:
            check_results: Результаты проверок
            score: Итоговый балл
            scorer: Объект для подсчёта балла
            use_json: Использовать JSON формат

        Returns:
            Код выхода
        """
        formatter = ReportFormatter(check_results, score)

        if use_json:
            print(formatter.format_json())
        else:
            print(formatter.format_text(scorer))

        # Если балл низкий, вернуть код ошибки
        if score < 50:
            return 1
        return 0

    def _handle_fix(self, repo_path: Path, force: bool, use_json: bool) -> int:
        """
        Обработать флаг --fix для создания файлов.

        Args:
            repo_path: Путь к репозиторию
            force: Перезаписать существующие файлы
            use_json: Использовать JSON формат

        Returns:
            Код выхода
        """
        fixer = RepositoryFixer(repo_path)
        fixer_results = fixer.create_missing_files(force=force)

        formatter = FixerReportFormatter(fixer_results)

        if use_json:
            print(formatter.format_json())
        else:
            print(formatter.format_text())

        return 0


def main(args: Optional[list] = None) -> int:
    """
    Точка входа приложения.

    Args:
        args: Аргументы командной строки

    Returns:
        Код выхода
    """
    app = CliApp()
    return app.run(args)
