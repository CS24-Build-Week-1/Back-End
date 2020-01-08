web: gunicorn adv_project.wsgi:application --log-file -
release: python manage.py migrate
release: python manage.py create_rooms
