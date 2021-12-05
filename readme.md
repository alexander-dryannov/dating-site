# Looking my love.

## Deploy

### Установка зависимостей

```shell
sudo apt install python3-pip supervisor libpq-dev pipenv nginx postgesql make build-essential
mkdir -p www/python/apps/
cd www/python/apps/
```
### Клонирование ветки deploy

```shell
git clone -b deploy https://github.com/alexander-dryannov/dating-site.git
```

```shell
sudo -u postgres psql
CREATE DATABASE new_database_name;
CREATE ROLE username LOGIN SUPERUSER PASSWORD 'your password';
ALTER ROLE username SET client_encoding TO 'utf8';
ALTER ROLE username SET default_transaction_isolation TO 'read committed';
ALTER ROLE username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE new_database_name TO username;
\q
```

### Добавление переменных окружения

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

### Настройка gunicorn

В каталоге config в файлах gunicorn.conf.py и lml.conf исправить current_user на имя своего пользователя.

### Настройка supervisor

```shell
cd /etc/supervisor/conf.d
sudo ln /home/current_user/www/python/apps/dating-site/looking_my_love/config/lml.conf
sudo update-rc.d supervisor enable
sudo service supervisor start
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status project
sudo supervisorctl restart project
```

### Настройка nginx
Открыть файл /etc/nginx/sites-available/default и добавить:

    server {
        listen 80;
        server_name your ip or domain name
        access_log  /var/log/nginx/example.log;
    
        location /static/ {
            root /home/current_user/www/python/apps/dating-site/looking_my_love/;
            expires 30d;
        }
        location /media/ {
            root /home/current_user/www/python/apps/dating-site/looking_my_love/;
            expires 30d;
        }
    
        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $server_name;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}




## Фильтрация.

- Фильтрация по полу
  - /api/list?gender=
- Фильтрация по имени
  - /api/list?first_name=
- Фильтрация по фамилии
  - /api/list?last_name=
- Фильтрация по городу
  - /api/list?city=
- Фильтрация по дистанции
  - /api/list?distance=киллометры
