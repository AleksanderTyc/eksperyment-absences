print( "Hello, this is routes.py and my name is", __name__ )

import flask
import flask_login

from app import aplikacja
from app import models
from app import forms

@aplikacja.route( '/hello' )
def hello():
  return flask.render_template( "index.html", title = "Main", user = flask_login.current_user )

@aplikacja.route( '/signin', methods = ['GET', 'POST'] )
def route_signin():
  if flask_login.current_user.is_authenticated:
    return flask.redirect( flask.url_for( "hello" ) )
  formatka = forms.SigninForm()
  if formatka.validate_on_submit():
    uzytkownik = models.User.query.filter_by( username = formatka.username.data ).first()
    if( uzytkownik == None ):
      flask.flash( "Invalid username or password" )
      return flask.redirect( flask.url_for( "route_signin" ) )
    flask_login.login_user( uzytkownik )
    return flask.redirect( flask.url_for( "hello" ) )
  return flask.render_template( "signin.html", title = "Log on", form = formatka )
  
@aplikacja.route( '/signout' )
def route_signout():
  if flask_login.current_user.is_authenticated:
    flask_login.logout_user()
  return flask.redirect( flask.url_for( "route_signin" ) )
