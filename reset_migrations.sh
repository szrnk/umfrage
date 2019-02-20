#!/usr/bin/env bash

find . -name \*.pyc -delete

find surveys -path "*/migrations/*.py" -not -name "__init__.py" -delete
find correspondents -path "*/migrations/*.py" -not -name "__init__.py" -delete

# in this one we are careful not to destroy migrations delivered from upstream, or
# we get a little issue, related to app blah, blah.
find core -path "*/migrations/*.py" -not -name "__init__.py" \
   -not -name "0001_initial.py" \
   -not -name "0002_alter_domain_unique.py" \
   -not -name "0003_set_site_domain_and_name.py" -delete

find core/users/migrations/*.py -not -name "__init__.py" -delete

# might as well rebuild too...
echo "Make migrations"
./manage.py makemigrations
echo "Migrate"
./manage.py migrate --settings=config.settings.local


