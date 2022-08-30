# Setup enviroment for local development

## Local development

If you want to develop something here is instruction how to setup local enviroment. Enjoy!

### Setup pipenv (Python)

1. Get pipenv: `pip3 install --user pipenv`
2. Install packages and activate virtual environment: `pipenv install --dev`
3. Check that it was installed correctly: `pipenv shell`
4. Exit from shell: `exit()`

### Setup postgres

#### locally
  Easies way is to run postgres is to run in docker, just run it with follow command:
  ```sh
  docker-compose -f docker-compose.yml up -d postgres
  ```
  When you need to connect to postgres use next params:
  ```dotenv
  POSTGRES_DB=vas3k_club
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  POSTGRES_HOST=localhost
  ```

  <details><summary>In case you really want setup local postgres then go under cut...</summary>

    Brief instruction:
  
    1. Install postgresql (for macos https://postgresapp.com/ is easies start)
    2. After you install and run postgress create a project database:
          ```sh
          # create db
          $ psql postgres
          postgres=# createdb pmi_club

          # create user (user: pmiclub, password: pmiclub)
          postgres=# createuser --interactive --pwpromp

          # grant priviliges
          postgres=# GRANT ALL PRIVILEGES ON DATABASE pmi_club TO pmiclub;
          postgres=# \connect pmi_club
          postgres=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pmiclub;
          postgres=# GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to pmiclub;
          postgres=# GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public to pmiclub;
          postgres=# \q

          # check connection
          $ psql -d pmi_club -U pmiclub
          ```

  </details>
  
#### Setup frontend

Start new console proccess
```sh
$ cd frontend
$ npm run watch # will implicitly run `npm ci`
```

In case you have some issues with dependencies use `--legacy-peer-deps` flag
```sh
$ npm run watch --legacy-peer-deps
```

#### Make .env file

Go to club directory and copy .env.example file
```sh
$ cd club
$ cp .env.example .env
```

Explore `.env` file. Basic example:
```
SECRET_KEY="wow_secret_phrase"

POSTGRES_USER="postgres"
POSTGRES_PASSWORD="postgres"

MEDIA_UPLOAD_URL="https://<my.pepic.url>"
MEDIA_UPLOAD_CODE="<my.pepic.code>"

EMAIL_HOST="<my.mail.host>"
EMAIL_HOST_USER="<sender@email>"
EMAIL_HOST_PASSWORD="<password_for_sender>"
```

#### Run dev server

After you have setup postgres, venv and build frontend (look this steps above) complete preparations with follow commands:
```sh
# run redis (remove -d flag if you want console output)
docker-compose -f docker-compose.yml up -d redis

# run queue (in new console)
pipenv run python manage.py qcluster

# run db migration (Creates DB structure)
pipenv run python manage.py migrate

# Update tags
pipenv run python manage.py update_tags

# run dev server (In new console)
pipenv run python manage.py runserver 0.0.0.0:8000
```

## Telegram bot

To run telegram bot you have to:
  1. Copy env.exmaple file: `cp ./club/.env.example ./club/.env`
  2. Fill all the requirement fields in `./club/env`, such as `TELEGRAM_TOKEN` etc.
      - `TELEGRAM_TOKEN` you can get from [@BotFather](https://t.me/BotFather)
      - To get `TELEGRAM_CLUB_CHANNEL_URL`, `TELEGRAM_ADMIN_CHAT_ID` etc Just Simply Forward a message from your group/channel to [@JsonDumpBot](https://t.me/JsonDumpBot) or [@getidsbot](https://t.me/getidsbot)
  3. Rebuild application: `docker-compose up --build`

