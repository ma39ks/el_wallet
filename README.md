## Установка

Потребуется докер для запуска проекта.
```bash
docker-compose up --build
```

## Использование

Проект запускается по адресу http://localhost:8000/, для начала нужно будет через /admin/ создать новых пользователей, так же можно создать им кошельки и транзакции. По адресу /login/ можно залогиниться под созданным пользователем, после входа открывается страница существующих кошельков, откуда можно создать транзакцию. 

## Тестирование

В контейнере в разделе exec нужно выполнить:
```bash
python manage.py test
```

## Логирование

В корне проекта в папке logs находится файл логов куда записывается основная информация по действиям пользователей.