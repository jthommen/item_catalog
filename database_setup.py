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

# Declares a base class our custom classes will inherit from
Base = declarative_base()


## CLASSES
# Correspond with tables to be created in db
class User(Base):
     ## TABLES
    __tablename__ = 'user'

    ## MAPPER for columns
    name = Column(
        String(80),
        # Meaning is needed to create new instance/row
        nullable = False)

    id = Column(
        Integer,
        primary_key = True)

    picture = Column(String(250))

    email = Column(
        String(250),
        nullable = False)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name' : self.name,
            'id' : self.id,
            'picture': self.picture,
            'email': self.email
        }


class Restaurant(Base):
    ## TABLES
    __tablename__ = 'restaurant'

    ## MAPPER for columns
    name = Column(
        String(80),
        # Meaning is needed to create new instance/row
        nullable = False
        )

    id = Column(
        Integer,
        primary_key = True)

    author_id = Column(
        Integer,
        ForeignKey('user.id')
        )

    author = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name' : self.name,
            'id' : self.id,
            'author_id': self.author_id
        }


class MenuItem(Base):
    ## TABLES
    __tablename__ = 'menu_item'

    ## MAPPER for columns
    name = Column(
        String(80),
        nullable = False)

    id = Column(
        Integer,
        primary_key = True)

    course = Column(
        String(250)
        )

    description = Column(
        String(250)
        )

    price = Column(
        String(8)
        )

    restaurant_id = Column(
        Integer,
        ForeignKey('restaurant.id')
        )

    author_id = Column(
        Integer,
        ForeignKey('user.id')
        )

    # Specifies relationships to other classes
    restaurant = relationship(Restaurant)
    author = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'price' : self.price,
            'course' : self.course,
            'author_id': self.author_id
        }


## ENDING configuration
###### insert at end of file ######
engine = create_engine(
    'sqlite:///restaurantmenuwithusers.db')

# Enters data specified into db
Base.metadata.create_all(engine)
