# where_to_go
![Alt text](https://github.com/lexashvetsoff/where_to_go/blob/main/screenshots/where_to_go_1.png)
Сайт выодит интересные места на карте с их описанием.  
[Пример сайта](https://lexashvetsoff.pythonanywhere.com/)

## Как запустить

Для запуска сайта вам понадобится Python третьей версии.

Скачайте код с GitHub. Затем установите зависимости

```sh
pip install -r requirements.txt
```

Запустите разработческий сервер

```sh
python3 manage.py runserver
```

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны переменные:
- `DEBUG` — дебаг-режим. Поставьте True, чтобы увидеть отладочную информацию в случае ошибки.
- `SECRET_KEY` — секретный ключ проекта  
- `SECURE_HSTS_SECONDS` — при деплои поставить True  
- `SECURE_SSL_REDIRECT` — при деплои поставить True  
- `SESSION_COOKIE_SECURE` — при деплои поставить True  
- `CSRF_COOKIE_SECURE` — при деплои поставить True  

## API
У сайта есть свой API, который отдает информацию в формате json по выбранному месту. Для этого к домену необходимо добавить запись вида "/places/id места", например: ```https://lexashvetsoff.pythonanywhere.com/places/1```

## Загрузка данных
Для загрузки из файла json необходимо ввести следующую команду:
```sh
python3 manage.py load_place путь/к/файлу/json
```

Сам файл json должен иметь следующую структуру:
```json
{
    "title": "Название",
    "imgs": [
        "список url-адресов изображений"
    ],
    "description_short": "Короткое описание",
    "description_long": "<p>Длинное описание, которое может содержать html-тэги href=\"https://www.instagram.com/anticafe.bi.zone/\" target=\"_blank\">в Instagram</a>.</p>",
    "coordinates": {
        "lng": "долгота",
        "lat": "широта"
    }
}
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
