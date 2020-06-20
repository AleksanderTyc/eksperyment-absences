print( "Hello, this is models.py and my name is", __name__ )

import datetime

import flask
import flask_login
import jwt
import werkzeug.security

from app import bazadanych
from app import zalogowany

class User( flask_login.UserMixin, bazadanych.Model ):
# ~ class User( bazadanych.Model ):
  __tablename__ = "users" # Pozwala na zdefiniowanie innej niz domyslna "user" nazwy tabeli stowarzyszonej. Por. https://docs.sqlalchemy.org/en/13/orm/tutorial.html
  
  id = bazadanych.Column( bazadanych.Integer, primary_key = True )
  name = bazadanych.Column( bazadanych.String( 64 ), index = True )
  surname = bazadanych.Column( bazadanych.String( 64 ), index = True )
  mgrid = bazadanych.Column( bazadanych.Integer, bazadanych.ForeignKey( "users.id" ) )
  role = bazadanych.Column( bazadanych.String( 1 ), index = True )
  username = bazadanych.Column( bazadanych.String( 64 ), index = True, unique = True )
  password_hash = bazadanych.Column( bazadanych.String( 128 ) )
  email = bazadanych.Column( bazadanych.String( 128 ), index = True )
  lastseen = bazadanych.Column( bazadanych.DateTime, default = datetime.datetime.utcnow )
  aboutme = bazadanych.Column( bazadanych.String( 100 ) )

  # ~ absences = bazadanych.relationship( "Absence", back_populates = "employee", lazy = 'immediate' )
  absences = bazadanych.relationship( "Absence", back_populates = "employee" )

  manager = bazadanych.relationship( "User", remote_side = [id], lazy = 'immediate' )
  reports = bazadanych.relationship( "User", lazy = 'immediate' )

  def __repr__( self ):
    return 'User {} <{}, {}, {}>'.format( self.username, self.name, self.surname, self.email )

  def setPassword( self, new_password ):
    self.password_hash = werkzeug.security.generate_password_hash( new_password )
    bazadanych.session.commit()

  def verifyPassword( self, check_password ):
    return werkzeug.security.check_password_hash( self.password_hash, check_password )

  def createToken( self, purpose = 0, timeout = 300 ):
    """Create JWT token. Purpose: 1 - password reset email; 2 - reserved for future use (REST API). Timeout in seconds."""
    return jwt.encode(  { "uid":self.id, "purpose":purpose, "exp":datetime.datetime.utcnow()+datetime.timedelta( seconds = timeout ) },
                        flask.current_app.config.get( 'SECRET_KEY' ),
                        algorithm = 'HS256' ).decode( encoding = 'UTF-8' )

  def getUserFromToken( token, purpose = 0 ):
    try:
      token_decoded = jwt.decode( token.encode( encoding = "UTF-8" ), flask.current_app.config.get( 'SECRET_KEY' ), algorithm = 'HS256' )
    except:
      token_decoded = None
    if token_decoded is None:
      return None
    if purpose != token_decoded[ 'purpose' ]:
      return None
    return token_decoded[ 'uid' ]

#  def updateLastSeen( self, argts = datetime.datetime.utcnow() ):
# utcnow jest wykonywana tylko raz, podczas rejestracji funkcji (czyli ladowania modulu) i nigdy potem.
  def updateLastSeen( self, argts = None ):
    self.lastseen = datetime.datetime.utcnow() if argts is None else argts

  def returnOwnAbsences( self ):
    return Absence.query.filter_by( userid = self.id )
    # ~ return Absence.query.filter_by( userid = self.id ).order_by( Absence.ts_absence_start.desc() )
  
  def returnAbsences( self, ref_user ):
    if ref_user is None:
      # ~ zwroc team members absences
      return Absence.query.filter( Absence.userid.in_ ([ czlonek.id for czlonek in self.reports ]) )
    else:
      # ~ zwroc absences uzytkownika ref_user
      return Absence.query.filter_by( userid = ref_user.id )


class Absence( bazadanych.Model ):
  __tablename__ = "absences"
  
  id = bazadanych.Column( bazadanych.Integer, primary_key = True )
  userid = bazadanych.Column( bazadanych.Integer, bazadanych.ForeignKey( "users.id" ), index = True )
  absence_category_id = bazadanych.Column( bazadanych.Integer, bazadanych.ForeignKey( "absence_category.id" ), index = True )
  ts_absence_start = bazadanych.Column( bazadanych.DateTime, index = True )
  ts_absence_end = bazadanych.Column( bazadanych.DateTime )
  ts_requested = bazadanych.Column( bazadanych.DateTime, default = datetime.datetime.utcnow, index = True )
  description = bazadanych.Column( bazadanych.String( 500 ) )

  # ~ employee = bazadanych.relationship( "User", back_populates = "absences", lazy = 'immediate' )
  employee = bazadanych.relationship( "User", back_populates = "absences" )
  
  # ~ absence_category_label = bazadanych.relationship( "AbsenceCategory", back_populates = "absences", lazy = 'immediate' )
  absence_category_label = bazadanych.relationship( "AbsenceCategory", back_populates = "absences" )
  
  def __repr__( self ):
    return 'Absence of {} categorised {} between {} and {}'.format( self.userid, self.absence_category_id, self.ts_absence_start, self.ts_absence_end )

  def getSortingArgument( sortowanie_kolumna, sortowanie_porzadek):
    lc_slownik_pol = {
      "absence_category_id":[Absence.absence_category_id, Absence.absence_category_id.desc()],
      "ts_absence_start":[Absence.ts_absence_start, Absence.ts_absence_start.desc()],
      "ts_absence_end":[Absence.ts_absence_end, Absence.ts_absence_end.desc()],
      "ts_requested":[Absence.ts_requested, Absence.ts_requested.desc()],
      "description":[Absence.description, Absence.description.desc()]}
    return lc_slownik_pol.get( sortowanie_kolumna )[ sortowanie_porzadek ]

  
class AbsenceCategory( bazadanych.Model ):
  __tablename__ = "absence_category"
  
  id = bazadanych.Column( bazadanych.Integer, primary_key = True )
  absence_category = bazadanych.Column( bazadanych.String( 50 ), index = True, unique = True )
  absence_category_description = bazadanych.Column( bazadanych.String( 200 ) )

  # ~ absences = bazadanych.relationship( "Absence", back_populates = "absence_category_label", lazy = 'immediate' )
  absences = bazadanych.relationship( "Absence", back_populates = "absence_category_label" )
  
  def __repr__( self ):
    return 'AbsenceCategory {} described {}'.format( self.absence_category, self.absence_category_description )

@zalogowany.user_loader
def load_user( strid ):
  return User.query.get( int( strid ) )
