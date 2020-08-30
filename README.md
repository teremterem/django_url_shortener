# Django URL Shortener

## Installation

1) [Install Docker Compose](https://docs.docker.com/compose/install/)
1) [Configure Docker to run without sudo (Linux)](https://docs.docker.com/engine/install/linux-postinstall/)
1) Clone this repo with either SSH
   ```shell script
   git clone git@github.com:teremterem/django_url_shortener.git
   ```
   or HTTPS
   ```
   git clone https://github.com/teremterem/django_url_shortener.git
   ```
1) Go to the repo dir (the rest of the instruction assumes that you're inside the repo dir)
   ```shell script
   cd django_url_shortener/
   ```

### Migrating DB

TODO

### Running

```shell script
docker-compose up
```

### Rebuilding

This is necessary when dependencies are changed in Pipfile and Pipfile.lock

```shell script
docker-compose build
```

## Misc

### Commands that were used to create Django project and app inside Docker

```shell script
docker-compose run web pipenv run django-admin startproject django_url_shortener .
docker-compose run web pipenv run django-admin startapp url_shortener
```

## References

1) https://choosealicense.com/
1) https://docs.docker.com/compose/django/
1) https://realpython.com/pipenv-guide/
1) https://pipenv-fork.readthedocs.io/en/latest/basics.html

### TODO

1) https://stackoverflow.com/questions/7382149/purpose-of-django-setting-secret-key
1) https://pythonspeed.com/articles/schema-migrations-server-startup/
1) https://runnable.com/docker/advanced-docker-compose-configuration
1) https://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint/
