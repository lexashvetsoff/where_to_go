# where_to_go
![Alt text](https://github.com/lexashvetsoff/where_to_go/blob/main/screenshots/where_to_go_1.png)
Сайт выводит интересные места на карте с их описанием.  
[Пример сайта](https://lexashvetsoff.pythonanywhere.com/)

## Как запустить

Для запуска сайта вам понадобится Python третьей версии.

Скачайте код с GitHub.  

Создайте файл .env с переменными окружения  

Создайте виртуальное окружение  
```sh
python3 -m venv venv
```

Затем установите зависимости

```sh
pip install -r requirements.txt
```

Выполните миграции  
```sh
python3 manage.py migrate
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
- `SECURE_HSTS_SECONDS` — в production среде эти переменные среды окружения должны иметь значения ```True``` см [документацию](https://docs.djangoproject.com/en/4.0/ref/settings/#secure-hsts-seconds)  
- `SECURE_SSL_REDIRECT` — в production среде эти переменные среды окружения должны иметь значения ```True``` см [документацию](https://docs.djangoproject.com/en/4.0/ref/settings/#secure-ssl-redirect)  
- `SESSION_COOKIE_SECURE` — в production среде эти переменные среды окружения должны иметь значения ```True``` см [документацию](https://docs.djangoproject.com/en/4.0/ref/settings/#session-cookie-secure)  
- `CSRF_COOKIE_SECURE` — в production среде эти переменные среды окружения должны иметь значения ```True``` см [документацию](https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-cookie-secure)  
- `ALLOWED_HOSTS` — см [документацию](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)

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
