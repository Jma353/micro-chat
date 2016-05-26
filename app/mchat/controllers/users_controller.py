from . import * 
# Returning based on errors
from helpers import http_resource, http_errors


# Namespace 
namespace = '/users'

# Sign Up Route 
@mchat.route(namespace + '/sign_up/', methods=['GET', 'POST'])
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
			result = UserSchema(exclude=("password_digest",)).dump(result.data)
			return http_resource(result, "user")



# Helper to auth on sign in 
def auth_pass(email, password): 
	user = db.session.query(User).filter(User.email == email).first()
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
@mchat.route(namespace + '/sign_in/', methods=['POST'])
def sign_in(): 
	# Get headers E and P (email and password)
	email = request.headers.get('E')
	password = request.headers.get('P')
	user_id, authenticated = auth_pass(email, password)
	if authenticated: 
		session = get_or_create_session(user_id)
		return jsonify(
			{ "success" : True, "data" : { 
				"session" : { 
					"session_code" : session.session_code 
					}
				}
			}
		)
	else: 
		resp = jsonify({ "success": False })
		resp.status_code = 401
		return resp

# Sign out (a lot of repeating, must refactor later)
@mchat.route(namespace + '/sign_out/', methods=['POST'])
def sign_out(): 
	session_code = request.headers.get('SessionCode')
	if not session_code: 
		resp = jsonify(
			{ "success" : False, "data" : {
				"errors" : ["No SessionCode header provided"]
				}
			}
		)
		resp.status_code = 401 
		return resp
	else: 
		sess = db.session.query(Session).filter(Session.session_code == session_code)
		if len(sess.all()) == 0:
			resp = jsonify(
				{ "success" : False, "data" : {
					"errors" : ["This session does not exist"]
					}
				}
			)
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











