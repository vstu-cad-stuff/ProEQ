## ProEQ web app

### Необходимые утилиты
* docker (1.6.0 и выше)
* docker-compose (1.3.1 и выше)

### Как собрать и запустить
Создаём файл `.env` со следующем содержимым:
```bash
DEBUG=True
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
DB_SERVICE=postgres
DB_PORT=5432
SECRET_KEY=<введите-свой-ключ>
```
Так же не забываем установить `SECRET_KEY`!


Собираем контейнеры
```bash
$ docker-compose build
```

Поднимаем их
```bash
$ docker-compose up -d
```

И создаём `demo` пользователя
```bash
$ docker-compose run web /usr/local/bin/python create_demo.py
```

Теперь можно открыть сам веб-сервис в браузере <localhost:4040>:

### Остановка сервиса
Для остановки работы контейнеров выполните следующую команду в директории с проектом
```bash
$ docker-compose stop
```