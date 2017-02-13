## BEGINNING CONFIGURATION
# Import functions to manipulate python runtime environment
import sys

# Used to write mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# Used to write configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# Used to create foreignkey relationships
from sqlalchemy.orm import relationship

# Used in configuration code at end of file
from sqlalchemy import create_engine

Base = declarative_base()


## CLASSES
# Correspond with tables to be created in db
class Restaurant(Base):
    ## TABLES
    __tablename__ = 'some_table'
    return

class MenuItem(Base):
    ## TABLES
    __tablename__ = 'some_table'
    return


## ENDING configuration
###### insert at end of file ######
engine = create_engine(
    'sqlite:///restaurantmenu.db')

# Enters data specified into db
Base.metadata.create_all(engine)
