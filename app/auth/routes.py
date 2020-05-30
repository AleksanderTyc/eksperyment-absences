print( "Hello, this is auth BP routes.py and my name is", __name__ )

import flask
import flask_login

from . import auth
from . import forms
from . import auth_email

from app import models
from app import bazadanych

@auth.route( '/signin', methods = ['GET', 'POST'] )
def route_signin():
  if flask_login.current_user.is_authenticated:
    return flask.redirect( flask.url_for( "hello" ) )
  formatka = forms.SigninForm()
  if formatka.validate_on_submit():
    uzytkownik = models.User.query.filter_by( username = formatka.username.data ).first()
    if( uzytkownik == None ) or (False == uzytkownik.verifyPassword( formatka.password.data )):
      flask.flash( "Invalid username or password" )
      return flask.redirect( flask.url_for( "auth.route_signin" ) )
    flask_login.login_user( uzytkownik )
    return flask.redirect( flask.url_for( "hello" ) )
  return flask.render_template( "auth/signin.html", title = "Log on", form = formatka )
  
@auth.route( '/signout' )
def route_signout():
  if flask_login.current_user.is_authenticated:
    flask_login.logout_user()
  return flask.redirect( flask.url_for( "auth.route_signin" ) )

@auth.route( '/password_reset_request', methods = ['GET', 'POST'] )
def route_password_reset_request():
  formatka = forms.PasswordResetRequestForm()
  if formatka.validate_on_submit():
    uzytkownik = models.User.query.filter_by( username = formatka.username.data ).first()
    if (uzytkownik is not None) and (uzytkownik.email == formatka.email.data):
      print( "Wysylam email:" )
      auth_email.send_password_reset_link( uzytkownik )
    flask.flash( "Please check your email and use the link provided to reset the password." )
    return flask.redirect( flask.url_for( "auth.route_signin" ) )
  return flask.render_template( "auth/password_reset_request.html", title = "Password reset request", form = formatka )

@auth.route( '/password_reset_execute/<token>', methods = ['GET', 'POST'] )
def route_password_reset_execute( token = None ):
  print( "This is password reset execute with parameter:", token )
  
  if flask_login.current_user.is_authenticated:
    return flask.redirect( flask.url_for( "hello" ) )
  else:
    if token is None:
      flask.flash( "Please log in to access the app." )
      return flask.redirect( flask.url_for( "auth.route_signin" ) )
    else:
      uzytkownik_id = models.User.getUserFromToken( token, purpose = 1 )
      if uzytkownik_id is None:
        flask.flash( "Password reset link expired. Please try again." )
        return flask.redirect( flask.url_for( "auth.route_password_reset_request" ) )
      uzytkownik = models.User.query.get( uzytkownik_id )
      if uzytkownik is None:
        flask.flash( "Password reset link expired. Please try again." )
        return flask.redirect( flask.url_for( "auth.route_signin" ) )
      
  print( "This is password reset execute for user:", uzytkownik )
  formatka = forms.PasswordResetExecuteForm()
  if formatka.validate_on_submit():
    uzytkownik.setPassword( formatka.password.data )
    bazadanych.session.commit()
    flask.flash( "New password saved. Please log in." )
    return flask.redirect( flask.url_for( "auth.route_signin" ) )
  return flask.render_template( "auth/password_reset_execute.html", title = "Password reset execute", form = formatka, username = uzytkownik.username )

@auth.route( '/password_change', methods = ['GET', 'POST'] )
def route_password_change():
  if (False == flask_login.current_user.is_authenticated):
    flask.flash( "Please log in to access the app." )
    return flask.redirect( flask.url_for( "auth.route_signin" ) )
  uzytkownik = flask_login.current_user
  print( "This is password change for user:", uzytkownik )
  formatka = forms.PasswordChangeForm()
  if formatka.validate_on_submit():
    if uzytkownik.verifyPassword( formatka.password_old.data ):
      uzytkownik.setPassword( formatka.password_new.data )
      bazadanych.session.commit()
      flask.flash( "New password saved." )
    else:
      flask.flash( "Current password is invalid." )
    return flask.redirect( flask.url_for( "hello" ) )
  return flask.render_template( "auth/password_change.html", title = "Password change", form = formatka, username = uzytkownik.username )
