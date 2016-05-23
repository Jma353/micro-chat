import redis # Used as temp storage 
from flask import Flask, render_template # Flask dependencies 

# App 
app = Flask(__name__)

# DB 
db = redis.StrictRedis("localhost", 6379, 0)

@app.route('/')
def main():
	# Storage of information of REDIS DB 
	c = db.incr("counter")
	return render_template("main.html", counter=c)



if __name__ == "__main__":
	app.run(debug=True) 