print( "Hello, this is util BP __init__.py and my name is", __name__ )

import flask

utility = flask.Blueprint( 'utility', __name__, template_folder = 'templates' )

# ~ from . import routes
