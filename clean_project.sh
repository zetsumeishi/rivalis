rm db.sqlite3
./manage.py del_mig
./manage.py clean_pyc
./manage.py makemigrations
./manage.py migrate
