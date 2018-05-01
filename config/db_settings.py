import os
from sqlalchemy.engine.url import URL

### Try to get environment variables for connection
password = os.environ['POSTGRES_PASSWORD'] if "POSTGRES_PASSWORD" in os.environ else None
user = os.environ['POSTGRES_USER'] if "POSTGRES_USER" in os.environ else None
 
connections = {
            "local":{
                'drivername': 'postgres',
                'host': 'localhost',
                'port': '5432',
                'username': 'devonwalshe',
                'password': '',
                'database': 'remedy',
                'query': {'client_encoding': 'utf8'}}
            ,
            "remote":{
                'drivername': 'postgres',
                'host': 'devpgsql.postgres.database.azure.com',
                'port': '5432',
                'username': user,
                'password': password,
                'database': 'gcc-dev-foi',
                'query': {'client_encoding': 'utf8'}}
            ,
            "docker_local":{
                'drivername': 'postgres',
                'host': 'docker.for.mac.localhost',
                'port': '5432',
                'username': 'devonwalshe',
                'password': '',
                'database': 'remedy',
                'query': {'client_encoding': 'utf8'}}
 
}
 
### Set environment variables
ECHO = True
 
### App settings
 