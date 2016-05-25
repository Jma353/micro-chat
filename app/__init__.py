#### IMPORTS AND INITS #### 

# GEvent needed for sockets (must patch server before anything else)
from gevent import monkey 
monkey.patch_all() 

# Import flask and template operators
from flask import Flask, render_template 

# Import SQLAlchemy 
from flask.ext.sqlalchemy import SQLAlchemy 

# SocketIO for Flask 
from flask.ext.socketio import SocketIO 

# Marshmallow
from flask_marshmallow import Marshmallow 

# Init socketio 
socketio = SocketIO() 


#### APP CONSTRUCTION ####


# Define the WSGI application object 
app = Flask(__name__)

# Set debug option
app.debug = True


# Define the database object (imported by modules + controllers)
db = SQLAlchemy(app)
# Marshmallow 
ma = Marshmallow(app)


# Import module / component using blueprint var
from app.mchat.controllers import mchat as micro_chat

# Register blueprint 
app.register_blueprint(micro_chat)
# app.register_blueprint(another_blueprint)

socketio.init_app(app)





# HTTP error handling 
@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404


























