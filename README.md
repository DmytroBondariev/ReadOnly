# Library-API-Service

Service for borrowing books with stripe payment system and notifications via telegram bot

## Installing process
Change mocks to your native data inside .env.sample. Do not forget to change file name to ".env".
#### Run with IDE
```
    git clone https://github.com/DmytroBondariev/ReadOnly.git
    cd ReadOnly
    python -m venv venv
    sourse venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
```
#### Set unique data to .env file
    DJANGO_SECRET_KEY=your_django_secret_key
    TELEGRAM_TOKEN=your_telegram_token
    TELEGRAM_CHAT_ID=your_chat_id
    STRIPE_SECRET_KEY=your_stripe_secret_key

## Run Redis/Celery/Celery-Beat
Docker should be installed locally to run Redis
#### Open separate terminal window for each command
```
    docker run -p 127.0.0.1:16379:6379 --name redis-celery -d redis
    celery -A library_service worker -l info --pool=solo -n worker@%h
    celery -A library_service beat -l INFO
    .\borrowings\telegram_helpers.py
```

## Getting access

* proceed to the BotFather in Telegram (https://t.me/BotFather) and create new bot
* set your bot token to TELEGRAM_TOKEN in .env file
* get your chat id via command "/start" in chat with your bot and set it to TELEGRAM_CHAT_ID in .env file
* create user via "/api/user/register"
* get access token via "api/user/login" (do not forget to add "Bearer " before token)
* create authors, books and proceed to creating borrowings via "/api/borrowings/"


## Features
* JWT authenticated
* Admin panel /admin/
* Managing borrowings depending on user stuff role
* Paying for borrowings with stripe
* Notifications via telegram bot
* Filtering borrowings by status and user
* Filtering books by author, title
