web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn bk_engenharia.wsgi --bind 0.0.0.0:$PORT --log-file -
