print( "Hello, this is auth BP __init__.py and my name is", __name__ )

import flask

auth = flask.Blueprint( 'auth', __name__, template_folder = 'templates' )

from . import routes
