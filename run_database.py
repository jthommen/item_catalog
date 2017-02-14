#### Script that connects to DB via sqlalchemy orm ####

## IMPORT
# Import sqlalchemy data to populate db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import database configuration classes
from database_setup import Base, Restaurant, MenuItem


## CONNECT
# Specifies database engine to connect to
engine = create_engine('sqlite:///restaurantmenu.db')

# Binds engine to base class
Base.metadata.bind = engine

# Creates link of communication via session -> interface
DBSession = sessionmaker(bind = engine)

# Staging object for database communication
session = DBSession()


## POPULATE
# Creates instances for db entry
myFirstRestaurant = Restaurant(name = "Juri's Pizza")
salmonPizza = MenuItem(
    name = 'Salmon Pizza',
    description = '''Delicious pizza with smoked
        wild Irish salmon and buffalo mozarella''',
    course = 'Main',
    price = '$16.00',
    restaurant = myFirstRestaurant)

# Adds instances to staging area
session.add(myFirstRestaurant)
session.add(salmonPizza)

# Commits staging area to db
session.commit()

# Queries items
print session.query(Restaurant).all()
print session.query(MenuItem).all()