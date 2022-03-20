# Сервис рассылки уведомлений


## Установка
Скачайте проект с репозитория Github
```bash
https://github.com/RadikAgl/notifications-service.git
```

Создайте в корне директории project файл .env и поместите туда JWT токен для авторизации в сервисе отправки сообщений клиентам. В этом проекте используется данный сервис для отправки уведомлений.
В приложении осуществлена отправка общей статистики на почту. Укажите следующие данные в файле .env:
```.env
TOKEN=Ваш токен
EMAIL_HOST=сервер smtp
EMAIL_HOST_USER=логин для входа на сервер SMTP
EMAIL_HOST_PASSWORD=пароль для входа на сервер SMTP
EMAIL_PORT=порт сервера smtp
ADMIN_EMAIL=test@email.com - почта, куда нужно отправлять статистику
```

## Запуск приложения
Выполните следующую команду для запуска всех контейнеров
```bash
docker-compose up -d
```

В приложении реализована административная панель, где можно управлять рассылками, списков клиентов и подготовленных сообщений.
Административная панель находится по адресу [http://0.0.0.0:8001/admin/](http://0.0.0.0:8001/admin/),
но предварительно нужно создать пользователя. Введите команду:

```bash
docker-compose exec web python manage.py createsuperuser
```
Далее нужно ввести логин создаваемого пользователя, почту(необязательно, пропустите, нажав Ввод) и дважды пароль.


После запуска по адресу [http://0.0.0.0:8001/docs/](http://0.0.0.0:8001/docs/) можно ознакомиться всем функционалом приложения.
В проекте осуществляется мониторинг приложения с помощью Prometheus. Метрики можно посмотреть по адресу [http://0.0.0.0:8001/metrics/](http://0.0.0.0:8001/metrics/)
