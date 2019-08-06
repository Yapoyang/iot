# iot
#installation
sudo apt-get update
sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
sudo pip3 install virtualenv
virtualenv iot_env
source iot_env/bin/activate
(iot_env)pip install django

#django setting
django-admin.py startproject iot
nano myproject/settings.py 
  -> change ALLOWED_HOSTS
  ->add at the bottom
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic

sudo ufw allow 8000

#apache2 setting *use config
sudo ufw delete allow 8000
sudo ufw allow 'Apache Full'
sudo apache2ctl configtest
sudo service apache2 restart

#python setting
install package
SQLAPchmy, mysqlclinet, requests, pandas, json
