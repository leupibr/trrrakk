# trrrakk ❤️
Application for tracking personal working hours.

## Installation

Prerequisite is Python 3.6 or newer and ``pip3``

First clone the project to your desired location

```bash
git clone git@github.com:leupibr/trrrakk.git trrrakk
cd trrrakk
```

Prepare the Python environment using ``pip3`` and ``pipenv``:

```bash
pip3 install pipenv
pipenv shell
pipenv install
```

Django requires a secret key for creating and accessing the database.
You can create secret by yourself or using a web tool like [Django Secret Key Generator](https://www.miniwebtool.com/django-secret-key-generator/)

```bash
export DJANGO_SECRET_KEY="<YOUR_KEY>"
```

Now create the database and a superuser:
```bash
./manage.py migrate
./manage.py createsuperuser
```

And finally run the application:
```bash
./manage.py runserver 127.0.0.1:8000
```

## Contributors

* [leupibr](http://github.com/leupibr)
* [tensorchief](https://github.com/tensorchief)
