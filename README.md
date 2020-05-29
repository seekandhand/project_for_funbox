Web-приложение для учета посещенных ссылок
===

### Инструкция по запуску

Перед началом работы необходимо:

1. Установить следующие
програмные пакеты:

    1. Интерпретатор python версии 3.7.6 - [python.org](http://python.org)
    2. Redis - [https://redis.io/](https://redis.io/)
    3. Git - [https://git-scm.com/book/ru/v2/Введение-Установка-Git](https://git-scm.com/book/ru/v2/Введение-Установка-Git)
    
2. Скачать git репозиторий на локальный ПК:
```bash
git clone https://github.com/seekandhand/project_for_funbox
```

3. Установить зависимости проекта (в созданной папке):
```bash
pip install -r requirements.txt
```

4. Запустить Django сервер:
```bash
python manage.py runserver
```

---

### Запуск тестов
```bash
pytest
```
