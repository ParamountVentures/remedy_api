## imports
import os
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from config import db_settings
from orm.models import *

def db_connect(connection):
    """
    Connects to the database
    """
    url = URL(**db_settings.connections[connection])
    return create_engine(url, echo=db_settings.ECHO, client_encoding='utf8')

def create_tables(engine, base):
    """
    Creates or maps the tables in the database
    """
    base.metadata.create_all(engine)

def create_session(base, connection):
    """
    Returns a queryable session
    """
    engine = db_connect(connection)
    create_tables(engine, base)
    Session = scoped_session(sessionmaker(bind=engine))
    base.query = Session.query_property()
    return(Session())

