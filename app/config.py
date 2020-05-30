print( "Hello, this is config.py and my name is", __name__ )

import os
# ~ import myloginpath

class Config():
  SECRET_KEY = os.environ.get( "SECRET_KEY" ) or "you-would-never-guess"

# Application name - useful in Blueprints where application name is required, e.g. sending emails.
  AT_APPLICATION_NAME = "Absences"

# SQLite
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' +os.path.join( os.path.abspath( os.path.dirname( __file__ ) ), 'app.db')
# MySQL specific
  # ~ DB_HOST = myloginpath.parse( "client" )[ "host" ] or "localhost"
  # ~ DB_USER = myloginpath.parse( "client" )[ "user" ] or "aleks"
  # ~ DB_PASSWD = myloginpath.parse( "client" )[ "password" ] 
  # ~ DB_SCHEMA = os.environ.get( "DB_SCHEMA" ) or "microblogg"
# myslqconnector published on MySQL webpage and officially documented by MySQL
  # ~ SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://" +DB_USER +":" +DB_PASSWD +"@" +DB_HOST +"/" +DB_SCHEMA

# PyMySQL, allegedly the best MySQL client for Python
  # ~ SQLALCHEMY_DATABASE_URI = "mysql://" +DB_USER +":" +DB_PASSWD +"@" +DB_HOST +"/" +DB_SCHEMA
  
# signal the application every time a change is about to be made in the database
  SQLALCHEMY_TRACK_MODIFICATIONS = False

# ~ migadu requirements for sending email
# ~ Outgoing Mail
# ~ Protocol	SMTP
# ~ Server	smtp.migadu.com
# ~ Port	465
# ~ Security	TLS
# ~ Authentication	Password
# ~ Username	admin@alekscorrugatedcontainers2005.cf
# ~ Password	(mailbox password)

# flask-mail configuration:
# ~ MAIL_SERVER : default ‘localhost’
# ~ MAIL_PORT : default 25
# ~ MAIL_USE_TLS : default False dotyczy autoryzacji StartTLS
# ~ MAIL_USE_SSL : default False dotyczy autoryzacji SSL/TLS (chyba nowsza)
# ~ MAIL_DEBUG : default app.debug
# ~ MAIL_USERNAME : default None
# ~ MAIL_PASSWORD : default None
# ~ MAIL_DEFAULT_SENDER : default None
# ~ MAIL_MAX_EMAILS : default None
# ~ MAIL_SUPPRESS_SEND : default app.testing
# ~ MAIL_ASCII_ATTACHMENTS : default False

  # ~ MAIL_SERVER = "localhost"
  MAIL_SERVER = "smtp.migadu.com"
  # ~ MAIL_PORT = "8025"
  MAIL_PORT = "465"
  MAIL_FROM = 'admin@alekscorrugatedcontainers2005.cf'
  MAIL_DEFAULT_SENDER = MAIL_FROM
  MAIL_USE_SSL = True
  MAIL_USERNAME = MAIL_FROM
  MAIL_PASSWORD = os.environ.get( "MAIL_PASSWORD" ) or "you-would-never-guess"
  
  # ~ MAIL_WATCHERS = ["watcher@localhost"]

# Pagination size
  AT_ITEMS_PER_PAGE = int( os.environ.get( key = "FLASK_ITEMS_PER_PAGE" ) or 5 )

# Bootstrap libraries served from local repository instead of internet
  BOOTSTRAP_SERVE_LOCAL = True
