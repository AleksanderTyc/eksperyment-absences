print( "Hello, this is applogic BP routes.py and my name is", __name__ )

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
  return flask.render_template( "applogic/index.html", title = "Main", user = flask_login.current_user )


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
    return flask.redirect( flask.url_for( "applogic.route_headpage" ) )
  return flask.render_template( "applogic/edit_profile.html", title = "Edit own profile", form = formatka, editablefields = pola_do_edycji )


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
    flask.flash( "New post saved" )
    return flask.redirect( flask.url_for( "applogic.route_headpage" ) )
  return flask.render_template( "applogic/new_absence.html", title = "New absence", form = formatka )


@application_logic.route( '/show_own_absences' )
@flask_login.login_required
def route_show_own_absences():
  uzytkownik = flask_login.current_user
  nrstrony = flask.request.args.get( "page", default = 1, type = int )
  sortowanie_kolumna = flask.request.args.get( "sort_by", default = "ts_absence_start", type = str )
  sortowanie_porzadek = flask.request.args.get( "sort_order", default = 0, type = int )
  # ~ posty = uzytkownik.returnOwnPosts().all()
  print( "Proba odczytu absences dla userid", uzytkownik.id, type( uzytkownik.id ), "strona, kolumna, porzadek", nrstrony, sortowanie_kolumna, sortowanie_porzadek )
  # ~ nieobecnosci = uzytkownik.returnOwnAbsences().paginate( page = nrstrony, per_page = flask.current_app.config.get( "AT_ITEMS_PER_PAGE" ), error_out = False )
  nieobecnosci = uzytkownik.returnOwnAbsences()
  nieobecnosci = nieobecnosci.order_by( models.Absence.getSortingArgument( sortowanie_kolumna, sortowanie_porzadek ) ).paginate( page = nrstrony, per_page = flask.current_app.config.get( "AT_ITEMS_PER_PAGE" ), error_out = False )
  poprzednia = flask.url_for( "applogic.route_show_own_absences", page = nieobecnosci.prev_num ) if nieobecnosci.has_prev else None
  nastepna = flask.url_for( "applogic.route_show_own_absences", page = nieobecnosci.next_num ) if nieobecnosci.has_next else None
  return flask.render_template( "applogic/show_absences.html", title = "Show own absences", user = uzytkownik, absences_pagination = nieobecnosci, absences = nieobecnosci.items, page = nrstrony, sort_by = sortowanie_kolumna, sort_order = sortowanie_porzadek, ppage = poprzednia, npage = nastepna )

@application_logic.route( '/export_absences' )
def route_export_absences():
# ~ https://www.designedbyaturtle.co.uk/how-to-force-the-download-of-a-file-with-http-headers-and-php/
# ~ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
# ~ https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response
  nieobecnosci = flask_login.current_user.returnOwnAbsences().order_by( models.Absence.ts_absence_start ).all()
  odpowiedz = flask.make_response( flask.render_template( 'applogic/export_absences.csv', absences = nieobecnosci ) )
  odpowiedz.headers['Content-Type'] = 'application/octet-stream; charset=utf-8'
  odpowiedz.headers['Content-Disposition'] = 'attachment; filename="absences.csv"'
  return odpowiedz

