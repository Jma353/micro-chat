# Import OS
import os

# Import marshmallow functionality 
from marshmallow import fields, validates_schema

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
