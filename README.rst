===============
django-memo
===============

django-memo a simple/example app for shared notes
runs on django >= 1.3 rc 1 and requires django-gravatar

************
Installation
************

To install it, use pip::

    pip install -e git://github.com/tbarbugli/django_memo.git#egg=django_memo


*****
Usage
*****

    INSTALLED_APPS = (
        # ...         
        'memo',
        'gravatar',
    ) 

let django copies static files to your static folder

    ./manage.py collectstatic
