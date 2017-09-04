import os.path

bind = 'unix://gunicorn_mbaas.sock'
daemon = True
pidfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gunicorn.pid')
reload = True
