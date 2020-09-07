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
:warning: ***This step is required before running the app for the first time.***

After that (and unless DB models were changed and new DB migrations were added)
there is no need to migrate DB again.

## Test

Run the tests:
```
docker-compose run --rm web pipenv run coverage run --source=. manage.py test
```

To generate test [coverage](https://coverage.readthedocs.io/) report run the following command:
```
docker-compose run --rm web pipenv run coverage html
```
And then open `htmlcov/index.html` in your browser:
```
open htmlcov/index.html
```

## Run

```
docker-compose up
```
Then open http://localhost:8000/ in your browser.

---

:warning: ***If you are not hosting this app locally (and/or you modified `docker-compose.yml` in such a way that the
app is available on a different port) then you also need to specify `DJANGO_URL_SHORTENER_PREFIX` env var for `web`
Docker container, which you can do [either in docker-compose.yml or through CLI](
https://docs.docker.com/compose/environment-variables/).***

Here is a relevant snippet from `docker-compose.yml`:
```
  ...
  web:
    environment:
      - DJANGO_URL_SHORTENER_PREFIX=http://localhost:8000/  # change to https://yourdomain.io/
                                                            # (replace yourdomain.io with your domain name)
      - ...
```
Changing this env var will ensure that the short urls that the app produces when url shortening is requested will start
with the prefix you specified. For ex. `https://yourdomain.io/WBcTkD5`.

:warning: ***`docker-compose up` needs to be restarted after `docker-compose.yml` is edited.***

## Rebuild

```
docker-compose build
```
One example of when rebuilding Docker would be necessary is after dependencies were changed in Pipfile and Pipfile.lock

## Debug with [ipdb](https://github.com/gotcha/ipdb)

Insert the following code at the location where you want to break into the debugger:
```python
import ipdb; ipdb.set_trace()
```
After that, if you are trying to debug tests then run the tests as described above in [Test](#Test) section.

:warning: ***If you are trying to debug the app directly (not through the tests) then run the app using the following
command:***
```
docker-compose run --rm -p 8000:8000 web
```
Running the app this way instead of using ```docker-compose up``` ensures that you will be able to interact with ipdb
(make sure to first stop the app if it is already running with ```docker-compose up```).

You will break into the debugger as soon as Python interpreter reaches the code above that you inserted (pay attention
to the console in which you ran docker-compose command).

See an [ipdb cheat sheet](https://wangchuan.github.io/coding/2017/07/12/ipdb-cheat-sheet.html) for quick help on how to
interact with ipdb debugger.

## URL shortening approach

A project description to [this library](https://pypi.org/project/short_url/) inspired me to do the following:
- When a long url is being shortened
  - A cryptographycally strong random sequence of 7 characters (a url handle) is generated using [secrets](
    https://docs.python.org/3/library/secrets.html#recipes-and-best-practices) library and an alphabet of 64 characters
    (see `generate_url_handle` function in `url_shortener/shortener/shortener_utils.py`).
  - This url handle is then converted to a number (`convert_url_handle_to_number` function of the same module) which is
    then used as primary key to store the original url against in a DB table (8-byte signed integer is used for this id
    in Postgres).
  - `64**7` (`4 398 046 511 103`) is not a small range of ids but still not UUID-grade, therefore a mechanism of up to 5
    handle (re)generation attempts is implemented when collisions happen.
- When a short url is being expanded
  - `convert_url_handle_to_number` function in `url_shortener/shortener/shortener_utils.py` is used to convert
    7-character url handle into a number which is then looked for in the primary key column of the DB table where long
    versions of urls are stored.  
    ***The assumption here is that lookup by int primary key is faster than by any other kind of primary key.***

Many URL shortening services use 5 chars for such handle. I used 7 to decrease the possibility of
[brute-force scanning](
https://www.forbes.com/sites/ygrauer/2016/04/20/five-reasons-you-should-stop-shortening-urls/#478be5e13f69) for short
urls by attackers at least somewhat while still keeping it short (however, I am not claiming doing so to be effective
against such scanning - I just hope that this way it is a bit harder to scan).

## How could it be improved further

- First of all, easily reproducible performance testing approach should be established for the app (see [issue #2](
  https://github.com/teremterem/django_url_shortener/issues/2)), in order to make the rest of optimization-for-speed
  decisions informed.
- Secondly, Redis in-memory cache could be used to cache long versions of urls (DB would still be used as permanent
  storage). I think, "least frequently used" eviction policy should be configured for such Redis cache.
- Redis sharding can also be considered. Splitting cached entries between several Redis servers and using certain bits
  of the id as a determinator of which server given entry belongs to (should be requested from). Given that ids are
  random rather than sequential the load between Redis servers should this way be distributed evenly.
- MICROOPTIMIZATION? `convert_url_handle_to_number` function is already optimized to use bitwise shift and xor (for
  what it's worth). Next step could be to replace Django view that accepts url handles (and responds with temporary
  redirects) with Django Middleware implementation in order to avoid the nessesity of going through Django's generic
  algorithm of url pattern matching.

## Choices made

- I always choose **pipenv** (see basic usage [here](https://pipenv-fork.readthedocs.io/en/latest/basics.html)) as
  dependency manager in my Python projects. It achieves the kind of dependency freezing that
  `pip freeze > requirements.txt` approach produces but does it in a much more elegant manner. Versions of the whole
  dependency tree are frozen in `Pipfile.lock` while `Pipfile` is used to maintain the list of the actual project
  dependencies (and not mix them with dependencies of dependencies as `pip freeze` does and which becomes a
  maintenance nightmare). See [this article](https://realpython.com/pipenv-guide/) for more info.

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

## Other useful links

1) https://choosealicense.com/
1) https://docs.docker.com/compose/django/
1) https://hub.docker.com/_/python
1) https://github.com/docker-library/faq#whats-the-difference-between-shared-and-simple-tags
1) https://docs.djangoproject.com/en/3.1/topics/migrations/#the-commands
1) https://pythonspeed.com/articles/schema-migrations-server-startup/
1) https://docs.djangoproject.com/en/3.1/topics/testing/overview/
1) https://odwyer.software/blog/how-to-use-ipdb-with-docker-compose
1) https://stackoverflow.com/questions/36249744/interactive-shell-using-docker-compose
1) https://docs.python.org/3/library/unittest.mock.html
1) https://docs.djangoproject.com/en/3.1/topics/db/transactions/
1) https://stackoverflow.com/a/57118885/2040370
1) https://docs.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax
1) https://stackoverflow.com/a/38260/2040370
1) https://realpython.com/caching-in-django-with-redis/
1) https://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint/
1) https://stackoverflow.com/questions/7382149/purpose-of-django-setting-secret-key
1) https://en.wikipedia.org/wiki/URL_shortening
