print( "Hello, this is __init__.py and my name is", __name__ )

import flask
import flask_sqlalchemy
import flask_migrate
import flask_bootstrap
import flask_login
import flask_mail
import flask_moment

from app import config
# ~ from app import forms

bazadanych = flask_sqlalchemy.SQLAlchemy()
migracje = flask_migrate.Migrate()
stylista = flask_bootstrap.Bootstrap()
zalogowany = flask_login.LoginManager()
wysylacz = flask_mail.Mail()
momencik = flask_moment.Moment()

# ~ from app import models

# ~ aplikacja = flask.Flask( __name__ )
# ~ aplikacja.config.from_object( config.Config )

# ~ bazadanych.init_app( aplikacja )
# ~ migracje.init_app( aplikacja, bazadanych )
# ~ stylista.init_app( aplikacja )
# ~ zalogowany.init_app( aplikacja )

# ~ from app.auth import auth as bp_auth
# ~ aplikacja.register_blueprint( bp_auth )

def create_app( config_class = config.Config ):
  lc_app = flask.Flask( __name__ )
  lc_app.config.from_object( config_class )
  
  bazadanych.init_app( lc_app )
  migracje.init_app( lc_app, bazadanych )
  stylista.init_app( lc_app )
  zalogowany.init_app( lc_app )
  wysylacz.init_app( lc_app )
  momencik.init_app( lc_app )
  
  from app.auth import auth as bp_auth
  lc_app.register_blueprint( bp_auth )

  from app.util import utility as bp_utility
  lc_app.register_blueprint( bp_utility )
  
  @lc_app.route( '/hello' )
  def hello():
    return flask.render_template( "index.html", title = "Main", user = flask_login.current_user )
    
  return lc_app
  

from app import routes
