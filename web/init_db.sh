python manage.py collectstatic --noinput
chmod 755 -R /usr/src/app/static
python manage.py makemigrations --noinput
python manage.py migrate --noinput
