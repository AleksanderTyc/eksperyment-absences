print( "Hello, this is auth BP forms.py and my name is", __name__ )

import flask_wtf
import wtforms

class SigninForm( flask_wtf.FlaskForm ):
  username = wtforms.StringField( "Username", validators = [wtforms.validators.InputRequired()] )
  password = wtforms.PasswordField( "Password", validators = [wtforms.validators.InputRequired()] )
  submit = wtforms.SubmitField( "Log In" )

class PasswordResetRequestForm( flask_wtf.FlaskForm ):
  username = wtforms.StringField( "Username", validators = [wtforms.validators.InputRequired()] )
  email = wtforms.StringField( "Email", validators = [wtforms.validators.InputRequired(), wtforms.validators.Email()] )
  submit = wtforms.SubmitField( "Submit" )
  
class PasswordResetExecuteForm( flask_wtf.FlaskForm ):
  password = wtforms.PasswordField( "New password", validators = [wtforms.validators.InputRequired()] )
  password_re = wtforms.PasswordField( "Retype new password", validators = [wtforms.validators.EqualTo("password", message="Passwords must match")] )
  submit = wtforms.SubmitField( "Submit" )
  
class PasswordChangeForm( flask_wtf.FlaskForm ):
  password_old = wtforms.PasswordField( "Current password", validators = [wtforms.validators.InputRequired()] )
  password_new = wtforms.PasswordField( "New password", validators = [wtforms.validators.InputRequired()] )
  password_re = wtforms.PasswordField( "Retype new password", validators = [wtforms.validators.EqualTo("password_new", message="Passwords must match")] )
  submit = wtforms.SubmitField( "Set new password" )

