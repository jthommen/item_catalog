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
    id = Column(
        Integer,
        primary_key = True)

    name = Column(
        String(250),
        # Meaning is needed to create new instance/row
        nullable = False)

    email = Column(
        String(250),
        nullable = False)

    picture = Column(String(250))


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(
        Integer,
        primary_key = True)

    name = Column(
        String(80),
        nullable = False
        )

    user_id = Column(
        Integer,
        ForeignKey('user.id')
        )

    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name' : self.name,
            'id' : self.id,
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

    restaurant = relationship(Restaurant)

    user_id = Column(
        Integer,
        ForeignKey('user.id')
        )

    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'price' : self.price,
            'course' : self.course,
        }


## ENDING configuration
###### insert at end of file ######
engine = create_engine(
    'sqlite:///restaurantmenuwithusers.db')

# Enters data specified into db
Base.metadata.create_all(engine)
