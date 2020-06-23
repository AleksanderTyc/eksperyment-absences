print( "Hello, this is errors BP routes.py and my name is", __name__ )

import flask
import werkzeug.exceptions

from . import errors

from app import bazadanych

# ~ @errors.app_errorhandler( 401 ) - z BluePrint, TODO: sprawdzic ze skladnia werkzeug.exceptions.Unauthorized, zrodlo Mega Tutorial
@errors.app_errorhandler( werkzeug.exceptions.Unauthorized )
def route_error_401( blad ):
  print( "AT: werkzeug.exceptions.Unauthorized", blad.get_response() )
  return flask.render_template( "errors/e401.html", argblad = blad ), 401

@errors.app_errorhandler( werkzeug.exceptions.Forbidden )
def route_error_403( blad ):
  print( "AT: werkzeug.exceptions.Forbidden", blad.get_response() )
  return flask.render_template( "errors/e403.html", argblad = blad ), 403

@errors.app_errorhandler( werkzeug.exceptions.NotFound )
def route_error_404( blad ):
  print( "AT: werkzeug.exceptions.NotFound", blad.get_response() )
  return flask.render_template( "errors/e404.html", argblad = blad ), 404

@errors.app_errorhandler( werkzeug.exceptions.InternalServerError )
def route_error_500( blad ):
  print( "AT: werkzeug.exceptions.InternalServerError", blad.get_response() )
  bazadanych.session.rollback()
  return flask.render_template( "errors/e500.html", argblad = blad ), 500

