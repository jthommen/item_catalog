# Import flask class from Flask library
from flask import Flask

## Imports db and db connection modules
# Imports db engine initialization
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Imports db setup
from database_setup import Base, Restaurant, MenuItem

# Create Flask instance with running app as arg
app = Flask(__name__)

# Specifies and creates db connection
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

# Creates db connection session item
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
        output += item.name + str(item.id) +"</br>"
        output += item.price + "</br>"
        output += item.description
        output += "</br></br>"
    return output

@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    output = ""
    output += "Here you can add new Menu items!"
    return output

@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/edit/')
def editMenuItem(restaurant_id, menuitem_id):
    return "Page to edit a menu item!"

@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/delete/')
def deleteMenuItem(restaurant_id, menuitem_id):
    return "Page to delete a menu item"


# Script only runs when directly run in python
# and not imported as module
if __name__ == '__main__':
    # Reloads server on code change
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)