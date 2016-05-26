# Import flask deps
from flask import Blueprint, request, render_template, \
	flash, g, session, redirect, url_for, jsonify

# Import for pass / encryption 
from werkzeug import check_password_hash, generate_password_hash 

# Import the db object from main app module
from app import db 

# Import module models 
from app.mchat.models import * 

# JWT 
import jwt 

# Marshmallow 
from marshmallow import ValidationError

# Define a Blueprint for this module (mchat)
mchat= Blueprint('mchat', __name__, url_prefix='/mchat')

# Import socketio for socket creation in this module 
from app import socketio



def http_json(result, bool):
	result.update({ "success": bool })
	return jsonify(result)


def http_resource(result, name):
	resp = { "data": { name : result.data }}
	return http_json(resp, True)

def http_errors(result): 
	errors = { "data" : { "errors" : result.errors["_schema"] }}
	return http_json(errors, False)


# Route + accepted methods 
@mchat.route('/signup/', methods=['GET', 'POST'])
def signup(): 
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
			result = UserSchema(exclude=("password",)).dump(result.data)
			return http_resource(result, "user")



# Socket testing 
@socketio.on('connect', namespace='/test')
def ws_conn():
	socketio.emit('msg', { 'lol' : 'you are connected, DAMNNN DANIEL' }, namespace='/test')



# Not necessary for now 
"""
@socketio.on('disconnect', namespace='/test')
def ws_disconn(): 
	socketio.emit('msg', { 'lol' : 'someone disconnected' }, namespace='/test')
"""




@socketio.on('chat', namespace='/test')
def chat(chat): 
	socketio.emit('chat', { 'lol' : chat }, namespace='/test')






