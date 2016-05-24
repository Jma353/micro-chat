# GEvent needed for sockets (must patch server before anything else)
from gevent import monkey 
monkey.patch_all() 

# Flask dependencies 
from flask import Flask, request, render_template, \
	flash, g, session, redirect, url_for 

# Password / encryption things 
from werkzeug import check_password_hash, generate_password_hash 

# SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy 

# SocketIO for Flask 
from flask.ext.socketio import SocketIO 

# Operating System 
import os 

# App 
app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# DB
db = SQLAlchemy(app) 

# Wrap app in socketIO 
socketio = SocketIO(app)

# Import our models 
from models import User

# Forms 
from forms import SignUp 




@app.route('/')
def main():
	return render_template("main.html")


@socketio.on("connect", namespace="/dd")
def ws_conn(): 
	c = 0 
	socketio.emit("msg", { "count": c }, namespace="/dd")



@socketio.on("disconnect", namespace="/dd")
def ws_disconn(): 
	c = 0 
	socketio.emit("msg", { "count": c }, namespace="/dd")




if __name__ == "__main__":
	socketio.run(app, host="0.0.0.0", debug=True, port=5000)  




