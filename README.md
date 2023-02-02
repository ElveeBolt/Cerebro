# 💎 Cerebro
[![Supported python versions](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/downloads/)
[![Supported elasticsearch versions](https://img.shields.io/badge/elasticsearch-8.6.1-yellow)](https://pypi.org/project/elasticsearch/)
[![Code style](https://img.shields.io/badge/code%20style-PEP8-blue)](https://peps.python.org/pep-0008/)

[![Django](https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=flat)](https://www.djangoproject.com/)

Cerebro - system of global search and identification of people, in particular mutants at your request.


## Install Elasticsearch

Before you start, you need to install elasticsearch on each node (separate server)
```bash
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.6.1-amd64.deb
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.6.1-amd64.deb.sha512
shasum -a 512 -c elasticsearch-8.6.1-amd64.deb.sha512 
sudo dpkg -i elasticsearch-8.6.1-amd64.deb
```
Save the password and user for further work with the node

Create directory to store elasticsearch indexes
```bash
sudo mkdir /mnt/data/elasticsearch
sudo chown -R elasticsearch:elasticsearch /mnt/data/elasticsearch
```

Get the fingerprint of the certificate and save it. 
This fingerprint is used to authorize third-party clients (Django, etc.)
```bash
sudo openssl x509 -fingerprint -sha256 -noout -in /etc/elasticsearch/certs/http_ca.crt
```

After installing elasticsearch, you need to edit the <code>elasticsearch.yml</code> settings file
```bash
sudo nano /etc/elasticsearch/elasticsearch.yml
```

```
cluster.name: cerebro-cluster
node.name: node-1
path.data: /mnt/data/elasticsearch
network.host: 192.168.20.125
http.port: 9200
cluster.initial_master_nodes: ["node-1"]
```

Run elasticsearch
```bash
sudo systemctl start elasticsearch.service
```

### Remove elasticsearch

```bash
sudo apt-get remove elasticsearch
sudo apt-get --purge autoremove elasticsearch
sudo rm -rf /var/lib/elasticsearch/
sudo rm -rf /etc/elasticsearch
sudo rm -rf /mnt/data/elasticsearch
```


## Install Gunicorn

```bash
pip install gunicorn
```

Create a <code>gunicorn.service</code> and <code>gunicorn.socket</code> files with content:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=root
WorkingDirectory=/mnt/data/cerebro/cerebro
ExecStart=/mnt/data/cerebro/venv/bin/gunicorn --workers 5 --bind unix:/run/gunicorn.sock cerebro.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

To check the gunicorn.service file for errors:
```bash
systemd-analyze verify gunicorn.service
```

If any changes are made to the <code>gunicorn.service</code> or <code>.socket</code> file, you must run the command:
```bash
systemctl daemon-reload
```

When changing the visual part of the project (html, javascript, etc.), you must run the command:
```bash
service gunicorn restart
```

## Install NGINX

To install NGINX please use the command:
```bash
sudo apt-get install nginx
```

Create <code>cerebro</code> file with content:
```bash
sudo nano  /etc/nginx/sites-available/cerebro
```

```
server {
    listen 80;
    server_name 192.168.20.125;

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

or if you have ssl certificate
```
server {
    server_name 192.168.20.125;
    listen 80;
    return 301 https://192.168.20.125$request_uri;
}

server {
    listen 443;
    ssl on;
    ssl_certificate /mnt/data/cert/cerebro-certificate.crt;
    ssl_certificate_key /mnt/data/cert/cerebro-certificate.key;
    server_name 192.168.20.125;

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    location /static/ {
        autoindex on;
        alias /mnt/data/cerebro/cerebro/static/;
    }
}
```

Create a symbolic link to a file in a directory
```bash
sudo ln -s /etc/nginx/sites-available/cerebro /etc/nginx/sites-enabled/
```

For any changes to the original file, run the command
```bash
sudo systemctl restart nginx
```

To check the NGINX configuration:
```bash
sudo nginx -t
```

## Create SSL / HTTPS Certificate

Create Certificate Authority
```bash
openssl req -x509 -sha256 -days 356 -nodes -newkey rsa:2048 -subj "/CN=10.0.0.2/C=US/L=San Fransisco" -keyout cerebro.key -out cerebro.crt 
```

Create the Server Private Key
```bash
openssl genrsa -out cerebro-certificate.key 2048
```

Create Certificate Signing Request Configuration
```bash
sudo nano csr.conf
```

```
[ req ]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[ dn ]
C = US
ST = California
L = San Fransisco
O = Cerebro
OU = Cerebro Dev
CN = 192.168.10.02

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = cerebro
IP.1 = 192.168.10.02
```

Generate Certificate Signing Request (CSR) Using Server Private Key
```bash
openssl req -new -key cerebro-certificate.key -out cerebro-certificate.csr -config csr.conf
```

Create a external file
```bash
sudo nano cert.conf
```

```
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = cerebro
IP.1 = 10.0.0.2
```

Generate SSL certificate With self signed CA
```bash
openssl x509 -req -in cerebro-certificate.csr -CA cerebro.crt -CAkey cerebro.key -CAcreateserial -out cerebro-certificate.crt -days 365 -sha256 -extfile cert.conf
```


## Installing Cerebro

Clone this repo and create virtual environment
```bash
git clone https://github.com/ElveeBolt/Cerebro.git
cd Cerebro

# For Linux/Ubuntu
python3 -m venv venv
source venv\bin\activate
pip install -r requirements.txt

# For Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Edit Django settings.py
```python
# Elastic settings
ELASTIC_CERT_FINGERPRINT = "09:CF:E0:A6:F0:EB:73:FD:4A:66:91:E8:64:A3:B7:6F:24:4C:9E:C9:ED:A2:6E:E8:5B:24:AF:0A:DC:2E:12:CE"
ELASTIC_USER = {
    'username': 'elastic',
    'password': 'CmXT6*4eT1Goy3Yv_-DJ'
}
ELASTIC_SERVER = 'https://127.0.0.1:9200'
```

Make migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

Create superuser
```bash
python manage.py createsuperuser
```

## Run Cerebro
```bash
python manage.py runserver
```

After starting you can go to http://127.0.0.1:8000/ and use Cerebro app

## Author
Developed and maintained by [ElveeBolt](https://github.com/ElveeBolt).

Thanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.