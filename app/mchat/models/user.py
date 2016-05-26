from . import * 


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
	name            = db.Column(db.String(128), nullable=False)
	
	# Email 
	email           = db.Column(db.String(128), nullable=False, unique=True)
	
	# Password Digest 
	password_digest = db.Column(db.String(192))



	def __init__(self, name, email, password):

		self.name     = name
		self.email    = email 

		self.password_digest = generate_password_hash(password)


	def __repr(self):
		return "<User %r>" % (self.name)





# Base Schema w/Session
class BaseSchema(ma.ModelSchema):
	class Meta: 
		sqla_session = Session



# User Schema serializer 
class UserSchema(BaseSchema):

	# B/c password is passed in 
	password = fields.String()

	class Meta(BaseSchema.Meta):
		model = User


	# Validations 

	# Email validations 
	@validates_schema
	def validate_email(self, data):
		email = data['email']
		# check format 
		email_format = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
		if not email_format.match(email):
			raise ValidationError("Please provide an email with correct format")

		# check unqiueness 
		users = db.session.query(User).filter(User.email == email)
		if len(users.all()) > 0: 
			raise ValidationError("Another user exists with this email address")


	# Name validations 
	@validates_schema
	def validate_name(self, data):
		name = data['name']
		if len(name) < 2: 
			raise ValidationError("Please enter a longer name")













