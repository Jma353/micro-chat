from . import * 


# User model of chat app; inherits Base 
class User(Base): 

	# Table Name
	__tablename__   = "users"
	
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


	def __repr__(self):
		return "<User %r>" % (self.name)




# User Schema serializer 
class UserSchema(BaseSchema):

	# To have access to id for foreign relations 
	id = field_for(User, 'id', dump_only=False)
	# B/c password is passed in 
	password = fields.String()

	class Meta(BaseSchema.Meta):
		model = User


	# Validations (all on validates_schema so we accumulate a list)

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













