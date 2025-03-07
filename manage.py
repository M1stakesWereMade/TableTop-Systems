#!/usr/bin/env python
"""Точка входа для управления Django-проектом.

Используется для:
    - Запуска сервера разработки
    - Выполнения миграций
    - Работы с shell
    - И других административных задач

Использование:
    python manage.py [команда]
"""
import os
import sys

def main():
    """Запуск основных административных функций."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_management.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что он установлен и "
            "доступен в переменной окружения PYTHONPATH. Возможно, вы забыли "
            "активировать виртуальное окружение?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()