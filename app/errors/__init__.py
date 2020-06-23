print( "Hello, this is errors BP __init__.py and my name is", __name__ )

import flask

errors = flask.Blueprint( 'errors', __name__, template_folder = 'templates' )

from . import routes
