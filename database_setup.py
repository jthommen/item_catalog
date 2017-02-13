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

    # Specifies relationship to class restaurant
    restaurant = relationship(Restaurant)

## ENDING configuration
###### insert at end of file ######
engine = create_engine(
    'sqlite:///restaurantmenu.db')

# Enters data specified into db
Base.metadata.create_all(engine)
