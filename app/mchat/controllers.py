# Import flask deps
from flask import Blueprint, request, render_template, \
	flash, g, session, redirect, url_for

# Import for pass / encryption 
from werkzeug import check_password_hash, generate_password_hash 

# Import the db object from main app module
from app import db 

# Import module models 
from app.mchat.models import * 

# Define a Blueprint for this module (mchat)
mchat = Blueprint('mchat', __name__, url_prefix='/mchat')



# Route + accepted methods 
@mchat.route('/signup/', methods=['GET', 'POST'])
def signup(): 
	# Only respond to gets for now 
	if request.method == 'GET':
		return render_template('signup.html')

