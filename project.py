# Import flask class from Flask library
from flask import Flask, render_template, request, redirect, url_for

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
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantmenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],
            description = request.form['description'],
            price = request.form['price'],
            restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantmenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menuitem_id):
    item = session.query(MenuItem).filter_by(id=menuitem_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        item.id = item.id
        session.add(item)
        session.commit()
        return redirect(url_for('restaurantmenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', item=item, restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menuitem_id):
    item = session.query(MenuItem).filter_by(id=menuitem_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('restaurantmenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=item, restaurant_id=restaurant_id)


# Script only runs when directly run in python
# and not imported as module
if __name__ == '__main__':
    # Reloads server on code change
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)