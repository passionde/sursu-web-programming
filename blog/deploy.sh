git clone https://github.com/passionde/sursu-web-programming.git
cp -r sursu-web-programming/blog/ .
cd blog/
pip install -r requirements.txt
python3 manage.py migrate