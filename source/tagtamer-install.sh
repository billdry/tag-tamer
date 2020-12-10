#!/bin/bash

# Install rpms
yum update -y
yum install -y python3 python3-pip dos2unix yum-utils
amazon-linux-extras install nginx1 -y

# Install Python modules
mkdir -p /home/ec2-user/tag-tamer/prod
chown -R ec2-user:ec2-user /home/ec2-user/tag-tamer
#pip3 install boto3 botocore flask flask-WTF gunicorn Flask_jwt_Extended flask_login
#pip3 install /var/tmp/tagtamer/source/Flask-AWSCognito
su - ec2-user -c "python3 -m venv /home/ec2-user/tag-tamer/prod;source /home/ec2-user/tag-tamer/prod/bin/activate; pip3 install boto3 botocore flask flask-WTF gunicorn Flask_jwt_Extended flask_login /var/tmp/tagtamer/source/Flask-AWSCognito; deactivate"

# Copy code and config
cd /var/tmp/tagtamer/source
cp config/tag-tamer.conf /etc/nginx/conf.d
cp config/proxy_params /etc/nginx
cp config/ssl-redirect.conf  /etc/nginx/default.d/
cp config/tagtamer.service /etc/systemd/system
cp -pr code/* to /home/ec2-user/tag-tamer/

mkdir -p /home/ec2-user/tag-tamer/log
mkdir -p /var/log/tag-tamer
touch /var/log/tag-tamer/tag-tamer.err.log
touch /var/log/tag-tamer/tag-tamer.out.log

# Permissions
chown root:root /etc/nginx/conf.d/tag-tamer.conf /etc/nginx/proxy_params /etc/nginx/default.d/ssl-redirect.conf /etc/systemd/system/tagtamer.service
chown -R ec2-user:ec2-user /home/ec2-user/tag-tamer /var/log/tag-tamer

dos2unix /home/ec2-user/tag-tamer/*.py
dos2unix /home/ec2-user/tag-tamer/templates/*.html

# Fix IP in config
sed -i  "s/192.168.10.80/`hostname -i`/g" /etc/nginx/conf.d/tag-tamer.conf 

# SSL certificate creation
mkdir -p /etc/pki/nginx/private 
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/pki/nginx/private/nginx-selfsigned.key -out /etc/pki/nginx/nginx-selfsigned.crt -subj "/C=US/ST=NC/L=Raleigh/O=AWS/OU=TAM/CN=tagtamer.amazon.com"
openssl dhparam -out /etc/pki/nginx/dhparam.pem 2048

# Enable and start services
systemctl  enable tagtamer.service; systemctl  start tagtamer.service
systemctl enable nginx; systemctl start nginx