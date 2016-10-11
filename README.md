## ProEQ web app

### Необходимые утилиты
* docker (1.6.0 и выше)
* docker-compose (1.3.1 и выше)

### Как собрать и запустить

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

### Остановка сервиса
Для остановки работы контейнеров выполните следующую команду в директории с проектом
```bash
$ docker-compose stop
```