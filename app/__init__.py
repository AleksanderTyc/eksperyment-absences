print( "Hello, this is __init__.py and my name is", __name__ )

import flask
import flask_sqlalchemy
import flask_migrate
import flask_bootstrap
import flask_login

from app import config
# ~ from app import forms

bazadanych = flask_sqlalchemy.SQLAlchemy()
migracje = flask_migrate.Migrate()
stylista = flask_bootstrap.Bootstrap()
zalogowany = flask_login.LoginManager()

# ~ from app import models

aplikacja = flask.Flask( __name__ )
aplikacja.config.from_object( config.Config )

bazadanych.init_app( aplikacja )
migracje.init_app( aplikacja, bazadanych )
stylista.init_app( aplikacja )
zalogowany.init_app( aplikacja )

# ~ def create_app( config_class = config.Config ):
  # ~ lc_app = flask.Flask( __name__ )
  # ~ lc_app.config.from_object( config_class )
  
  # ~ bazadanych.init_app( lc_app )
  # ~ migracje.init_app( lc_app, bazadanych )
  # ~ stylista.init_app( lc_app )
  # ~ zalogowany.init_app( lc_app )
  # ~ return lc_app
  

from app import routes
