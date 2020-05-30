print( "Hello, this is auth BP auth_email.py and my name is", __name__ )

import flask
import flask_mail

from app import wysylacz

# ~ import email.message
# ~ import email.utils
# ~ import smtplib

def wyslijWiadomosc( wiadomosc ):
  # ~ wysylacz = smtplib.SMTP( host = flask.current_app.config.get( 'MAIL_SERVER' ), port = flask.current_app.config.get( 'MAIL_PORT' ) )
  # ~ wysylacz.send_message( wiadomosc )
  wysylacz.send( wiadomosc )
  # ~ wysylacz.quit()
  
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
  wyslijWiadomosc( wiadomosc )

