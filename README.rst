django-mbaas
============

Description
-----------

Push notification service for iOS

Installation
------------

Prepare
~~~~~~~

.. code:: bash

    $ git clone https://github.com/nnsnodnb/django-mbaas.git
    $ cd django-mbaas/
    $ pip install -r requirements.txt
    $ cp mbaas/settings.py.sample mbaas/settings.py
    # Edit it if necessary (Email infomation etc.)
    $ python manage.py migrate
    $ python manage.py createsuperuer

In addition, add the following to the cron.

.. code:: crontab

    * * * * * python /path/to/manage.py startbatches
    */10 * * * * cd /path/to/django-mbaas && python manage.py dis_push

If you use this product on debug mode.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ python manage.py runserver
    # Example of command options under
    $ python manage.py runserver 0.0.0.0:8000

If you use this product on production mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To False DEBUG of in ``mbaas/setttings``

.. code:: bash

    $ gunicorn mbaas.wsgi:application
    # Example of command options under
    $ gunicorn mbaas.wsgi:application --bind 0.0.0.0:8000 -D

`LICENSE <LICENSE>`__
---------------------

Apache-2.0 License

Author
------

Yuya Oka (`nnsnodnb <https://twitter.com/nnsnodnb>`__)
