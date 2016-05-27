from . import * 
from helpers import http_resource, http_errors

# Namespace 
namespace = '/users'

# Schema generators 
user_schema = UserSchema(exclude=("password_digest",))
users_schema = UserSchema(many=True, exclude=("password_digest",))


# User Index Route 
@mchat.route(namespace + '/index', methods=['GET'])
def user_index(): 
	# Get all users 
	all_users = db.session.query(User).all() 
	result = users_schema.dump(all_users)
	resp = http_resource(result.data, "users", True)
	return resp



# Sign Up Route 
@mchat.route(namespace + '/sign_up', methods=['GET', 'POST'])
def sign_up(): 
	if request.method == 'GET':
		return render_template('signup.html')

	if request.method == 'POST':
		json_data = request.get_json() 
		result = UserSchema().load(json_data)
		if result.errors: 
			return http_errors(result)
		else: 
			db.session.add(result.data)
			db.session.commit() 
			result = user_schema.dump(result.data)
			return http_resource(result.data, "user", True)



# Helper to auth on sign in 
def auth_pass(email, password): 
	user = db.session.query(User).filter(User.email == email).first()
	if user == None: 
		return None, False
	user_id = user.id
	return user_id, check_password_hash(user.password_digest, password)


# Get or create a session (NOTE: different than user session)
def get_or_create_session(user_id): 

	sessions = db.session.query(Session).filter(Session.user_id == user_id)

	# Check to see if the session doesn't exist or is inactive 
	if len(sessions.all()) == 0: 
		session = Session(user_id=user_id)
		db.session.add(session)
		db.session.commit() 
		return session
	else: 
		session = sessions.first() 
		if not session.is_active: 
			session.update_session_code() 
			db.session.commit() 
		return session



# Sign in 
@mchat.route(namespace + '/sign_in', methods=['POST'])
def sign_in(): 
	# Get headers E and P (email and password)
	email = request.headers.get('E')
	password = request.headers.get('P')
	user_id, authenticated = auth_pass(email, password)
	if authenticated: 
		session = get_or_create_session(user_id)
		session_data = { "session_code" : session.session_code }
		return http_resource(session_data, "session", True)
	else: 
		errors = ["No email and password match these credentials"]
		resp = http_resource(errors, "errors", False)
		resp.status_code = 401
		return resp



# Sign out
@mchat.route(namespace + '/sign_out', methods=['POST'])
def sign_out(): 
	session_code = request.headers.get('SessionCode')
	if not session_code: 
		errors = ["No SessionCode header provided"] 
		resp = http_resource(errors, "errors", False)
		resp.status_code = 401 
		return resp
	else: 
		sess = db.session.query(Session).filter(Session.session_code == session_code)
		if len(sess.all()) == 0:
			errors = ["This session does not exist"] 
			resp = http_resource(errors, "errors", False)
			resp.status_code = 401
			return resp
		else: 
			sess = sess.first() 
			sess.is_active = False
			db.session.commit() 
			return jsonify({ "success" : True })




# Socket testing 
@socketio.on('connect', namespace='/test')
def ws_conn():
	socketio.emit('msg', { 'lol' : 'you are connected, DAMNNN DANIEL' }, namespace='/test')

@socketio.on('disconnect', namespace='/test')
def ws_disconn(): 
	socketio.emit('msg', { 'lol' : 'someone disconnected' }, namespace='/test')

@socketio.on('chat', namespace='/test')
def chat(chat): 
	socketio.emit('chat', { 'lol' : chat }, namespace='/test')











