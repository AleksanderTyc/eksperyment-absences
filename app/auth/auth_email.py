print( "Hello, this is auth BP auth_email.py and my name is", __name__ )

import threading

import flask
import flask_mail

from app import wysylacz

# ~ import email.message
# ~ import email.utils
# ~ import smtplib

def wyslijWiadomosc( wiadomosc, aplikacja ):
  with aplikacja.app_context():
    wysylacz.send( wiadomosc )
  
def send_password_reset_link( uzytkownik ):
  pwr_link = flask.url_for( 'auth.route_password_reset_execute', _external = True, token = uzytkownik.createToken( purpose = 1 ) )
  print( pwr_link )
  wiadomosc = flask_mail.Message(
    subject = flask.current_app.config.get( 'AT_APPLICATION_NAME' ) +' - password reset',
    recipients = [uzytkownik.email],
    body = flask.render_template( 'auth/password_reset_email.txt', password_reset_link = pwr_link ),
    html = flask.render_template( 'auth/password_reset_email.html', password_reset_link = pwr_link )
# ~ ,sender – email sender address, or MAIL_DEFAULT_SENDER by default
    )
  # ~ wiadomosc[ 'From' ] = flask.current_app.config.get( 'MAIL_FROM' )
  # ~ wiadomosc[ 'To' ] = 
  # ~ wiadomosc[ 'Date' ] = email.utils.localtime()
  # ~ wiadomosc.set_content(  )
  # ~ wiadomosc.add_alternative(  )
  # ~ print( flask.render_template( 'auth/password_reset_email.txt', password_reset_link = pwr_link ) )

# To nie dziala, bo current_app nie jest obiektem aplikacji tylko jego proxy. Porownaj https://flask.palletsprojects.com/en/1.1.x/signals/#sending-signals  
  # ~ watek = threading.Thread( target = wyslijWiadomosc, args = (wiadomosc, flask.current_app) )
# Wymuszamy, aby thread otrzymal prawdziwy obiekt aplikacji:
  watek = threading.Thread( target = wyslijWiadomosc, args = (wiadomosc, flask.current_app._get_current_object()) )
  watek.start()
# General idea: obecnie wykonywana aplikacja, tj. application context, musi byc podana do background thread, bo wysylacz z niej korzysta,
# np do odczytu ustawien konfiguracyjnych. Dlatego current_app musi byc argumentem wywolania funkcji, ktora bedzie wykonywana przez thread.
# Nastepnie wewnatrz tej funkcji current_app bedzie uzyta do stworzenia context manager aplikacji i wewnatrz bedzie wywolane wysylanie email.
