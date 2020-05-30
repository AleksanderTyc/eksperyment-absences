print( "Hello, this is util BP email.py and my name is", __name__ )

import threading

import flask

from app import wysylacz


def sendEmailInContext( wiadomosc, aplikacja ):
# wiadomosc jest typu flask_mail.Message
# aplikacja jest flask.current_app._get_current_object()
  with aplikacja.app_context():
    wysylacz.send( wiadomosc )

def sendEmailAsynchro( wiadomosc ):
# Wymuszamy, aby thread otrzymal prawdziwy obiekt aplikacji:
  watek = threading.Thread( target = sendEmailInContext, args = (wiadomosc, flask.current_app._get_current_object()) )
  watek.start()
# To nie dziala, bo current_app nie jest obiektem aplikacji tylko jego proxy. Porownaj https://flask.palletsprojects.com/en/1.1.x/signals/#sending-signals  
  # ~ watek = threading.Thread( target = sendEmailInContext, args = (wiadomosc, flask.current_app) )
# General idea: obecnie wykonywana aplikacja, tj. application context, musi byc podana do background thread, bo wysylacz z niej korzysta,
# np do odczytu ustawien konfiguracyjnych. Dlatego current_app musi byc argumentem wywolania funkcji, ktora bedzie wykonywana przez thread.
# Nastepnie wewnatrz tej funkcji current_app bedzie uzyta do stworzenia context manager aplikacji i wewnatrz bedzie wywolane wysylanie email.
