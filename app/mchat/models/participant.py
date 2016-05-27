from . import * 
from app.mchat.models.user import UserSchema

# Participant model (linking users to chats)
class Participant(Base):
	
	# Table name
	__tablename__ = "participants"
	
	# Foreign key to user 
	user_id       = db.Column(db.Integer, db.ForeignKey('users.id'))
	
	# Foreign key to chat 
	chat_id       = db.Column(db.Integer, db.ForeignKey('chats.id'), index=True)

	def __init__(self, user_id, chat_id):

		self.user_id = user_id
		self.chat_id = chat_id

	def __repr__(self):
		rep = "<U: " + str(self.user_id) + ", C: " + str(self.chat_id) + ">"
		return rep



# Participant schema
class ParticipantSchema(BaseSchema):

	# Nest the user in the JSON 
	user = fields.Nested(UserSchema)

	class Meta(BaseSchema.Meta):
		model = Participant

	# Validates uniqueness of <user_id,chat_id> combo 
	@validates_schema
	def unique_user_chat(self, data):
		user_id = int(data['user_id'])
		chat_id = int(data['chat_id'])

		parts = db.session.query(Participant).filter(Participant.user_id == user_id)
		parts = parts.filter(Participant.chat_id == chat_id)
		if len(parts.all()) > 0: 
			raise ValidationError("You are already part of this chat")





