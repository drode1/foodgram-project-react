# Продуктовый помощник

Это сайт, на котором пользователи могут публиковать рецепты и сохранять рецепты
других пользователей в избранное. А также, пользователи могут подписываться на
публикации других пользователей.
Также есть дополнительный сервис «Список покупок», который формирует
продуктовую корзину выбранных рецептов пользователя, ее можно скачать в виде
файла и отправиться за покупками.

![Workflow](https://github.com/drode1/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Проверить сайт можно по ссылке [eremezov.ru](https://eremezov.ru)
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

1. В папке ```infra/``` создайте файл, по аналогии
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

### Как развернуть проект на сервере
1. Скопируйте на сервер папку `docs`
2. Скопируйте на сервер файл `infra/docker-compose-server.yml` и переименуйте его в `docker-compose.yml (для версии без SSL скопируйте файл `infra/docker-compose.yml`)
3. Создайте на сервере папку `nginx` и поместите в него файл `infra/nginx.conf`, предварительно изменив `server_name` на имя вашего сервера (если нужна версия без ssl, то скопируйте файл `nginx-local.conf`)
4. Соберите папку `static на сервере. Для этого нужно:
   6. Собрать статику django проекта, с помощью команды `python manage.py collectstatic --no-input`
   7. Сделать build frontend папки проекта и скопируйте из папки `build/static` папки `css, js, media` и добавьте
   8. Переместить все папки из двух пунктов выше в папку `static` на сервере 
9. Запустите контейнер с помощью команды `sudo docker-compose up -d`, а после сделайте миграции и импорт тестовых данных
   10. `sudo docker exec -it backend bash`
   11. `python manage.py migrate`
   12. `python manage.py import`
13. Затем перезапустите контейнер с помощью команды из п.4
___

## Контакты

- [Егор Ремезов](https://github.com/drode1)
    - [Telegram](https://t.me/e_remezov)
    - [Mail](mailto:info@eremezov.com)

___