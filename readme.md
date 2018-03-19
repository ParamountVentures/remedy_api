# Setup
Database configuration is in `./config/db_settings.py`

Set which database instance to use at the top of `app.py`

then: 

`$ docker run docker run --rm -d -p 5002:5000 remedy-api`

# Querying the API

Accepted params:
 - `start` date formatted as  `"%Y-%m-%d"`
 - `end` date formatted as  `"%Y-%m-%d"`
 - `per_page` integer, max 500, numbers over this amount will default to 500
 - `page` integer, offset for query

 