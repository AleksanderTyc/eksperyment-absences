print( "Hello, this is auth BP auth_email.py and my name is", __name__ )

import flask
import flask_mail

from app.util import email

  
def send_password_reset_link( uzytkownik ):
  pwr_link = flask.url_for( 'auth.route_password_reset_execute', _external = True, token = uzytkownik.createToken( purpose = 1 ) )
  wiadomosc = flask_mail.Message(
    subject = flask.current_app.config.get( 'AT_APPLICATION_NAME' ) +' - password reset',
    recipients = [uzytkownik.email],
    body = flask.render_template( 'auth/password_reset_email.txt', password_reset_link = pwr_link ),
    html = flask.render_template( 'auth/password_reset_email.html', password_reset_link = pwr_link )
    )
  email.sendEmailAsynchro( wiadomosc )
