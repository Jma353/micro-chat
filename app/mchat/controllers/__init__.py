# Import flask deps
from flask import request, render_template, \
	flash, g, session, redirect, url_for, jsonify, abort

# Import for pass / encryption 
from werkzeug import check_password_hash, generate_password_hash 

# Import the db object from main app module
from app import db 

# Marshmallow 
from marshmallow import ValidationError

# Import socketio for socket creation in this module 
from app import socketio

# Import module models 
from app.mchat.models.chat import * 
from app.mchat.models.message import * 
from app.mchat.models.participant import * 
from app.mchat.models.session import * 
from app.mchat.models.user import * 



# IMPORT THE BLUEPRINT APP OBJECT 
from app.mchat import mchat 