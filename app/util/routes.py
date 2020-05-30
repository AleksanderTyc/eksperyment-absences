print( "Hello, this is util BP routes.py and my name is", __name__ )

import datetime

import flask_login

from . import utility
from app import bazadanych

# Zauwaz roznice miedzy before_request i before_app_request - pierwsza dotyczy tylko tych requests, ktore odnosza sie do routes w tym BP; druga do wszystkich.
@utility.before_app_request
def route_update_lastseen():
  if flask_login.current_user.is_authenticated:
    flask_login.current_user.updateLastSeen()
    bazadanych.session.commit()
