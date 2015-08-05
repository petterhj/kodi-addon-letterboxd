# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
# Database
FILE = 'sqlite:////home/petterhj/projects/xbmc-addon-letterboxd/plugin.video.letterboxd/sqlalchemy_example.db'

# Base
Base = declarative_base() 

# Model: Film
class Film(Base):
    __tablename__ = 'film'

    id = Column(Integer, primary_key=True)
    slug = Column(String(250))
    available_library = Boolean()
    available_stream = Boolean()
    last_check = DateTime()


# Class: Database
class Database():
	# Init
	def __init__(self):
		# Create database
		engine = create_engine(FILE)

		Base.metadata.create_all(engine)


db = Database()