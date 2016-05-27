# Micro-Chat

### Flask with Sockets + Chat 


# DB Setup 
	
PostgreSQL is required.  Execute the following commands to create your DB: 

```bash
# Enter postgres command line interface 
$ psql 
# Create your database
CREATE DATABASE micro_chat; 
# Quit out 
\q 
```

To initialize migrations (only done once), make a migration, and apply that migration to the DB, run the following: 

```python
# Initialize migrations
python manage.py db init 
# Create a migration 
python manage.py db migrate
# Apply it to the DB
python manage.py db upgrade 
```


# Environment Variables 
Environment variables are necessary for the configuration of this framework.  The package [autoenv](https://github.com/kennethreitz/autoenv) allows for environment variable loading and virtual environment setup on cd'ing into the base directory of the project.  Follow the following command line arguments to install `autoenv`: 

```python
# Install the package from pip 
pip install autoenv
# Override cd by adding this to your .*rc file (* = bash, zsh, fish, etc.)
echo "source `which activate`" >> ~/.*rc 
# Reload your shell 
source ~/.*rc 
# Make a .env file to hold configuration steps 
touch .env 
```

In the `.env` file, one should place environment variables like the following: 
```python 
# Activate the virtualenv on cd
source venv/bin/activate 
# Set the environment type of the app (see config.py)
export APP_SETTINGS="config.DevelopmentConfig"
# Set the DB url to a local database for development 
export DATABASE_URL="postgresql://localhost/micro_chat"
```

# Making Endpoint Requests 
I've found that one of the easiest ways to make endpoint requests to a backend like this is to use the command line tool [httpie](https://github.com/jkbrzt/httpie).  All documentation regarding HTTP request types, headers, etc. can be found on that github page. 


# Endpoints 

## Users

### Index
GET `/mchat/users/index/` : Get a list of current users

### Sign Up 
POST `/mchat/users/sign_up/` : Sign up 
##### HTTP Request BODY
	{ name: "Joe", email: "joe@lol.com", password: "hello_world" }


### Sign In 
POST `/mchat/users/sign_in/` : Sign in 
##### HTTP Request HEADERS
	E:joe@lol.com
	P:hello_world


### Sign Out 
POST `/mchat/users/sign_out/` : Sign out
##### HTTP Request HEADERS 
	SessionCode:XYZ




















	
