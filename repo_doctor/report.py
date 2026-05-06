"""
Модуль для форматирования и вывода отчётов.

Поддерживает красивый вывод в терминал и JSON формат.
"""

import json
from typing import Dict, Any


class ReportFormatter:
    """Класс для форматирования отчётов о здоровье репозитория."""

    def __init__(self, check_results: Dict, score: int):
        """
        Инициализация форматера отчёта.

        Args:
            check_results: Результаты проверок
            score: Общий балл здоровья
        """
        self.check_results = check_results
        self.score = score

    def format_text(self, scorer: Any = None) -> str:
        """
        Форматировать отчёт в красивый текстовый вид.

        Args:
            scorer: Объект HealthScorer для дополнительной информации

        Returns:
            Форматированная строка отчёта
        """
        lines = []

        # Заголовок
        lines.append("=" * 60)
        lines.append("📊 REPO HEALTH DOCTOR - ОТЧЁТ О ЗДОРОВЬЕ РЕПОЗИТОРИЯ")
        lines.append("=" * 60)
        lines.append("")

        # Общий балл
        score_level = scorer.get_score_level(self.score) if scorer else self._get_score_level()
        score_emoji = scorer.get_score_emoji(self.score) if scorer else self._get_score_emoji()

        lines.append(f"🎯 ОБЩИЙ БАЛЛ: {score_emoji} {self.score}/100 ({score_level})")
        lines.append("")

        # Проверка обязательных файлов
        lines.append("📁 ОБЯЗАТЕЛЬНЫЕ ФАЙЛЫ:")
        required = self.check_results.get('required_files', {})
        for file_name, exists in required.items():
            status = "✅" if exists else "❌"
            lines.append(f"  {status} {file_name}")
        lines.append("")

        # README анализ
        readme = self.check_results.get('readme', {})
        if readme.get('exists'):
            lines.append("📄 АНАЛИЗ README.MD:")
            lines.append(f"  ✅ Файл существует ({readme.get('length', 0)} символов)")
            if readme.get('has_title'):
                lines.append("  ✅ Есть заголовок")
            else:
                lines.append("  ❌ Нет заголовка")
            if readme.get('has_installation'):
                lines.append("  ✅ Есть секция установки")
            else:
                lines.append("  ❌ Нет секции установки")
            if readme.get('has_usage'):
                lines.append("  ✅ Есть секция использования")
            else:
                lines.append("  ❌ Нет секции использования")
            if readme.get('has_examples'):
                lines.append("  ✅ Есть примеры кода")
            else:
                lines.append("  ❌ Нет примеров кода")
            lines.append("")
        else:
            lines.append("📄 README.MD: ❌ Файл не найден")
            lines.append("")

        # Рекомендуемые файлы
        recommended = self.check_results.get('recommended_files', {})
        found_recommended = sum(1 for v in recommended.values() if v)
        if found_recommended > 0:
            lines.append(f"💡 РЕКОМЕНДУЕМЫЕ ФАЙЛЫ (найдено {found_recommended}/{len(recommended)}):")
            for file_name, exists in recommended.items():
                status = "✅" if exists else "❌"
                lines.append(f"  {status} {file_name}")
            lines.append("")

        # GitHub конфигурация
        github = self.check_results.get('github_files', {})
        found_github = sum(1 for v in github.values() if v)
        if found_github > 0:
            lines.append(f"🐙 GITHUB КОНФИГУРАЦИЯ (найдено {found_github}/{len(github)}):")
            for file_name, exists in github.items():
                status = "✅" if exists else "❌"
                lines.append(f"  {status} {file_name}")
            lines.append("")

        # Проблемы и предупреждения
        issues = self.check_results.get('issues', [])
        warnings = self.check_results.get('warnings', [])
        suggestions = self.check_results.get('suggestions', [])

        if issues:
            lines.append("⛔ ПРОБЛЕМЫ:")
            for issue in issues:
                lines.append(f"  {issue}")
            lines.append("")

        if warnings:
            lines.append("⚠️  ПРЕДУПРЕЖДЕНИЯ:")
            for warning in warnings:
                lines.append(f"  {warning}")
            lines.append("")

        if suggestions:
            lines.append("💡 РЕКОМЕНДАЦИИ:")
            for suggestion in suggestions:
                lines.append(f"  {suggestion}")
            lines.append("")

        # Итоговая сводка
        lines.append("-" * 60)
        summary_score = self.check_results.get('issues', [])
        if len(summary_score) == 0 and self.score >= 80:
            lines.append("✨ Отличная работа! Репозиторий находится в хорошем состоянии.")
        elif self.score >= 60:
            lines.append("👍 Хорошее состояние. Рекомендуем улучшить документацию.")
        else:
            lines.append("📝 Требуются улучшения. Начните с обязательных файлов.")

        lines.append("=" * 60)

        return "\n".join(lines)

    def format_json(self) -> str:
        """
        Форматировать отчёт в JSON.

        Returns:
            JSON строка с полными результатами
        """
        output = {
            'score': self.score,
            'required_files': self.check_results.get('required_files', {}),
            'recommended_files': self.check_results.get('recommended_files', {}),
            'github_files': self.check_results.get('github_files', {}),
            'project_files': self.check_results.get('project_files', {}),
            'env_files': self.check_results.get('env_files', {}),
            'readme': {
                k: v for k, v in self.check_results.get('readme', {}).items()
                if k != 'issues'
            },
            'readme_issues': self.check_results.get('readme', {}).get('issues', []),
            'issues': self.check_results.get('issues', []),
            'warnings': self.check_results.get('warnings', []),
            'suggestions': self.check_results.get('suggestions', []),
        }

        return json.dumps(output, ensure_ascii=False, indent=2)

    def _get_score_level(self) -> str:
        """Получить уровень здоровья по баллам (для совместимости)."""
        if self.score >= 90:
            return "🟢 Отличный"
        elif self.score >= 75:
            return "🟡 Хороший"
        elif self.score >= 50:
            return "🟠 Средний"
        elif self.score >= 25:
            return "🔴 Плохой"
        else:
            return "🔴 Критический"

    def _get_score_emoji(self) -> str:
        """Получить emoji для балла."""
        if self.score >= 90:
            return "🟢"
        elif self.score >= 75:
            return "🟡"
        elif self.score >= 50:
            return "🟠"
        else:
            return "🔴"


class FixerReportFormatter:
    """Класс для форматирования отчётов о создании файлов."""

    def __init__(self, fixer_results: Dict):
        """
        Инициализация форматера.

        Args:
            fixer_results: Результаты работы RepositoryFixer
        """
        self.fixer_results = fixer_results

    def format_text(self) -> str:
        """Форматировать отчёт о созданных файлах."""
        lines = []
        created = self.fixer_results.get('created', [])
        skipped = self.fixer_results.get('skipped', [])

        lines.append("")
        lines.append("=" * 60)
        lines.append("✨ РЕЗУЛЬТАТЫ СОЗДАНИЯ ФАЙЛОВ")
        lines.append("=" * 60)

        if created:
            lines.append(f"\n✅ Создано {len(created)} файлов:")
            for file_path in created:
                lines.append(f"  ✓ {file_path}")

        if skipped:
            lines.append(f"\n⏭️  Пропущено {len(skipped)} файлов:")
            for file_path in skipped:
                lines.append(f"  ✗ {file_path}")

        lines.append("\n" + "=" * 60)

        return "\n".join(lines)

    def format_json(self) -> str:
        """Форматировать отчёт в JSON."""
        return json.dumps(self.fixer_results, ensure_ascii=False, indent=2)
