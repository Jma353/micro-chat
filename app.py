from gevent import monkey 
monkey.patch_all() 


from flask import Flask, render_template # Flask dependencies 
from flask.ext.sqlalchemy import SQLAlchemy # SQLAlchemy
from flask.ext.socketio import SocketIO # SocketIO for Flask 
import os # Operating System 


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