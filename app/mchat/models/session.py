from . import *

# For key generation 
import hashlib

# Session model of chat app; inherits Base 
class Session(Base):

	# Table Name 
	__tablename__ = "sessions"
	
	# Foreign key to user 
	user_id       = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, index=True)
	
	# Session code 
	session_code  = db.Column(db.String(40))
	
	# Is active boolean field 
	is_active     = db.Column(db.Boolean)

	def __init__(self, user_id):

		self.user_id = user_id
		self.session_code = hashlib.sha1(os.urandom(64)).hexdigest()
		self.is_active = True 


	def __repr__(self):
		return "<Session for user %r>" % (self.user_id)

	# To update the session code on re-sign in 
	def update_session_code(): 
		self.session_code = hashlib.sha1(os.urandom(64)).hexdigest() 
		self.is_active = True 



# Session schema 
class SessionSchema(BaseSchema):

	class Meta(BaseSchema.Meta):
		model = Session 

	# Validations (all on validates_schema so we accumulate a list)

	# User_id validations 
	@validates_schema
	def validate_user_id(self, data):
		user_id = int(data['user_id'])

		# check that the user exists 
		users = db.session.query(User).filter(User.id == user_id)
		if len(users.all()) == 0: 
			raise ValidationError("No user exists with this ID")
















