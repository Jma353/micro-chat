from . import * 
from app.mchat.models.user import UserSchema

# Message model 
class Message(Base):
	
	# Table name 
	__tablename__ = "messages"
	
	# Text of the message
	text          = db.Column(db.String(196), nullable=False)
	
	# Foreign key to sending user
	sender_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
	
	# Foreign key to chat 
	chat_id       = db.Column(db.Integer, db.ForeignKey('chats.id'))

	def __init__(self, text, sender_id, chat_id): 

		self.text = text 
		self.sender_id = sender_id
		self.chat_id = chat_id

	def __repr__(self):
		rep = "<Message %r>" % self.id


# Message schema 
class MessageSchema(BaseSchema):

	# Nested user in the JSON 
	user = fields.Nested(UserSchema, only=["name"])

	class Meta(BaseSchema.Meta):
		model = Message

	# Validations would go here 
	

