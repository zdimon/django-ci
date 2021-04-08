## Continue Integration with Django.

System allows to create different environments for the developers.

Every environment includes separate subdomain and git branch.

It runs all needed prosess in supervisor for deploing project on subdomain.

It creates sobdomain whit nginx virtual hosts.

## Installation

    ./install

## Requirements

    sudo apt-get install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     supervisor redis-server libpq-dev postgresql


## Deploy

Rename configs
 
    cp ci-conf/django-ci-supervisor.__conf ci-conf/django-ci-supervisor.conf

Edit supervisor conf

    sudo nano /etc/supervisor/supervisor.conf

Add path to django-ci config and future environments configs.

    files = /etc/supervisor/conf.d/*.conf /home/zdimon/ssd/web/django-ci/ci/ci-conf/*.conf  /home/zdimon/ssd/web/django-ci/ci/env-conf/*.conf

Restart supervisor

    sudo service supervisor restart
