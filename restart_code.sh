echo "--------------create migration--------------"
python manage.py makemigrations
echo "--------------migration---------------------"
python manage.py migrate
echo "--------------restart server----------------"
python manage.py runserver