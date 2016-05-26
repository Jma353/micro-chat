from . import * 
# Returning based on errors
from helpers import http_resource, http_errors


# Namespace 
namespace = '/users'

# Sign Up Route 
@mchat.route(namespace + '/signup/', methods=['GET', 'POST'])
def signup(): 
	if request.method == 'GET':
		return render_template('signup.html')

	if request.method == 'POST':
		json_data = request.get_json() 
		result = UserSchema().load(json_data)
		if result.errors: 
			print result.errors
			return http_errors(result)
		else: 
			db.session.add(result.data)
			db.session.commit() 
			result = UserSchema(exclude=("password_digest",)).dump(result.data)
			return http_resource(result, "user")


# Helper to auth on sign in 
def auth_pass(email, password): 
	user = db.session.query(User).filter(User.email==email).first()
	return check_password_hash(user.password_digest, password)

# Sign in 
@mchat.route(namespace + '/signin/', methods=['POST'])
def signin(): 
	# Get headers E and P (email and password)
	email = request.headers.get('E')
	password = request.headers.get('P')

	if auth_pass(email, password): 
		return jsonify({ "success": True })
	else: 
		resp = jsonify({ "success": False })
		resp.status_code = 401
		return resp





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











