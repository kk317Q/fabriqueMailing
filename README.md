# fabriqueMailing

##Запуск проекта и зависимостей

1. Копирование файлов проекта на локальный ПК

'https://github.com/kk317Q/fabriqueMailing.git'

2. Переходим в папку с проектом fabriqueMailing(Указан условный путь до проекта)
'cd documnets/fabriqueMailing'

4. Запуск виртуальной среды
'conda activate fabriqueEnv'

3. Установка всех зависимостей. Команда ниже установит необходимые библиотеки для работы приложения: Django, DRF, Celery, etc.
'pip install -r requirements.txt'

4. Настройка базы данных. 
   - В разработке использовался PostgreSQL. 
   - Для запуска проекта, Вам необходимо установить PostgreSQL на компьютер
   - Затем запустите PostgreSQL сервер на компьютере. 
   - Далее необходимо добавить настройки сервера в Django проект в файле settings.py

'DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fabriqueMailingDataBase',  #Имя базы данных
        'USER': 'postgres', #Ваше имя пользователя на сервере PostgreSQL
        'PASSWORD': '123456', #Ваше пароль пользователя на сервере PostgreSQL
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}'
