export DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5432/umfrage
python manage.py migrate


zappa deploy dev

zappa update

zappa manage dev sqlcreate

zappa manage dev migrate
  
zappa manage dev create_admin_user <UNAME> <EMAIL> <PASS>

zappa manage dev "collectstatic --noinput"


## Run once after adding sortable Mixin
python manage.py reorder surveys.Option surveys.Question
zappa manage reorder surveys.Option surveys.Question

# References
https://en.wikipedia.org/wiki/Questionnaire
https://en.wikipedia.org/wiki/Questionnaire_construction
http://www.mrxplorer.com/index.php/2017/02/06/6-common-survey-writing-errors-to-avoid/
https://www.surveymonkey.com/curiosity/using-skip-logic-means-better-data-heres-proof/
https://getsitecontrol.com/howto/survey-widget/how-use-branching-logic-survey/
https://www.zoho.com/survey/help/branching-and-logic.html
https://help.surveygizmo.com/help/setup-question-logic
https://help.surveygizmo.com/help/set-up-skip-logic
