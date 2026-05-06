# Repo Health Doctor

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Консольная утилита для анализа здоровья локальных Git-репозиториев. Проверяет готовность проекта к публикации, наличие важной документации и базовую структуру.

## 📋 Возможности

✅ **Проверка обязательных файлов**: README.md, LICENSE, .gitignore
✅ **Анализ README**: структура, разделы, примеры кода  
✅ **Проверка документации**: CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md  
✅ **GitHub конфигурация**: workflows, issue/PR шаблоны  
✅ **Расчёт Repo Health Score** (0-100)  
✅ **Автоматическое исправление**: создание недостающих шаблонов файлов  
✅ **Красивый вывод**: форматированный текст или JSON  

## 🎯 Зачем нужно

Когда вы готовите проект к публикации на GitHub или хотите убедиться, что ваш репозиторий удобен для пользователей и контрибьюторов, нужно проверить много параметров:

- Есть ли хороший README с примерами?
- Есть ли файл лицензии?
- Понятно ли, как установить проект?
- Как контрибьюторам начать помогать?
- Защищена ли информация о безопасности?

**Repo Health Doctor** делает это за вас за одну команду!

## 🚀 Быстрый старт

### Установка

```bash
# Глобальная установка (рекомендуется)
pip install repo-doctor

# Или из исходников (для разработки)
git clone https://github.com/PASTREL1997/repo-health-doctor.git
cd repo-health-doctor
pip install -e .
```

### Основной запуск

```bash
# Проверить текущую папку
repo-doctor .

# Или используя Python модуль
python -m repo_doctor .

# Проверить конкретную папку
repo-doctor /path/to/your/repo
```

### Примеры запуска

**1. Базовая проверка с красивым отчётом:**
```bash
repo-doctor .
```

**Вывод:**
```
============================================================
📊 REPO HEALTH DOCTOR - ОТЧЁТ О ЗДОРОВЬЕ РЕПОЗИТОРИЯ
============================================================

🎯 ОБЩИЙ БАЛЛ: 🟡 78/100 (🟡 Хороший)

📁 ОБЯЗАТЕЛЬНЫЕ ФАЙЛЫ:
  ✅ README.md
  ✅ LICENSE
  ✅ .gitignore

📄 АНАЛИЗ README.MD:
  ✅ Файл существует (1245 символов)
  ✅ Есть заголовок
  ✅ Есть секция установки
  ✅ Есть секция использования
  ✅ Есть примеры кода

💡 РЕКОМЕНДУЕМЫЕ ФАЙЛЫ (найдено 1/4):
  ✅ CONTRIBUTING.md
  ❌ SECURITY.md
  ❌ CODE_OF_CONDUCT.md
  ❌ .env.example

⛔ ПРОБЛЕМЫ:
  ❌ Отсутствует Политика безопасности: SECURITY.md

💡 РЕКОМЕНДАЦИИ:
  💡 Рекомендуется добавить: Кодекс поведения (CODE_OF_CONDUCT.md)
  💡 Рекомендуется добавить: GitHub Actions workflows

============================================================
👍 Хорошее состояние. Рекомендуем улучшить документацию.
============================================================
```

**2. Вывод результата в JSON:**
```bash
repo-doctor . --json
```

**JSON вывод:**
```json
{
  "score": 78,
  "required_files": {
    "README.md": true,
    "LICENSE": true,
    ".gitignore": true
  },
  "readme": {
    "exists": true,
    "has_title": true,
    "has_installation": true,
    "has_usage": true,
    "has_examples": true,
    "length": 1245
  },
  "issues": [
    "❌ Отсутствует Политика безопасности: SECURITY.md"
  ],
  "suggestions": [
    "💡 Рекомендуется добавить: Кодекс поведения (CODE_OF_CONDUCT.md)"
  ]
}
```

**3. Автоматическое создание недостающих файлов:**
```bash
# Создать недостающие файлы (не перезаписывать существующие)
repo-doctor . --fix

# Результат:
# ✅ Создано 4 файлов:
#   ✓ CONTRIBUTING.md
#   ✓ SECURITY.md
#   ✓ CODE_OF_CONDUCT.md
#   ✓ .env.example
```

**4. Пересоздать файлы (с перезаписью):**
```bash
# ОСТОРОЖНО: перезаписывает созданные шаблоны
repo-doctor . --fix --force
```

## 📊 Что проверяется

### Обязательные файлы (30 баллов)
- ✅ README.md
- ✅ LICENSE
- ✅ .gitignore

### Качество README (25 баллов)
- ✅ Заголовок проекта
- ✅ Секция установки
- ✅ Секция использования
- ✅ Примеры кода
- ✅ Минимальный размер (100+ символов)

### Документация (20 баллов)
- ✅ CONTRIBUTING.md
- ✅ SECURITY.md
- ✅ CODE_OF_CONDUCT.md

### GitHub конфигурация (15 баллов)
- ✅ .github/workflows (CI/CD)
- ✅ .github/ISSUE_TEMPLATE
- ✅ .github/pull_request_template.md

### Безопасность (10 баллов)
- ✅ Отсутствие .env в репозитории
- ✅ .env.example для примера

**Итого: 100 баллов максимум**

## 🎨 Уровни здоровья

| Балл | Уровень | Статус |
|------|---------|--------|
| 90-100 | 🟢 Отличный | Проект готов к публикации |
| 75-89 | 🟡 Хороший | Небольшие улучшения рекомендуются |
| 50-74 | 🟠 Средний | Требуются улучшения |
| 25-49 | 🔴 Плохой | Серьёзные проблемы |
| 0-24 | 🔴 Критический | Требуется полная переработка |

## 🛠️ Команды и флаги

```bash
repo-doctor [PATH] [OPTIONS]

ARGUMENTS:
  PATH                  Путь к репозиторию (по умолчанию: .)

OPTIONS:
  --json                Вывести результат в JSON формате
  --fix                 Создать недостающие шаблоны файлов
  --force               С --fix: перезаписать существующие файлы
  --version             Показать версию
  --help                Показать справку
```

## 📝 Создаваемые файлы (--fix)

При использовании флага `--fix` утилита создаёт следующие файлы с шаблонами:

1. **CONTRIBUTING.md** - гайд для контрибьюторов
2. **SECURITY.md** - политика безопасности
3. **CODE_OF_CONDUCT.md** - кодекс поведения
4. **.env.example** - пример переменных окружения
5. **.github/ISSUE_TEMPLATE/bug_report.md** - шаблон для bug report
6. **.github/pull_request_template.md** - шаблон для PR

**Важно**: флаг `--fix` НЕ перезаписывает существующие файлы. Используйте `--force` для пересоздания.

## 🧪 Разработка и тестирование

### Установка зависимостей для разработки

```bash
pip install -e ".[dev]"
```

### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=repo_doctor tests/

# Конкретный тест
pytest tests/test_checks.py::test_check_required_files_all_exist -v
```

### Проверка кода

```bash
# Форматирование
black repo_doctor tests

# Linting
flake8 repo_doctor tests

# Type checking
mypy repo_doctor
```

## 📁 Структура проекта

```
repo_doctor/
├── __init__.py          # Инициализация пакета
├── __main__.py          # Точка входа для python -m repo_doctor
├── cli.py               # CLI парсер и главное приложение
├── checks.py            # Проверка файлов и структуры репозитория
├── scoring.py           # Расчёт Repo Health Score
├── fixers.py            # Создание недостающих файлов
└── report.py            # Форматирование отчётов (текст и JSON)

tests/
├── __init__.py
├── test_checks.py       # Тесты для checks.py
├── test_scoring.py      # Тесты для scoring.py
└── test_cli.py          # Тесты для cli.py

README.md                # Этот файл
pyproject.toml          # Конфигурация проекта
LICENSE                 # Лицензия MIT
.gitignore             # Git ignore файл
```

## 🔄 Roadmap (Планы на будущее)

- [ ] Поддержка конфигурационного файла (.repo-doctor.yml)
- [ ] Проверка качества кода (сложность, дублирование)
- [ ] Анализ истории коммитов (frequency, message quality)
- [ ] Интеграция с pre-commit hooks
- [ ] Web интерфейс для отчётов
- [ ] Поддержка других VCS (Mercurial, SVN)
- [ ] Плагины для специфичных фреймворков (Django, FastAPI, etc.)
- [ ] Автоматическое исправление общих проблем
- [ ] Экспорт отчётов в HTML/PDF
- [ ] Публикация пакета в PyPI

## 🤝 Как внести вклад

Мы приветствуем любые вклады! Вот как начать:

1. **Fork** репозиторий
2. Создайте **ветку** для вашей фишки (`git checkout -b feature/amazing-feature`)
3. **Коммитьте** ваши изменения (`git commit -m 'Add amazing feature'`)
4. **Push** в ветку (`git push origin feature/amazing-feature`)
5. Откройте **Pull Request**

### Требования для контрибьюторов

- Python 3.10+
- pytest для тестов
- Код должен соответствовать PEP 8
- Добавляйте docstrings для функций и классов
- Покрывайте новый код тестами

### Запуск тестов перед PR

```bash
pytest
black --check repo_doctor tests
flake8 repo_doctor tests
```

## 📄 Лицензия

Проект распространяется под лицензией MIT. Смотрите [LICENSE](LICENSE) для деталей.

## 👤 Автор

Создано для помощи разработчикам в подготовке проектов к публикации.

## 📞 Поддержка

Возникли вопросы или нашли баг?

- 📝 Создайте [issue на GitHub](https://github.com/yourusername/repo-health-doctor/issues)
- 💬 Обсудите в [discussions](https://github.com/yourusername/repo-health-doctor/discussions)
- 📧 Свяжитесь по email (добавьте в профиль)

## 🙏 Благодарности

- Вдохновлено лучшими практиками GitHub
- Спасибо всем контрибьюторам!

---

**Сделано с ❤️ для сообщества разработчиков**
