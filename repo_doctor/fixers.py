"""
Модуль для автоматического создания недостающих файлов репозитория.

Содержит шаблоны для CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md и т.д.
"""

import os
from pathlib import Path
from typing import Dict, List


class RepositoryFixer:
    """Класс для создания недостающих файлов в репозитории."""

    TEMPLATES = {
        'CONTRIBUTING.md': '''# Contributing

Спасибо за интерес к проекту! Мы приветствуем любые вклады.

## Как начать

1. Fork проект
2. Создайте ветку для вашей фишки (`git checkout -b feature/amazing-feature`)
3. Сделайте коммиты (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## Требования

- Python 3.10+
- pytest для тестов
- Код должен соответствовать PEP 8

## Запуск тестов

```bash
pytest
```

## Кодовый стиль

Пожалуйста, следуйте PEP 8 и добавляйте docstrings для функций и классов.

## Вопросы?

Не стесняйтесь открывать issue!
''',

        'SECURITY.md': '''# Security Policy

## Сообщение об уязвимостях

Если вы обнаружили уязвимость безопасности, пожалуйста, НЕ открывайте публичный issue.

Вместо этого отправьте детали на:
- Создайте приватный security advisory через GitHub
- Или свяжитесь с maintainers напрямую

Пожалуйста, дайте нам разумное время для исправления уязвимости перед публичным раскрытием.

## Поддерживаемые версии

| Version | Статус          |
|---------|-----------------|
| 1.x     | Поддерживается  |
| < 1.0   | Не поддерживается |

## Безопасность зависимостей

Мы регулярно обновляем зависимости и проверяем на известные уязвимости.
''',

        'CODE_OF_CONDUCT.md': '''# Code of Conduct

## Наши обещания

В интересах содействия открытой и гостеприимной среде мы, как участники и мейнтейнеры, обязуемся участие в нашем проекте и нашем сообществе свободной от домогательств опытом для всех, независимо от возраста, размера, инвалидности, этнической принадлежности, гендерной идентичности и выражения, уровня опыта, национальности, внешнего вида, расы, религии или сексуальной идентичности и ориентации.

## Наши стандарты

Примеры поведения, которые способствуют созданию позитивной среды, включают:

- Использование приветливого и инклюзивного языка
- Уважительное отношение к различным точкам зрения и опыту
- Принятие критики конструктивно
- Сосредоточение внимания на том, что лучше для сообщества
- Проявление сочувствия к другим членам сообщества

Примеры неприемлемого поведения участников включают:

- Использование сексуализированного языка или образов
- Персональные атаки
- Троллинг или оскорбительные/уничижительные комментарии
- Домогательства, публичные или приватные
- Публикация приватной информации других

## Применение

Случаи оскорбительного, преследующего или неприемлемого поведения могут быть сообщены путем связи с мейнтейнерами. Все жалобы будут рассмотрены и проанализированы.

## Attribution

Этот Code of Conduct адаптирован из [Contributor Covenant](https://www.contributor-covenant.org/)
''',

        '.env.example': '''# Пример файла окружения
# Скопируйте этот файл в .env и заполните реальными значениями
# НИКОГДА не коммитьте .env файл с реальными секретами!

# DEBUG режим
DEBUG=false

# Другие переменные окружения
# API_KEY=your_api_key_here
# DATABASE_URL=postgresql://user:password@localhost/dbname
''',

        '.github/ISSUE_TEMPLATE/bug_report.md': '''---
name: Bug report
about: Сообщить об ошибке
title: '[BUG] '
labels: 'bug'
assignees: ''

---

## Описание ошибки
Четкое и краткое описание проблемы.

## Как воспроизвести
Шаги для воспроизведения:
1. Шаг 1
2. Шаг 2
3. ...

## Ожидаемое поведение
Что должно было произойти

## Фактическое поведение
Что произошло вместо этого

## Окружение
- ОС: [например, Windows 10]
- Версия Python: [например, 3.10]
- Версия проекта: [например, 1.0.0]

## Дополнительный контекст
Любая другая релевантная информация
''',

        '.github/pull_request_template.md': '''## Описание
Кратко опишите ваши изменения

## Тип изменения
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Связанные issues
Закрывает #(issue number)

## Как это было протестировано
Опишите тесты, которые вы запустили

## Чек-лист
- [ ] Код следует стилю проекта
- [ ] Я обновил документацию
- [ ] Я добавил тесты
- [ ] Все новые и существующие тесты прошли успешно
- [ ] Я обновил CHANGELOG
''',
    }

    def __init__(self, repo_path: str):
        """
        Инициализация фиксера.

        Args:
            repo_path: Путь к репозиторию
        """
        self.repo_path = Path(repo_path).resolve()
        self.created_files: List[str] = []
        self.skipped_files: List[str] = []

    def create_missing_files(self, force: bool = False) -> Dict[str, List[str]]:
        """
        Создать недостающие файлы.

        Args:
            force: Перезаписать существующие файлы

        Returns:
            Словарь с созданными и пропущенными файлами
        """
        for file_path, content in self.TEMPLATES.items():
            self._create_file(file_path, content, force)

        return {
            'created': self.created_files,
            'skipped': self.skipped_files,
        }

    def _create_file(self, relative_path: str, content: str, force: bool = False) -> bool:
        """
        Создать отдельный файл.

        Args:
            relative_path: Относительный путь файла
            content: Содержимое файла
            force: Перезаписать существующий файл

        Returns:
            True если файл был создан, False если пропущен
        """
        full_path = self.repo_path / relative_path

        # Создать директории если их нет
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Если файл уже существует и force=False
        if full_path.exists() and not force:
            self.skipped_files.append(relative_path)
            return False

        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.created_files.append(relative_path)
            return True
        except Exception as e:
            self.skipped_files.append(f"{relative_path} (ошибка: {str(e)})")
            return False

    def get_summary(self) -> Dict:
        """Получить краткую сводку по созданным файлам."""
        return {
            'created_count': len(self.created_files),
            'skipped_count': len(self.skipped_files),
            'created': self.created_files,
            'skipped': self.skipped_files,
        }
