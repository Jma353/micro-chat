from . import * 
from helpers import http_resource, http_errors 

# Namespace 
namespace = '/chats'

# Schema generators 
chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)


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
	# Get the user from the request context 
	u = g.user 
	part = db.session.query(Participant).filter(Participant.user_id == u.id).first()
	# Get the chats associated with the user 
	chats = [] if not part else db.session.query(Chat).filter(Chat.id == part.chat_id).all() 
	chats_json = chats_schema.dump(chats)	
	print chats_json
	return http_resource(chats_json.data, "chats", True)




# Chat Creation Route 
@mchat.route(namespace + '/make_chat/<user_id>', methods=['POST'])
@req_session_code
def make_chat(user_id): 
	u = g.user 
	# TODO 
	return jsonify({ "to" : "do" })






















