# Сервис рассылки уведомлений


## Установка
Скачайте проект с репозитория Gitlab
```bash
git clone
cd project
```

Создайте в корне директории project файл .env и поместите туда JWT токен для авторизации в сервисе. В этом проекте используется данный сервис для отправки уведомлений.
```.env
TOKEN=Ваш токен
```

## Запуск приложения
Выполните следующую команду для запуска приложения
```bash
docker-compose up -d
```

Примените миграции:
```bash
docker-compose run web python manage.py migrate
```

После запуска по адресу [http://0.0.0.0:8001/swagger/](http://0.0.0.0:8001/swagger/) можно ознакомиться всем функционалом приложения.
