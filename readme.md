# Looking my love.

## Добавление переменных окружения

В каталоге с файлом settigns.py создать файл .env и добавить в него следующие ключи:

    SECRET_KEY=your_secret_key
    
    NAME=database_name
    
    USER=username
    
    PASSWORD=user_password
    
    HOST=host_port
    
    PORT=postgres_port
    
    EMAIL_HOST=smtp.yandex.ru(for yandex)
    
    EMAIL_PORT=465(for yandex)
    
    EMAIL_HOST_USER=email
    
    EMAIL_HOST_PASSWORD=mail_password
    
    DEFAULT_FROM_EMAIL=email
    
    EMAIL_USE_TLS=False(for yandex)
    
    EMAIL_USE_SSL=True(for yandex)

## Фильтрация.

- Фильтрация по полу
  - /api/list?gender=
- Фильтрация по имени
  - /api/list?first_name=
- Фильтрация по фамилии
  - /api/list?last_name=
- Фильтрация по дистанции
  - /api/list?distance=киллометры
