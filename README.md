# Django URL Shortener

## Installation

1) [Install Docker Compose](https://docs.docker.com/compose/install/)
1) [Configure Docker to run without sudo (Linux)](
   https://docs.docker.com/engine/install/linux-postinstall/)
1) Clone this repo with either SSH
   ```shell script
   git clone git@github.com:teremterem/django_url_shortener.git
   ```
   or HTTPS
   ```
   git clone https://github.com/teremterem/django_url_shortener.git
   ```
   or any other way that suits you and that GitHub supports
1) Go to the repo dir (the rest of the instruction assumes
   that you're at the top of the repo directory structure)
   ```shell script
   cd django_url_shortener/
   ```

## Migrating DB

```shell script
docker-compose run web pipenv run python manage.py migrate
```

## Testing

TODO

## Running

```shell script
docker-compose up
```
Then open http://localhost:8000/ in your browser.

## Rebuilding

This is necessary when dependencies are changed in Pipfile and Pipfile.lock

```shell script
docker-compose build
```

## Choices made

- Pipenv
- I could have specified versions of packages in Pipfile but I haven't done so.
  Versions are frozen in Pipfile.lock so there is no danger of not specifying them in Pipfile.
  I will probably come back to this later and specify at least major parts of versions of my direct
  dependencies solely for the sake of being explicit in the eyes of the reader of this repo.

TODO

## Areas of improvement

- Switch from Django built-in web server to [a production grade web server](
  https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/) (try out [ASGI](
  https://asgi.readthedocs.io/en/latest/)).
- Use [multiple docker compose files](
  https://runnable.com/docker/advanced-docker-compose-configuration#using-multiple-docker-compose-files)
  to make commands that run DB migrations, unit tests etc. shorter.
  - And more than one Dockerfile to separate between prod / non-prod images?  
    For ex. prod version of Dockerfile should contain
    ```shell script
    RUN pipenv install --deploy
    ```
    instead of
    ```shell script
    RUN pipenv install --dev --deploy
    ```
- Measure test [coverage](https://coverage.readthedocs.io/en/coverage-5.2.1/).

## Misc

### Command to make DB migrations

```shell script
docker-compose run web pipenv run python manage.py makemigrations
```

### Commands to log into the running Docker container

See [SSH into a Container](
https://phase2.github.io/devtools/common-tasks/ssh-into-a-container/).

### Commands that were used to create Django project and app

```shell script
docker-compose run web pipenv run django-admin startproject django_url_shortener .
docker-compose run web pipenv run django-admin startapp url_shortener
```

## References

1) https://choosealicense.com/
1) https://docs.docker.com/compose/django/
1) https://hub.docker.com/_/python
1) https://github.com/docker-library/faq#whats-the-difference-between-shared-and-simple-tags
1) https://realpython.com/pipenv-guide/
1) https://pipenv-fork.readthedocs.io/en/latest/basics.html
1) https://docs.djangoproject.com/en/3.1/topics/db/models/
1) https://docs.djangoproject.com/en/3.1/topics/migrations/
1) https://pythonspeed.com/articles/schema-migrations-server-startup/

### TODO

1) https://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint/
1) https://stackoverflow.com/questions/7382149/purpose-of-django-setting-secret-key
