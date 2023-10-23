git clone https://github.com/passionde/sursu-web-programming.git
cp -r sursu-web-programming/blog/ .
cd blog/
python3 manage.py migrate
python3 manage.py createsuperuser