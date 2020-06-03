print( "Hello, this is applogic BP __init__.py and my name is", __name__ )

import flask

application_logic = flask.Blueprint( 'applogic', __name__, template_folder = 'templates' )

from . import routes
