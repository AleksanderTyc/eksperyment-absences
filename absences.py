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

# przykladowy odczyt z tablicy users:
# ~ import app
# ~ aplikacja = app.create_app()
# ~ with aplikacja.app_context():
# ~   uzytkownik = app.models.User.query.get( 1 )
# ~   uzytkownik = app.models.User.query.get( 123 )
  # ~ uzytkownik = app.models.User.query.get( 7 )
  # ~ uzytkownik.setPassword( "FF123" )
  # ~ app.bazadanych.session.commit()

# pip install email-validator flask-login flask-wtf bootstrap-flask
# Generator token (password reset email, API):
# pip install flask-mail pyjwt
# pip install Flask-Moment

# Po przeniesieniu aplikacja do __init__ (przygotowanie do factory):
# ~ with app.aplikacja.app_context():
  # ~ uzz = app.models.User.query.filter_by( username = "ZZ" ).first()
  # ~ uzz.setPassword( "ZZ123" )
  # ~ uzz = app.models.User.query.filter_by( username = "AA" ).first()
  # ~ uzz.setPassword( "AA123" )
  # ~ uzz = app.models.User.query.filter_by( username = "BB" ).first()
  # ~ uzz.setPassword( "BB123" )
  # ~ uzz = app.models.User.query.filter_by( username = "CC" ).first()
  # ~ uzz.setPassword( "CC123" )
  # ~ uzz = app.models.User.query.filter_by( username = "DD" ).first()
  # ~ uzz.setPassword( "DD123" )
  # ~ uzz = app.models.User.query.filter_by( username = "EE" ).first()
  # ~ uzz.setPassword( "EE123" )
  # ~ uzz = app.models.User.query.filter_by( username = "FF" ).first()
  # ~ uzz.setPassword( "FF123" )
# ~ with app.aplikacja.app_context():
  # ~ uzz = app.models.User.query.filter_by( username = "CC" ).first()
  # ~ uzz.verifyPassword( "CC123" )

# ~ with app.aplikacja.app_context():
  # ~ kateg = app.models.AbsenceCategory.query.get( 4 )
  # ~ print( kateg )
  # ~ kateg_abs = kateg.absences # Lista?
  # ~ print( kateg_abs )
  # ~ kabs0 = kateg_abs[0]
  # ~ print( kabs0.absence_category_label )
  # ~ kabs0emp = kabs0.employee
  # ~ print( kabs0emp )
  # ~ print( kabs0emp.absences )
  # ~ kabs0empm = kabs0emp.manager
  # ~ print( kabs0empm )
  # ~ print( kabs0empm.reports )

import app

aplikacja = app.create_app()
