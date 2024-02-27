# SETTING UP AND RUNNING THE CODE LOCALLY

### CLONING THE REOOSITORY
```
    git clone repo_url
```
### SETUP ENVIRONMENTAL VAIRABLES
<li>Locate the .env_sample file and add replace the value for REDIS_URL with <code>'redis://127.0.0.1:6379/1'</code></li>
<li>Locate the .env_sample file and add replace the value for RabbitMQ (CELERY_BROKER_URL) with <code>'amqp://guest:guest@localhost:5672'</code></li>
<li>Locate the .env_sample file and add replace the value for ACCESS_TOKEN_LIFETIME <code>60</code> which is in minutes</li>
<li>Locate the .env_sample file and add replace the value for REFRESH_TOKEN_LIFETIME <code>1</code> which is in measured in day(s)</li>
... and rename the file to <code>.env</code>

>[!NOTE]
please ensure REDIS and RABBITMQ Is Installed on your Local Machine, to avoid errors (using docker images containers is highly recommended while exposing the necessary ports)


### SETUP VIRTUAL ENVIRONMENT
```
    setup virtual environment and activate it(to avoid dependencies conflicts)
```


### INSTALING PROJECT DEPENDENCIES
```
    pip install -r requirements.txt
```

### APPLYING MIGRATIONS 

```
    python manage.py makemigrations
```

```
    python manage.py migrate
```

### RUNNING THE LOCAL/DEVELOPMENT SERVER

```
    python manage.py runserver
```

### RUNNING THE CELERY WORKER FOR ASYNCHRONOUS TASK (WINDOWS) 
```
    celery -A assesment_david worker --pool=solo -l info
```
### VIEW TASKS API WITH SWAGGER UI

```
    {{BASE_URL}}/swagger
```

where BASE_URL is <code> http://127.0.0.1:8000/</code>

### CREATING SUPER USER AND GROUPS
```
    python manage.py createsuperuser
```
...follow the prompt and after successful message, super user can access the admin page, create groups as required <br>

The Groups available are:
admin 
regular_users
others

### RUNNING TESTS FOR THE CODE 
```
    python manage.py test
```
... This will run all 4 test and return an OK status

>[!NOTE]

Please always append "/" at the end of all route to avoid a 404 Error

### USING ACCESS TOKEN IN SWAGGER UI
```
    Append Bearer before using the token on the swagger authorize Button i.e. it shoule follow the order with the white space

    Bearer TokenExample
```