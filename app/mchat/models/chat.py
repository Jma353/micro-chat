from . import * 
from app.mchat.models.participant import Participant, ParticipantSchema

# For namespace generation 
import hashlib 

# Chat model: inherits Base 
class Chat(Base):

	# Table Name 
	__tablename__ = "chats"
	
	# Namespace 
	namespace     = db.Column(db.String(45))
	
	# Is active boolean field 
	is_active     = db.Column(db.Boolean)

	# Name
	name = db.Column(db.String(128)) 

	def __init__(self, name):

		self.name = name
		self.namespace = "chat-" + hashlib.sha1(os.urandom(64)).hexdigest() 
		self.is_active = True 

	def __repr__(self):
		return "<Chat %r>" % self.id


	def disable_chat(): 
		self.is_active = False 

# Chat schema 
class ChatSchema(BaseSchema):

	# To have access to id for foreign relations
	id = field_for(Chat, 'id', dump_only=False)

	class Meta(BaseSchema.Meta):
		model = Chat 


	# Add the the participants to the chat JSON 
	@post_dump
	def add_participants(self, item):
		chat_id = int(item['id'])
		parts = db.session.query(Participant).filter(Participant.chat_id == chat_id).all() 
		parts_json = ParticipantSchema(many=True).dump(parts).data
		item['participants'] = parts_json
		return item 








