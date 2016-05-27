# Import OS
import os

# Import marshmallow functionality 
from marshmallow import fields, validates_schema, ValidationError, post_load

# Load these from the main app 
from app import db 
from app import ma 

# Regular expressions 
import re 

# Import for pass / encryption 
from werkzeug import check_password_hash, generate_password_hash 

# SQLAlchemy imports 
from sqlalchemy import orm, create_engine

# Establish db sessions for concurrency safety 
Session = orm.scoped_session(orm.sessionmaker())
engine = create_engine(os.environ['DATABASE_URL'])
Session.configure(bind=engine)




# Base db model (similar to ActiveModel)
class Base(db.Model): 

	# Makes this abstract so we aren't directly subclassing this relation 
	# If we were, we'd need a foreign key to this "Base" relation from the subclass 
	__abstract__ = True 
 

	id           = db.Column(db.Integer, primary_key=True)
	created_at   = db.Column(db.DateTime, default=db.func.current_timestamp())
	updated_at   = db.Column(db.DateTime, default=db.func.current_timestamp())




# Base Schema w/Session
class BaseSchema(ma.ModelSchema):
	class Meta: 
		sqla_session = Session

