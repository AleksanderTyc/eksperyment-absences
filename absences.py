# Zanim to uruchomisz, pamietaj aby:
# [aleks@f31 ~]$ cd Archiwum/DataScientist/Python/PythonVirtEnvs/absences/
# Chyba niepotrzebne [aleks@f31 microblog]$ python -m venv venv
# [aleks@f31 microblog]$ . venv/bin/activate
# (venv) $ export FLASK_APP=absences.py

# Debug mode: flask restart when a source file is modified; error messages are shown on web page.
# (venv) $ export FLASK_DEBUG=1
# Status debug w aplikacji dostepny jest w aplikacja.debug: True - debug on; False - debug off
# Na innej konsoli wydac polecenie: python -m smtpd -n -c DebuggingServer localhost:8025

# pip install flask flask-sqlalchemy flask-migrate pymysql

# MySQL (i inne) database configuration and persistence when deploying on Docker: https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/linux-installation-docker.html

# Praca w CLI z fabryka aplikacji:
# ~ import app
# ~ aplikacja = app.create_app()
# ~ with aplikacja.app_context():
# przykladowy odczyt z tablicy AbsenceCategory
  # ~ kateg = app.models.AbsenceCategory.query.get( 1 )
  # ~ uzytk = app.models.User.query.filter_by( role = 'P' ).all()
  # ~ nieob = app.models.Absence.query.all()
  # ~ unieob = nieob[0].employee
  # ~ knieob = nieob[0].absence_category_label
  # ~ munieob = unieob.manager
# ~ kateg
# ~ unieob
# ~ knieob
# ~ munieob
# Dziala, ale wszystkie relationships musialy byc ustawione na lazy = 'immediate'. Nie wiem jakie to ma konsekwencje.
# Nie wiem czy jest to zwiazane z fabryka aplikacji, uruchamianiem w CLI czy z SQLite. Potrzebne sa eksperymenty.

# pip install email-validator flask-login flask-wtf bootstrap-flask

import app

# ~ aplikacja = app.create_app()
