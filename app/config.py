print( "Hello, this is config.py and my name is", __name__ )

import os
# ~ import myloginpath

class Config():
  SECRET_KEY = os.environ.get( "SECRET_KEY" ) or "you-would-never-guess"
  
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

  # ~ MAIL_SERVER = "localhost"
  # ~ MAIL_PORT = "8025"
  # ~ MAIL_WATCHERS = ["watcher@localhost"]

# Pagination size
  FLASK_ITEMS_PER_PAGE = int( os.environ.get( key = "FLASK_ITEMS_PER_PAGE" ) or 3 )

# Bootstrap libraries served from local repository instead of internet
  BOOTSTRAP_SERVE_LOCAL = True
