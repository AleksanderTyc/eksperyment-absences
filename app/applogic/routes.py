print( "Hello, this is applogic BP routes.py and my name is", __name__ )

import flask
import flask_login

from app import bazadanych
# ~ from app import models

from . import application_logic
from . import forms

@application_logic.route( '/hello' )
def hello():
  uzytkownik = flask_login.current_user if flask_login.current_user.is_authenticated else None
  print( "W hello view function, flask_login.current_user:", flask_login.current_user, "uzytkownik:", uzytkownik )
  return flask.render_template( "applogic/index.html", title = "Main", user = uzytkownik )
  
@application_logic.route( '/edit_profile', methods = ['GET', 'POST'] )
@flask_login.login_required
def route_edit_own_profile():
  uzytkownik = flask_login.current_user
  formatka = forms.UserProfileForm()
  pola_do_edycji = ['name', 'surname', 'email', 'aboutme']
  formatka.username.validators = []
  formatka.mgrusername.validators = []
  formatka.role.validators = []
  if flask.request.method == "GET":
    formatka.name.data = uzytkownik.name
    formatka.surname.data = uzytkownik.surname
    formatka.username.data = uzytkownik.username
    formatka.mgrusername.data = uzytkownik.manager.username
    formatka.role.data = uzytkownik.role
    formatka.email.data = uzytkownik.email
    formatka.aboutme.data = uzytkownik.aboutme
  if formatka.validate_on_submit():
    uzytkownik.name = formatka.name.data
    uzytkownik.surname = formatka.surname.data
    uzytkownik.email = formatka.email.data
    uzytkownik.aboutme = formatka.aboutme.data
    bazadanych.session.commit()
    flask.flash( "User profile updated" )
    return flask.redirect( flask.url_for( "applogic.hello" ) )
  return flask.render_template( "applogic/edit_profile.html", title = "Edit own profile", form = formatka, editablefields = pola_do_edycji )
