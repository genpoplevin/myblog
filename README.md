# Myblog

## Описание
Myblog — это современный REST API для социальной сети, реализованный на Django REST Framework. Сервис позволяет пользователям создавать посты, комментировать, подписываться на других пользователей, просматривать группы и управлять доступом через JWT-аутентификацию. Проект построен с учетом лучших практик Python, DRF и безопасности.

---

## Технологии
- Python 3.10+
- Django 4.2+
- Django REST Framework 3.14+
- Simple JWT (аутентификация)
- djoser (регистрация и управление пользователями)
- PostgreSQL (опционально)
- Pytest (тестирование)
- Docker (опционально для контейнеризации)

---

## Функциональность
- JWT-аутентификация и регистрация пользователей
- CRUD для постов
- CRUD для комментариев к постам
- Подписки на пользователей
- Просмотр и фильтрация групп
- Ограничение доступа для неавторов
- Документация OpenAPI/Redoc
- Покрытие тестами бизнес-логики и API

---

## Структура проекта
```
api_final_yatube/
├── yatube_api/           # Основное Django-приложение
│   ├── api/             # API, сериализаторы, permissions, роуты
│   ├── posts/           # Модели, бизнес-логика
│   └── yatube_api/      # Настройки Django
├── tests/               # Тесты Pytest
├── requirements.txt     # Зависимости
├── .env.example         # Пример переменных окружения
├── Dockerfile           # (опционально) Docker-сборка
├── docker-compose.yml   # (опционально) Docker-оркестрация
├── README.md            # Документация
└── API.md               # Примеры запросов и ответы
```

---

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/AndreyZherdetskiy/api_final_yatube
cd api_final_yatube
```
2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Скопируйте пример переменных окружения и настройте свой `.env`:
```bash
cp .env.example .env
```
5. Примените миграции:
```bash
python manage.py migrate
```
6. Запустите сервер:
```bash
python manage.py runserver
```

---

## Переменные окружения
- Все переменные описаны в `.env.example`.
- Не храните секретные ключи в открытом доступе!

---

## Документация API
- Redoc: [`/redoc/`](http://localhost:8000/redoc/)
- Примеры запросов: [API.md](API.md)

---

## Тестирование

```bash
pytest
```
- Все тесты находятся в папке `tests/`
- Используется Pytest и pytest-django

---

## Архитектура
- Django-приложение `yatube_api` с модульной структурой
- Используется Django ORM и DRF ViewSets
- JWT-аутентификация через Simple JWT
- Документация через Redoc
- Константы и настройки вынесены в отдельные модули
- Оптимизированные запросы к БД (`select_related`, `prefetch_related`)
- Весь код снабжен type hints и докстрингами

---

## Контакты
- Автор: [Жердецкий Андрей](https://github.com/AndreyZherdetskiy/)

---

## Лицензия
MIT License
