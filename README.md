# Micro-Chat

## Flask with Sockets + Chat 


## DB Setup 
	
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






	
