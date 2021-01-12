rm db.sqlite3
./manage.py del_mig
py3clean .
./manage.py makemigrations
./manage.py migrate
