"""
Точка входа для запуска как модуля: python -m repo_doctor
"""

import sys
from .cli import main

if __name__ == '__main__':
    sys.exit(main())
