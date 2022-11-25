# Продуктовый помощник

Это сайт, на котором пользователи могут публиковать рецепты и сохранять рецепты
других пользователей в избранное. А также, пользователи могут подписываться на
публикации других пользователей.
Также есть дополнительный сервис «Список покупок», который формирует
продуктовую корзину выбранных рецептов пользователя, ее можно скачать в виде
файла и отправиться за покупками.

![Workflow](https://github.com/drode1/foodgram-project-react/blob/master/.github/workflows/main.yml/badge.svg)

### **Стек**

![python version](https://img.shields.io/badge/Python-3.7-green)
![django version](https://img.shields.io/badge/Django-2.2-green)
![djangorestframework version](https://img.shields.io/badge/DRF-3.12-green)
![djoser version](https://img.shields.io/badge/Djoser-2.1.0-green)
![docker version](https://img.shields.io/badge/Docker-3-green)

### Как запустить проект локально с помощью venv:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/drode1/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
. venv/bin/activate
```

```
python -m pip install --upgrade pip
```    

Установить зависимости из файла requirements.txt:

``` 
pip install -r backend/requirements.txt
```   

Выполнить миграции:

```
python backend/manage.py migrate
```       

Запустить проект:

```
python backend/manage.py runserver
```

### Как запустить скрипт через Docker:

1. В папке ```backend/``` создайте файл, по аналогии
   с ```.env.example``` и заполните ее данными;
2. Перейдите в папку ```infra/```.
3. Создайте образ докера и запустите контейнер в
   фоне ```docker-compose up -d --build```.

### Импорт тестовых данных (для Docker)

Для проверки работы проекта можно наполнить проект тестовыми данными, для этого
можно ввести команду, находясь в контейнере backend

```
python manage.py import
```

Данная команда импортирует данные по:

- ингредиентам;
- тегам;
- пользователям.

___

## Контакты

- [Егор Ремезов](https://github.com/drode1)
    - [Telegram](https://t.me/e_remezov)
    - [Mail](mailto:info@eremezov.com)

___