# Import Form 
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements
from wtforms import TextField, PasswordField, BooleanField 

# Import Form validators
from wtforms.validators import Required, Email, EqualTo

# Sign Up Form 
class SignUp(Form):

	# Username field 
	username = TextField("Username", [
		Required(message="You must provide a username")
	])

	# Email field
	email = TextField("Email Address", [
		Email(), 
		Required(message="You must provide an email address")
	])

	# Password field
	password = PasswordField("Password", [
		Required(message="You must provide a password")
	])