#!/bin/bash

# Stop script execution as soon as there are any errors
set -e

pwd
now=$(date +"%T")
echo "$now Running provision.sh"

# Instructions from: https://www.elastic.co/guide/en/elasticsearch/reference/1.4/setup-repositories.html
wget -qO - https://packages.elasticsearch.org/GPG-KEY-elasticsearch | sudo apt-key add -
echo 'deb http://packages.elasticsearch.org/elasticsearch/1.4/debian stable main' | sudo tee /etc/apt/sources.list.d/elasticsearch.list

# Install the packages we need
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  build-essential \
  gettext \
  git \
  libffi-dev \
  libssl-dev \
  openjdk-8-jre \
  postfix \
  python-dev \
  python-pip \
  python-virtualenv \
  rabbitmq-server \
  sqlite3 \
  yui-compressor

# Install ES seaprately as this old version's repository has signature
# failures that are not likely to be fixed as it is EOL.
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --allow-unauthenticated \
  elasticsearch

# Ensure ES is running
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch

# Set virtualenv directory and create it if needed.
virtualenv_dir="/home/vagrant/writeit-virtualenv"
[[ -d "$virtualenv_dir" ]] || virtualenv "$virtualenv_dir"

# Install the python requirements
# We specify a long timeout and use-mirrors to avoid
# errors like "SSLError: The read operation timed out"
cd /vagrant
"$virtualenv_dir/bin/pip" install -U pip
"$virtualenv_dir/bin/pip" install --timeout=120 --requirement /vagrant/requirements.txt

# Set up the Django database
"$virtualenv_dir/bin/python" /vagrant/manage.py syncdb --noinput
"$virtualenv_dir/bin/python" /vagrant/manage.py migrate

# Make sure message files for other languages are compiled:
"$virtualenv_dir/bin/python" /vagrant/manage.py compilemessages

motd_file="/etc/update-motd.d/99-writeit-instructions"

# Set shell login message
echo '#!/bin/sh
echo "-------------------------------------------------------
Welcome to the WriteIt vagrant machine

Add some seed data to your instance with:
  ./manage.py loaddata example_data.yaml

Run the web server with:
  ./manage.py runserver 0.0.0.0:8000

Then visit http://127.0.0.1.xip.io:8000/ to use WriteIt

Run a celery worker with:
  celery -A writeit worker

Run celery beat with:
  celery -A writeit beat

Run the tests with:
  ./manage.py test nuntium contactos mailit

-------------------------------------------------------"
' | sudo tee "$motd_file" > /dev/null
sudo chmod +x "$motd_file"

# Add cd /vagrant to ~/.bashrc
grep -qG "cd /vagrant" "$HOME/.bashrc" || echo "cd /vagrant" >> "$HOME/.bashrc"

# Activate virtualenv in ~/.bashrc
grep -qG "source $virtualenv_dir/bin/activate" "$HOME/.bashrc" || echo "source $virtualenv_dir/bin/activate" >> "$HOME/.bashrc"
