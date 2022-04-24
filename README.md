# fabriqueMailing

## О сервисе
 fabriqueMailing это API сервис по рассылке сообщений клиентам. Приложение способно делать рассылку сообщений в фоновом режиме, таким образом не замедляя взаимодействия клиентов с сервисом. Приложение разработано на основе Django + Rest Framework и Celery + Redis. Ключевой функционал позволяет работать с Рассылками, Клиентами и Сообщениями. Можно создавать, обновлять, а так же удалять элементы ссылаясь практически на один и тот же URL но по разным методам. Исключением будет два специфичных URL дающие дополнительные возможности: **mailingsStatisticsOverall** и **retrieveMessagesForMailing**. 

## Запуск проекта и зависимостей

##### 1. Копирование файлов проекта на локальный ПК

  https://github.com/kk317Q/fabriqueMailing.git 

### Окно терминала 1
##### 2. Переходим в папку с проектом fabriqueMailing(Указан условный путь до проекта) и запускаем виртуальную среду

     cd documnets/fabriqueMailing
     conda activate fabriqueEnv

     
 
##### 3. Установка всех зависимостей. Команда ниже установит необходимые библиотеки для работы приложения: Django, DRF, Celery, etc.
     pip install -r requirements.txt 

##### 4. Настройка базы данных. 
   - В разработке использовался PostgreSQL. 
   - Для запуска проекта, Вам необходимо установить PostgreSQL на компьютер
   - [Инструкция по установкеPostgreSQL](https://www.postgresql.org/docs/current/installation.html)
   - Затем запустите PostgreSQL сервер на компьютере. 
   - [Инструкция по запуску сервера](https://www.postgresql.org/docs/current/app-pg-ctl.html)
   - Далее необходимо добавить настройки сервера в Django проект в файле settings.py

 DATABASES = {

    'default': {
    
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        
        'NAME': 'fabriqueMailingDataBase',  #Имя базы данных - ИЗМЕНИТЬ
        
        'USER': 'postgres', #Ваше имя пользователя на сервере PostgreSQL - ИЗМЕНИТЬ
        
        'PASSWORD': '123456', #Ваше пароль пользователя на сервере PostgreSQL - ИЗМЕНИТЬ
        
        'HOST': '127.0.0.1', 
        
        'PORT': '5432',
        
    }
    
} 

##### 5. Создание таблиц в БД по двум командам. Соблюдайте очерёдность команд. 
     python manage.py makemigrations 
     python manage.py migrate 
     
### Окно терминала 2
##### 6. Прежде чем запускать Celery, необходимо настроить брокера сообщений Redis. 
   • Сначала необходимо открыть новое окно терминала и установить Redis. 
   [Инструкция по установке Redis](https://redis.io/docs/getting-started/)
  
   • Далее необходимо в Django settings.py убедиться в корректности адреса Redis сервера
   
     CELERY_BROKER_URL = 'redis://localhost:6379' #Заменить по необходимости на актуальный адрес
     CELERY_RESULT_BACKEND = 'redis://localhost:6379' #Заменить по необходимости на актуальный адрес
     CELERY_ACCEPT_CONTENT = ['application/json']  
     CELERY_RESULT_SERIALIZER = 'json'  
     CELERY_TASK_SERIALIZER = 'json'  
     CELERY_TIMEZONE = 'Europe/Moscow'
     CELERY_ALWAYS_EAGER = True
    
   • Затем в терминале введите команду для запуска сервера
   
    redis-server
 
   
   Redis готов к работе. Переходим к Celery

### Окно терминала 3
##### 7. Следующим шагом в отдельном окне терминала запустим Celery процессы для поддержки фоновой обработки задач на backend. Следуйте шагам ниже
   • В новом окне терминала перейдите в папку проекта 
   
     cd documnets/fabriqueMailing
   
   • Далее активируйте виртуальную среду и запустите Celery Beta - для возможности планирования задач
  
     conda activate fabriqueEnv
  
     celery -A fabriqueMailing beat -l INFO
  
### Окно терминала 4
##### 8. Далее в очередном новом окне терминала повторите комнады из 6 пункта, с измененной последней командой для запуска Celery Worker

     cd documnets/fabriqueMailing 
     
     conda activate fabriqueEnv
     
     celery -A fabriqueMailing worker -l INFO -n worker1
 
### Окно терминала 1
##### 9. Последний шаг: Запуск Django сервера в первом окне терминала
     python manage.py runserver 
   
Сервер готов к работе!

_____

# API Endpoints
Разработанный сервис имеет ряд Endpoints доступных для внешнего клиента. 
Доступ к ним можно получить через определённый **URL** и Request Method(GET, POST, PUT, etc) + имеет значение наличие **параметеров в URL**

#### •Доступ к OpenAPI спецификации можно получить через URL
#### [http://{yourDomain}/api/v1/swagger/](swagger)

_____
Ниже представлены основные API:

### API для Клиентов

#### •Получение информации обо всех созданных Клиентах(GET)
#### [http://{yourDomain}/api/v1/client/](Client)

#### •Получение информации об одном Клиенте(GET)
#### [http://{yourDomain}/api/v1/client/{id}](Client)

#### •Добавления нового Клиента в справочник со всеми его атрибутами(POST)
#### [http://{yourDomain}/api/v1/client/](Client)

#### •Обновления данных атрибутов Клиента(PUT)
#### [http://{yourDomain}/api/v1/client/{id}/](Client)

#### •Удаления Клиента из справочника(DELETE)
#### [http://{yourDomain}/api/v1/client/{id}/](Client)

____

### API для Рассылок

#### •Получение информации обо всех созданных Рассылках(GET)
#### [http://{yourDomain}/api/v1/client/](v)

#### •Получения общей статистики по созданным Рассылкам и количеству отправленных Ссообщений по ним с группировкой по статусам(GET)
#### [http://{yourDomain}/api/v1/mailing/mailingsStatisticsOverall/](Mailing)

#### •Обновления атрибутов Рассылки(PUT)
#### [http://{yourDomain}/api/v1/mailing/{id}](Mailing) 

#### •Удаления Рассылки(DELETE)
#### [http://{yourDomain}/api/v1/mailing/{id}](Mailing)

____

### API для Сообщений

#### •Получение информации обо всех созданных Сообщениях(GET)
#### [http://{yourDomain}/api/v1/message/](message)

#### •Получения детальной статистики отправленных Сообщений по конкретной Рассылке(GET) 
#### [http://{yourDomain}/api/v1/message/{id}/retrieveMessagesForMailing/](message)
*В данном запросе передаётся ID Рассылки, а не Собщения*

____
Вся основаня информация по запуску проекта и API Endpoints указана в данном README. Теперь Вы можете начать работу с сервисом!

____
### Интерфес Администратора
В проекте реализована возможность управелния базой данных и расслыками через WEB UI. Вы можете создавать рассылки и смотреть короткую статистику по ним. 
Так же как с API, созданная рассылка автоматически запустится в фоне. Чтобы подключиться к WEB UI:

### Окно терминала 1
##### 1. Введите команду ниже и следуйте инструкциям в терминале

    python manage.py createsuperuser
  
##### 2. Далее перейдите по URL и войдите в систему под своим логином/паролем [http://{yourDomain}/admin](Admin)

### Настройка EMAIL
В проекте реализована возможность автоматической отправки информации по рассылкам на Вашу почту на ежедневной основе. Для правильной работы сервиса, Вам нужно будет указать правильную конфигурацию для подключения к почтовому сервису и указать получателя. 

##### 1. В settings.py укажите правильные данные для почты. 

      #Email Settings
      EMAIL_HOST = 'smtp.gmail.com' #Укажите данные под Вашу почту
      EMAIL_PORT = 587
      EMAIL_HOST_USER = 'somegmail.com' #Укажите данные под Вашу почту
      EMAIL_HOST_PASSWORD = 'somePassword+' #Укажите данные под Вашу почту
      EMAIL_USE_TLS = True

##### 2. В mailingApp/tasks.py укажите адрес получателя отчётов(аттрибут to=['someMail@yandex.ru'])


      88: email = EmailMessage('Mailing statistics', someStr.join(str(element)+'\n' for element in varContainer), to=['someMail@yandex.ru'])

Всё настроено. Можете перезапускать сервера Celery Beat, Worker, Django и пользоватся всеми возможностями. 
   

## Дополнительные задания

•Сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API. Пример: https://petstore.swagger.io

•Реализовать дополнительный сервис, который раз в сутки отправляет статистику по обработанным рассылкам на email

•Реализовать администраторский Web UI для управления рассылками и получения статистики по отправленным сообщениям

•Удаленный сервис может быть недоступен, долго отвечать на запросы или выдавать некорректные ответы. Необходимо организовать обработку ошибок и откладывание запросов при неуспехе для последующей повторной отправки. Задержки в работе внешнего сервиса никак не должны оказывать влияние на работу сервиса рассылок
