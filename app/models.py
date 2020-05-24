print( "Hello, this is models.py and my name is", __name__ )

# ~ import flask_login
import datetime

from app import bazadanych

# ~ class User( flask_login.UserMixin, bazadanych.Model ):
class User( bazadanych.Model ):
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

  absences = bazadanych.relationship( "Absence", back_populates = "employee", lazy = 'immediate' )
  manager = bazadanych.relationship( "User", remote_side = [id], lazy = 'immediate' )
  reports = bazadanych.relationship( "User", lazy = 'immediate' )

  def __repr__( self ):
    return 'User {} <{}, {}, {}>'.format( self.username, self.name, self.surname, self.email )

class Absence( bazadanych.Model ):
  __tablename__ = "absences"
  
  id = bazadanych.Column( bazadanych.Integer, primary_key = True )
  userid = bazadanych.Column( bazadanych.Integer, bazadanych.ForeignKey( "users.id" ), index = True )
  absence_category_id = bazadanych.Column( bazadanych.Integer, bazadanych.ForeignKey( "absence_category.id" ), index = True )
  ts_absence_start = bazadanych.Column( bazadanych.DateTime, index = True )
  ts_absence_end = bazadanych.Column( bazadanych.DateTime )
  ts_requested = bazadanych.Column( bazadanych.DateTime, default = datetime.datetime.utcnow, index = True )
  description = bazadanych.Column( bazadanych.String( 500 ) )

  employee = bazadanych.relationship( "User", back_populates = "absences", lazy = 'immediate' )
  absence_category_label = bazadanych.relationship( "AbsenceCategory", back_populates = "absences", lazy = 'immediate' )
  
  def __repr__( self ):
    return 'Absence of {} categorised {} between {} and {}'.format( self.userid, self.absence_category_id, self.ts_absence_start, self.ts_absence_end )

  
class AbsenceCategory( bazadanych.Model ):
  __tablename__ = "absence_category"
  
  id = bazadanych.Column( bazadanych.Integer, primary_key = True )
  absence_category = bazadanych.Column( bazadanych.String( 50 ), index = True, unique = True )
  absence_category_description = bazadanych.Column( bazadanych.String( 200 ) )

  absences = bazadanych.relationship( "Absence", back_populates = "absence_category_label", lazy = 'immediate' )
  
  def __repr__( self ):
    return 'AbsenceCategory {} described {}'.format( self.absence_category, self.absence_category_description )
