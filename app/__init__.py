print( "Hello, this is __init__.py and my name is", __name__ )

import flask
import flask_sqlalchemy
import flask_migrate
import flask_bootstrap
import flask_login
import flask_mail
import flask_moment

import werkzeug

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
  zalogowany.login_view = "auth.route_signin"

# ~ Cannot be done as a blueprint, see https://stackoverflow.com/questions/28137451/blueprint-404-errorhandler-doesnt-activate-under-blueprints-url-prefix
  # ~ from app.errors import errors as bp_errors
  # ~ lc_app.register_blueprint( bp_errors )
  
  from app.util import utility as bp_utility
  lc_app.register_blueprint( bp_utility )
  
  from app.applogic import application_logic as bp_application_logic
  lc_app.register_blueprint( bp_application_logic )
  
  @lc_app.errorhandler( werkzeug.exceptions.Unauthorized )
  def route_error_401( blad ):
    print( "AT: werkzeug.exceptions.Unauthorized", blad.get_response() )
    return flask.render_template( "e401.html", argblad = blad ), 401

  @lc_app.errorhandler( werkzeug.exceptions.Forbidden )
  def route_error_403( blad ):
    print( "AT: werkzeug.exceptions.Forbidden", blad.get_response() )
    return flask.render_template( "e403.html", argblad = blad ), 403

  @lc_app.errorhandler( werkzeug.exceptions.NotFound )
  def route_error_404( blad ):
    print( "AT: werkzeug.exceptions.NotFound", blad.get_response() )
    return flask.render_template( "e404.html", argblad = blad ), 404

  @lc_app.errorhandler( werkzeug.exceptions.InternalServerError )
  def route_error_500( blad ):
    print( "AT: werkzeug.exceptions.InternalServerError", blad.get_response() )
    bazadanych.session.rollback()
    return flask.render_template( "e500.html", argblad = blad ), 500


  return lc_app

