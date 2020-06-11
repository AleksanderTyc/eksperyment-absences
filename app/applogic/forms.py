print( "Hello, this is applogic BP forms.py and my name is", __name__ )

import datetime

import flask_wtf
import wtforms

class UserProfileForm( flask_wtf.FlaskForm ):
  name = wtforms.StringField( "Name", validators = [wtforms.validators.InputRequired(), wtforms.validators.Length( min = 0, max = 64 )] )
  surname = wtforms.StringField( "Surname", validators = [wtforms.validators.InputRequired(), wtforms.validators.Length( min = 0, max = 64 )] )
  username = wtforms.StringField( "Username", validators = [wtforms.validators.InputRequired(), wtforms.validators.Length( min = 0, max = 64 )] )
  mgrusername = wtforms.StringField( "Manager username", validators = [wtforms.validators.InputRequired()] )
  role = wtforms.StringField( "Role", validators = [wtforms.validators.InputRequired()] )
  email = wtforms.StringField( "Email", validators = [wtforms.validators.InputRequired(), wtforms.validators.Email()] )
#  aboutme = wtforms.TextAreaField( "About", cols = 20, rows = 4, validators = [wtforms.validators.Length( min = 0, max = 100 )] )
  aboutme = wtforms.TextAreaField( "About", validators = [wtforms.validators.Length( min = 0, max = 100 )] )
  submit = wtforms.SubmitField( "Save" )

class UserAbsenceForm( flask_wtf.FlaskForm ):
  choice_category = wtforms.SelectField( "Absence category", validate_choice=False, coerce=int )
  ts_absence_start = wtforms.DateTimeField( "Absence start", validators = [wtforms.validators.InputRequired()] )
  ts_absence_end = wtforms.DateTimeField( "Absence end", validators = [wtforms.validators.InputRequired()] )
  description = wtforms.TextAreaField( "Description", validators = [wtforms.validators.Length( min = 0, max = 500 )] )
  submit = wtforms.SubmitField( "Save" )
