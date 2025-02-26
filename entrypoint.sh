# #!/bin/sh

python manage.py migrate && \
python manage.py collectstatic --noinput && \
python manage.py create_superuser && \
python manage.py runserver 0.0.0.0:$BACKEND_PORT