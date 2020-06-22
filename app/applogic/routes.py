print( "Hello, this is applogic BP routes.py and my name is", __name__ )

import datetime

import werkzeug
import flask
import flask_login

from app import bazadanych
from app import models

from . import application_logic
from . import forms


@application_logic.route( '/' )
@application_logic.route( '/index' )
@flask_login.login_required
def route_headpage():
  (nieobecnosci, uzytkownik) = flask_login.current_user.getRelevantAbsences( flask_login.current_user.username )
  nieobecnosci = nieobecnosci.order_by( models.Absence.getSortingArgument( "ts_absence_start", 1 ) ).paginate( page = 1, per_page = 3, error_out = False )
  return flask.render_template( "applogic/index.html", title = "Main", user = uzytkownik, absences = nieobecnosci.items )


@application_logic.route( '/zepsuj_edit_profile', methods = ['GET', 'POST'] )
@flask_login.login_required
def route_edit_own_profile():
  # ~ TODO:
    # ~ - manager field when showing CEO - done
    # ~ - manager field as choice when applicable
    # ~ - email validation - correct and unique
    # ~ - mgr options - user name validation - unique
    # ~ - mgr options - role as radio button
    # ~ - mgr options - role modification check - are you sure, only when downgrading, really
    # ~ - mgr options - mgr name modification check - are you sure, check for real modification
    # ~ - mgr options - editable fields when editing existing profile: email, role, mgr name
    # ~ - mgr options - editable fields when creating new user: name, surname, username, email, role, mgr name
    # ~ - mgr options - create new user: input profile details, validate, insert to DB, send email to the new user
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
    formatka.mgrusername.choices = [(kierownik.id, kierownik.username) for kierownik in models.User.query.filter_by( role = 'P' ).order_by( "username" )]
    formatka.mgrusername.data = uzytkownik.mgrid
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
    return flask.redirect( flask.url_for( "applogic.route_headpage" ) )
  return flask.render_template( "applogic/edit_profile.html", title = "Edit own profile", user = uzytkownik, form = formatka, editablefields = pola_do_edycji )


@application_logic.route( '/edit_profile/<nazwauzytkownika>', methods = ['GET', 'POST'] )
@flask_login.login_required
def route_edit_profile( nazwauzytkownika ):
  # ~ TODO:
    # ~ - manager field when showing CEO - done
    # ~ - manager field as choice when applicable
    # ~ - email validation - correct and unique
    # ~ - mgr options - user name validation - unique
    # ~ - mgr options - role as radio button
    # ~ - mgr options - role modification check - are you sure, only when downgrading, really
    # ~ - mgr options - mgr name modification check - are you sure, check for real modification
    # ~ - mgr options - editable fields when editing existing profile: email, role, mgr name
    # ~ - mgr options - editable fields when creating new user: name, surname, username, email, role, mgr name
    # ~ - mgr options - create new user: input profile details, validate, insert to DB, send email to the new user

  formatka = forms.UserProfileForm()
  if nazwauzytkownika == flask_login.current_user.username:
    uzytkownik = flask_login.current_user
    pola_do_edycji = ['name', 'surname', 'email', 'aboutme']
    formatka.mgrusername.choices = [(kierownik.id, kierownik.username) for kierownik in models.User.query.filter_by( role = 'P' ).order_by( "username" ) if kierownik.username != nazwauzytkownika]
  else:
    uzytkownik = flask_login.current_user.getTeamMember( nazwauzytkownika )
    pola_do_edycji = ['email', 'role', 'mgrusername']
    formatka.mgrusername.choices = [(kierownik.id, kierownik.username) for kierownik in models.User.query.filter_by( role = 'P' ).order_by( "username" )]
  formatka.name.data = uzytkownik.name
  formatka.surname.data = uzytkownik.surname
  formatka.username.data = uzytkownik.username
  formatka.mgrusername.data = uzytkownik.mgrid
  formatka.role.data = uzytkownik.role
  formatka.email.data = uzytkownik.email
  formatka.aboutme.data = uzytkownik.aboutme

  if flask.request.method == 'POST':
    for pole in flask.request.form.keys():
      if pole in pola_do_edycji:
        obiekt = getattr( formatka, pole )
        setattr( obiekt, 'data', int( flask.request.form.getlist( pole )[0] ) if pole == 'mgrusername' else flask.request.form.getlist( pole )[0] )
    
    if formatka.validate():
      uzytkownik.name = formatka.name.data
      uzytkownik.surname = formatka.surname.data
      # ~ uzytkownik.username = formatka.username.data
      if uzytkownik.role != formatka.role.data and uzytkownik.role == 'P':
        for pracownik in uzytkownik.reports:
          pracownik.mgrid = flask_login.current_user.id
      uzytkownik.mgrid = formatka.mgrusername.data
      uzytkownik.role = formatka.role.data
      uzytkownik.email = formatka.email.data
      uzytkownik.aboutme = formatka.aboutme.data
      bazadanych.session.commit()
      flask.flash( "User profile updated" )
      return flask.redirect( flask.url_for( "applogic.route_headpage" ) )
  return flask.render_template( "applogic/edit_profile.html", title = "Edit own profile", user = uzytkownik, form = formatka, editablefields = pola_do_edycji )


@application_logic.route( '/new_absence', methods = ['POST', 'GET'] )
@flask_login.login_required
def route_new_absence():
  print( "route_new_absence, method:", flask.request.method )
  formatka = forms.UserAbsenceForm()
  if flask.request.method == "GET":
    formatka.choice_category.choices = [(kategoria.id, kategoria.absence_category) for kategoria in models.AbsenceCategory.query.order_by( "id" )]
    formatka.choice_category.data = formatka.choice_category.choices[0][0]
  if formatka.validate_on_submit():
    print( "route_new_absence, validated", formatka )
    nowy_rekord = models.Absence()
    # ~ nowy_rekord.userid = flask_login.current_user.id
    nowy_rekord.absence_category_id = formatka.choice_category.data
    nowy_rekord.ts_absence_start = formatka.ts_absence_start.data
    nowy_rekord.ts_absence_end = formatka.ts_absence_end.data
    # ~ ts_requested = datetime.datetime.utcnow()
    nowy_rekord.description = formatka.description.data
    flask_login.current_user.absences.append( nowy_rekord )
    bazadanych.session.commit()
    flask.flash( "New absence saved" )
    return flask.redirect( flask.url_for( "applogic.route_headpage" ) )
  return flask.render_template( "applogic/new_absence.html", title = "New absence", form = formatka )


@application_logic.route( '/show_absences' )
@application_logic.route( '/show_absences/<nazwauzytkownika>' )
@flask_login.login_required
def route_show_absences( nazwauzytkownika = None ):
  # ~ uzytkownik = flask_login.current_user
  (nieobecnosci, uzytkownik) = flask_login.current_user.getRelevantAbsences( nazwauzytkownika )
  nrstrony = flask.request.args.get( "page", default = 1, type = int )
  sortowanie_kolumna = flask.request.args.get( "sort_by", default = "ts_absence_start", type = str )
  sortowanie_porzadek = flask.request.args.get( "sort_order", default = 1, type = int )
  nieobecnosci = nieobecnosci.order_by( models.Absence.getSortingArgument( sortowanie_kolumna, sortowanie_porzadek ) ).paginate( page = nrstrony, per_page = flask.current_app.config.get( "AT_ITEMS_PER_PAGE" ), error_out = False )
  # ~ posty = uzytkownik.returnOwnPosts().all()
  # ~ print( "Proba odczytu absences dla userid", uzytkownik.id, type( uzytkownik.id ), "strona, kolumna, porzadek", nrstrony, sortowanie_kolumna, sortowanie_porzadek )
  # ~ nieobecnosci = uzytkownik.returnOwnAbsences().paginate( page = nrstrony, per_page = flask.current_app.config.get( "AT_ITEMS_PER_PAGE" ), error_out = False )
  poprzednia = flask.url_for( "applogic.route_show_absences", page = nieobecnosci.prev_num ) if nieobecnosci.has_prev else None
  nastepna = flask.url_for( "applogic.route_show_absences", page = nieobecnosci.next_num ) if nieobecnosci.has_next else None
  return flask.render_template( "applogic/show_absences.html", title = "Show own absences", user = uzytkownik, absences_pagination = nieobecnosci, absences = nieobecnosci.items, page = nrstrony, sort_by = sortowanie_kolumna, sort_order = sortowanie_porzadek, ppage = poprzednia, npage = nastepna )


@application_logic.route( '/export_absences' )
@application_logic.route( '/export_absences/<nazwauzytkownika>' )
@flask_login.login_required
def route_export_absences( nazwauzytkownika = None ):
# ~ https://www.designedbyaturtle.co.uk/how-to-force-the-download-of-a-file-with-http-headers-and-php/
# ~ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
# ~ https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response
  (nieobecnosci, uzytkownik) = flask_login.current_user.getRelevantAbsences( nazwauzytkownika )
  nieobecnosci = nieobecnosci.order_by( models.Absence.ts_absence_start ).all()
  czyje = 'team' if nazwauzytkownika is None else ('own' if nazwauzytkownika == flask_login.current_user.username else nazwauzytkownika)
  contentDisposition = '"'.join( ['attachment; filename=', '_'.join( [ 'absences', flask_login.current_user.username, czyje, datetime.datetime.utcnow().strftime( "%Y%m%d%H%M" )] ) +'.csv', "'"] )
  odpowiedz = flask.make_response( flask.render_template( 'applogic/export_absences.csv', absences = nieobecnosci ) )
  odpowiedz.headers['Content-Type'] = 'application/octet-stream; charset=utf-8'
  odpowiedz.headers['Content-Disposition'] = 'attachment; filename="absences.csv"'
  odpowiedz.headers['Content-Disposition'] = contentDisposition
  return odpowiedz

