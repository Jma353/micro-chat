from app import db 
# This import was part of the Real Python tutorial, but possibly not needed for our purposes 
from sqlalchemy.dialects.postgresql import JSON


# Base db model (similar to ActiveModel)
class Base(db.Model): 

	# Makes this abstract so we aren't directly subclassing this relation 
	# If we were, we'd need a foreign key to this "Base" relation from the subclass 
	__abstract__ = True 
 

	id           = db.Column(db.Integer, primary_key=True)
	created_at   = db.Column(db.DateTime, default=db.func.current_timestamp())
	updated_at   = db.Column(db.DateTime, default=db.func.current_timestamp())



# User model of chat app; inherits Base above 
class User(Base): 

	# Table Name
	__tablename__ = "users"

	# Username
	name          = db.Column(db.String(128), nullable=False)

	# Email 
	email         = db.Column(db.String(128), nullable=False, unique=True)

	# Password (plain-text for now ... pending BCrypt integration)
	password      = db.Column(db.String(192), nullable=False)


	def __init__(self, name, email):

		self.name     = name
		self.email    = email 
		self.password = password


	def __repr(self):
		return "<User %r>" % (self.name)

















