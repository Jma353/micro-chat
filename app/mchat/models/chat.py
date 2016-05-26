from . import * 

# For namespace generation 
import hashlib 

# Chat model: inherits Base 
class Chat(Base):

	# Table Name 
	__tablename__ = "chats"

	# Namespace 
	namespace = db.Column(db.String(45))

	# Is active boolean field 
	is_active = db.Column(db.Boolean)

	def __init__(self):

		self.namespace = "chat-" + hashlib.sha1(os.urandom(64)).hexdigest() 
		self.is_active = True 

	def __repr__(self):
		return "<Chat %r>" % self.id


	def disable_chat(): 
		self.is_active = False 

# Chat schema 
class ChatSchema(BaseSchema):

	# Will nest participants in here eventually 

	class Meta(BaseSchema.Meta):
		model = Chat 

	