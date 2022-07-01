# GoCardless sample application

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/CarbonWay/collector.git
$ cd collector-main
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv env
$ source env/bin/activate or env/Scripts/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd collector
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/admin/`.