Hexagonal Architecture in Python using FastAPI and SqlAlchemy
=====================================================================

Installation and Usage
=======================

### Requirements

- Install Python 3.10, then

```bash
$ pip install virtualenv
$ sudo apt-get install libpq-dev python3.10-dev
$ git clone https://git.tipti.ec/tipti/self-services
$ cd self-services
```

### Create .env file

In the folder, there is a .env.example file, copy into .env file and change the values of variables

```bash
# Copy the .env.example
$ cp .env.example .env
```

Local setup (local db)
===============================

### To run

Create virtual environment and install requirements

```bash
$ python -m venv venv
$ source venv/bin/activate
$ chmod +x ./setup.sh
$ ./setup.sh # this execution upgrade pip and install requirements
```

Setup DB

```bash
# To create first tables
python manage.py db migrate
```

To make new migrations

```bash
$ python manage.py db makemigrations -m "first migrations"
```

To apply migrations

```bash
$ python manage.py db migrate
```

To run server

```bash
$ python manage.py server --host 0.0.0.0 --port 5000
```

To run the tests:

```bash
$ python manage.py check tests
```

To run the tests in watch mode:

```bash
$ python manage.py check tests --watch
```

Docker setup
=======================

### Running the database

To use a local mounted database:

```bash
# Run only the first time
$ mkdir docker/db
```

### Run docker compose

```bash
$ docker-compose -f docker/docker-compose.yml up -d
```

### Run migrations and migrate in Docker

To run migrations and migrate, first we need to enter the docker web console

```bash
$ docker-compose -f docker/docker-compose.yml exec web bash
```

Once inside, we run the migration commands

To make migrations

```bash
$ python manage.py db makemigrations -m "first migrations"
```

To migrate

```bash
$ python manage.py db migrate
```

To run tests

```bash
$ python manage.py check tests
```

To run the tests in watch mode:

```bash
$ python manage.py check tests --watch
```

Some interesting stuff
======================

https://stackoverflow.com/questions/72622714/how-to-handle-two-implementations-of-the-same-service