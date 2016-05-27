from . import * 
from app.mchat.models.user import * 

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

	user_id = field_for(Participant, 'user_id', dump_only=False)
	chat_id = field_for(Participant, 'chat_id', dump_only=False)

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


	@post_dump 
	def add_user(self, item):
		user_id = int(item['user_id'])
		item.pop('user_id', None) # Get rid of this
		user = db.session.query(User).filter(User.id == user_id).first() 
		user_json = UserSchema(exclude=('password_digest',)).dump(user).data
		item['user'] = user_json
		return item







