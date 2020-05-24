print( "Hello, this is __init__.py and my name is", __name__ )

import flask
import flask_sqlalchemy
import flask_migrate

from app import config

bazadanych = flask_sqlalchemy.SQLAlchemy()
migracje = flask_migrate.Migrate()

def create_app( config_class = config.Config ):
  lc_app = flask.Flask( __name__ )
  lc_app.config.from_object( config_class )
  
  bazadanych.init_app( lc_app )
  migracje.init_app( lc_app, bazadanych )
  
  return lc_app

from app import models
