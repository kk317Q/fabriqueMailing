# fabriqueMailing

## Запуск проекта и зависимостей

##### 1. Копирование файлов проекта на локальный ПК

`https://github.com/kk317Q/fabriqueMailing.git`

### Окно терминала 1
##### 2. Переходим в папку с проектом fabriqueMailing(Указан условный путь до проекта)
`cd documnets/fabriqueMailing`

 - и Запускаем виртуальную среду
'conda activate fabriqueEnv'

##### 3. Установка всех зависимостей. Команда ниже установит необходимые библиотеки для работы приложения: Django, DRF, Celery, etc.
`pip install -r requirements.txt`

##### 4. Настройка базы данных. 
   - В разработке использовался PostgreSQL. 
   - Для запуска проекта, Вам необходимо установить PostgreSQL на компьютер
   - [Инструкция по установкеPostgreSQL](https://www.postgresql.org/docs/current/installation.html)
   - Затем запустите PostgreSQL сервер на компьютере. 
   - [Инструкция по запуску сервера](https://www.postgresql.org/docs/current/app-pg-ctl.html)
   - Далее необходимо добавить настройки сервера в Django проект в файле settings.py

`DATABASES = {

    'default': {
    
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        
        'NAME': 'fabriqueMailingDataBase',  #Имя базы данных - ИЗМЕНИТЬ
        
        'USER': 'postgres', #Ваше имя пользователя на сервере PostgreSQL - ИЗМЕНИТЬ
        
        'PASSWORD': '123456', #Ваше пароль пользователя на сервере PostgreSQL - ИЗМЕНИТЬ
        
        'HOST': '127.0.0.1', 
        
        'PORT': '5432',
        
    }
    
}`

##### 5. Создание таблиц в БД по двум командам. Соблюдайте очерёдность команд. 
   `python manage.py makemigrations

    python manage.py migrate`

### Окно терминала 2
##### 6. Следующим шагом в отдельном окне терминала запустим Celery процессы для поддержки фоновой обработки задач на backend. Следуйте шагам ниже
   • В новом окне терминала перейдите в папку проекта 
   `cd documnets/fabriqueMailing`
   • Далее активируйте виртуальную среду и запустите Celery Beta - для возможности планирования задач
   'conda activate fabriqueEnv'
   'celery -A fabrieMailing beat -l INFO'
  
### Окно терминала 3
7. Далее в очередном новом окне терминала повторите комнады из 6 пункта, с измененной последней командой для запуска Celery Worker
   `cd documnets/fabriqueMailing`
   'conda activate fabriqueEnv'
   'celery -A fabrieMailing beat -l INFO'
 
### Окно терминала 1
##### 8. Последний шаг: Запуск Django сервера в первом окне терминала
   'python manage.py runserver'
   
Сервер готов к работе!


