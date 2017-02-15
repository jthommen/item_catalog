# Import flask class from Flask library
from flask import Flask

# Create Flask instance with running app as arg
app = Flask(__name__)

## Imports db and db connection modules
# Imports db engine initialization
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Imports db setup
from database_setup import Base, Restaurant, MenuItem

# Specifies and creates db connection
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Decorator that wraps app into flask route function
# decorators can get stacked on top of each other
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantmenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    output = ""
    for item in items:
        output += item.name + "</br>"
        output += item.price + "</br>"
        output += item.description
        output += "</br></br>"
    return output

# Script only runs when directly run in python
# and not imported as module
if __name__ == '__main__':
    # Reloads server on code change
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)