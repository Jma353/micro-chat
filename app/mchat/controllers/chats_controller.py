from . import * 
from helpers import http_resource, http_errors 

# Namespace 
namespace = '/chats'

# Schema generators 
chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)
participant_schema = ParticipantSchema()
participants_schema = ParticipantSchema(many=True)


# session_code decorator function 
def req_session_code(view):
	@wraps(view)
	def decorator_function(*args, **kwargs):
		# Obtain header
		sess_code = request.headers.get("SessionCode")
		# If it's not there
		if not sess_code:
			errors = ["No SessionCode header provided"]
			resp = http_resource(errors, "errors", False)
			resp.status_code = 401
			return resp 

		# Try and find the session object
		sess = db.session.query(Session).filter(Session.session_code == sess_code)
		sess = sess.filter(Session.is_active == True)
		if len(sess.all()) == 0: 
			errors = ["No user exists with said session_code"]
			resp = http_resource(errors, "errors", False)
			resp.status_code = 401
			return resp

		# Find the user and set the request context (g)
		sess = sess.first() 
		user = db.session.query(User).filter(User.id == sess.user_id).first() 
		g.user = user 

		return view(*args, **kwargs)
	return decorator_function



# Chat Index Route 
@mchat.route(namespace + '/index', methods=['GET'])
@req_session_code
def chat_index(): 
	u = g.user

	# Get the user's participants
	parts = db.session.query(Participant).filter(Participant.user_id == u.id).all()
	# Get the chats associated with the user 
	chats = [] 
	for part in parts: 
		chat = db.session.query(Chat).filter(Chat.id == part.chat_id).first() 
		chats.append(chat)

	chats_json = chats_schema.dump(chats)	
	return http_resource(chats_json.data, "chats", True)




# Chat Creation Route 
@mchat.route(namespace + '/make_chat/<user_id>', methods=['POST'])
@req_session_code
def make_chat(user_id): 
	u = g.user
	
	# Check if the opposing user exists
	other_u = db.session.query(User).filter(User.id == user_id).first() 
	if not other_u:
		errors = ["No user exists with the specified user_id"]
		resp = http_resource(errors, "errors", False)
		resp.status_code = 404
		return resp

	# Get the name of the chat 
	chat_name = request.get_json()['chat_name']

	# If the other user exists, we can make our chat
	chat_json = { "name" : chat_name }
	chat = chat_schema.load(chat_json).data
	db.session.add(chat)
	db.session.commit() 
	print chat.id

	# Make our participants 
	self_json = { "user_id" : u.id, "chat_id" : chat.id }
	other_json = { "user_id" : other_u.id, "chat_id" : chat.id }

	self_obj = participant_schema.load(self_json).data
	other_obj = participant_schema.load(other_json).data

	db.session.add(self_obj)
	db.session.add(other_obj)
	db.session.commit() 

	chat_resp = chat_schema.dump(chat)
	return http_resource(chat_resp.data, "chat", True)






















