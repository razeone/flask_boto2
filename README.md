# flask boto2

NOTE: This is deprecated

Is a conjunction work of Thomas Liakos and myself to have a simple web app for AWS monitoring and learn flask. 

It can be used for examples for the Flask framework with:

* SQLAlchemy integration (but just one model declared)
* AWS boto2 library for interaction with AWS cloud (just some methods implemented)
* Google Login with Flask-OAuth2
* Tasks caching using celery

This is an unfinished work released under GPLv2 and without any garanty.

## Installation

Redis must be running in localhost, and a previouslly configured database or SQLite for development.

### Edit `config.py`

* To enable the use of Google Login usinf Flask-Oath2
* The AWS keys using boto2
* Production database using PostgreSQL (SQLAlchemy)
* Redis and Celery

### Also edit `flask_boto2/app/mod_auth/user_controller.py`

In the line 46 you can set a domain name to allow only access in conjunction with Google Login, or disable it.

```bash
virtualenv env
source env/bin/activate
pip install -r flask_boto2/requirements/development.txt
export FLASK_ENVIRONMENT='development'
export $PYTHONPATH='/your-path-to-this-project/flask_boto2'
celery -A celery_worker worker -l info
python flask_boto2/run.py 
```

# Production?

For production edit the `flask_boto2/config.py` or set your environment variables for your database and Redis broker. But I don't recommend you use this in production.

# Total WIP 
