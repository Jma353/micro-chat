# Import OS
import os

# Import marshmallow functionality 
from marshmallow import fields, validates_schema, ValidationError, post_dump

from marshmallow_sqlalchemy import field_for

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
engine = create_engine(os.environ['DATABASE_URL'])




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
		Session = orm.scoped_session(orm.sessionmaker())
		Session.configure(bind=engine)
		sqla_session = Session

