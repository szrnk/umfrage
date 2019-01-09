export DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5432/umfrage
python manage.py migrate


zappa deploy dev

zappa update

zappa manage dev sqlcreate

zappa manage dev migrate
  
zappa manage dev create_admin_user <UNAME> <EMAIL> <PASS>

zappa manage dev "collectstatic --noinput"


