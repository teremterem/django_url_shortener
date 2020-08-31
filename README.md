# Django URL Shortener

## Install Docker Compose

- [Install Docker Compose](https://docs.docker.com/compose/install/)
- [Configure Docker to run without sudo (Linux)](
   https://docs.docker.com/engine/install/linux-postinstall/)

## Clone this repo
- Clone this repo with either SSH
   ```
   git clone git@github.com:teremterem/django_url_shortener.git
   ```
   or HTTPS
   ```
   git clone https://github.com/teremterem/django_url_shortener.git
   ```
   or get it any other way that suits you and that GitHub supports
- Go to the repo dir (the rest of the instruction assumes
   that you're at the top of the repo directory structure)
   ```
   cd django_url_shortener/
   ```

## Migrate DB

```
docker-compose run --rm web pipenv run python manage.py migrate
```
***This step is required before running the app for the first time.***  
After that (and unless DB models were changed and new DB migrations were added)
there is no need to migrate DB again.

## Test

```
docker-compose run --rm web pipenv run python manage.py test
```

## Run

```
docker-compose up
```
Then open http://localhost:8000/ in your browser.

## Rebuild

```
docker-compose build
```
One example of when rebuilding Docker would be necessary is after dependencies were changed in Pipfile and Pipfile.lock

## Debug with [ipdb](https://github.com/gotcha/ipdb)

- Insert the following code at the location where you want to break into the debugger:
  ```python
  import ipdb; ipdb.set_trace()
  ```
- If you are trying to debug tests then run the tests as described above in [Test](#Test) section.
- ***If you are trying to debug the app itself then run it using the following command:***
  ```
  docker-compose run --rm -p 8000:8000 web
  ```
  Running it this way instead of using ```docker-compose up```
  ensures that you will be able to interact with ipdb (make sure to first stop the app if it is already running with
  ```docker-compose up```).

You will break into the debugger as soon as python interpreter reaches the code above that you inserted (pay attention
to the console in which you ran docker-compose command).

See an [ipdb cheat sheet](https://wangchuan.github.io/coding/2017/07/12/ipdb-cheat-sheet.html) for quick help on how to
interact with ipdb debugger.

## Choices made

- **Pipenv** (see basic usage [here](https://pipenv-fork.readthedocs.io/en/latest/basics.html))  
  Versions of the whole dependency tree are frozen in Pipfile.lock and for this reason it is ok to have wildcards and
  ranges instead of specific versions in Pipfile. See [this article](https://realpython.com/pipenv-guide/) for more
  info.
- Shortly.cc urls are super short (5 chars currently - which is max 1 billion urls in case of 64 letters).

TODO

### Attempt to improve url lookup performance

- https://realpython.com/lessons/cryptographically-secure-random-data-python/
- Inspiration: https://pypi.org/project/short_url/
- https://en.wikipedia.org/wiki/Universally_unique_identifier
- https://stackoverflow.com/questions/33836749/postgresql-using-uuid-vs-text-as-primary-key
- https://docs.python.org/3/library/secrets.html#recipes-and-best-practices

TODO

## Areas of improvement

- Switch from Django built-in web server to [a production grade web server](
  https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/) (try out [ASGI](
  https://asgi.readthedocs.io/en/latest/)).
- Use [multiple docker compose files](
  https://runnable.com/docker/advanced-docker-compose-configuration#using-multiple-docker-compose-files)
  to make commands that run DB migrations, unit tests etc. shorter.
  - Also use more than one Dockerfile to separate between prod / non-prod images?  
    For ex. prod version of Dockerfile should contain
    ```
    RUN pipenv install --deploy
    ```
    instead of
    ```
    RUN pipenv install --dev --deploy
    ```
- Measure test [coverage](https://coverage.readthedocs.io/en/coverage-5.2.1/).
- Switch from unittests to [pytest-django](https://pytest-django.readthedocs.io/en/latest/)?  
  Add [pytest-bdd](
  https://automationpanda.com/2018/10/22/python-testing-101-pytest-bdd/) for black box testing (try out BDD)?  
  Some of the advantages of pytest over vanilla unittest:
  - pytest fixtures
  - framework level support of python's native assert statements
    (unittest requires you to use it's own assert functions if you want test output to be informative)
- Describe in this README.md how to use [pdb](https://docs.python.org/3/library/pdb.html)
  to debug Django app inside Docker (as well as how to debug tests).
- Benchmark url lookup speed (what toolset to use for this?)
- Switch from Django template with a form to REST and JSON ([is CSRF concern relevant in case of REST?](
  https://security.stackexchange.com/questions/166724/should-i-use-csrf-protection-on-rest-api-endpoints)) for url
  shortening to make this service headless (and attach a simple jQuery based UI page to it).
- Turn url expander view into Django middleware ? (to avoid the overhead of url resolution).
- Cover Django views with tests as well.
- Turn some of the unit tests into doctests?
- Validate that it is indeed a url that is being shortened

### Ideas to further improve url lookup

- Sharding of postgres table across multiple postgres servers
- Does sharding redis make any sense at all?

## Miscellaneous

### Command to make DB migrations

```
docker-compose run --rm web pipenv run python manage.py makemigrations
```

### Commands to log into the running Docker container

See [SSH into a Container](
https://phase2.github.io/devtools/common-tasks/ssh-into-a-container/)

### Commands that were used to create Django project and app

```
docker-compose run --rm web pipenv run django-admin startproject django_url_shortener .
docker-compose run --rm web pipenv run django-admin startapp url_shortener
```

## More references

1) https://choosealicense.com/
1) https://docs.docker.com/compose/django/
1) https://hub.docker.com/_/python
1) https://github.com/docker-library/faq#whats-the-difference-between-shared-and-simple-tags
1) https://docs.djangoproject.com/en/3.1/topics/db/models/
1) https://docs.djangoproject.com/en/3.1/topics/migrations/
1) https://pythonspeed.com/articles/schema-migrations-server-startup/
1) https://docs.djangoproject.com/en/3.1/topics/testing/overview/
1) https://odwyer.software/blog/how-to-use-ipdb-with-docker-compose
1) https://stackoverflow.com/questions/36249744/interactive-shell-using-docker-compose
1) https://docs.python.org/3/library/unittest.mock.html

### TODO

1) https://realpython.com/caching-in-django-with-redis/
1) https://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint/
1) https://stackoverflow.com/questions/7382149/purpose-of-django-setting-secret-key
1) https://www.forbes.com/sites/ygrauer/2016/04/20/five-reasons-you-should-stop-shortening-urls/#17ecff623f69
1) https://en.wikipedia.org/wiki/URL_shortening
