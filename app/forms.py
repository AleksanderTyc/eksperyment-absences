print( "Hello, this is forms.py and my name is", __name__ )

import flask_wtf
import wtforms

class SigninForm( flask_wtf.FlaskForm ):
  username = wtforms.StringField( "Username", validators = [wtforms.validators.InputRequired()] )
  password = wtforms.PasswordField( "Password", validators = [wtforms.validators.InputRequired()] )
  submit = wtforms.SubmitField( "Log In" )
