# Google OAuth
# Client ID: 909204405195-37r0lmucv8qu5vvrk1qorva6rla5f7a0.apps.googleusercontent.com
# Client Secret: HF9NxXMoPg4rKlIISlPvTZ69

# Import flask class from Flask library
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

## Imports db and db connection modules
# Imports db engine initialization
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Imports db setup
from database_setup import Base, Restaurant, MenuItem, User

# Imports session module
from flask import session as login_session
import random, string

# Imports for OAuth server response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


# Create client ID
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Create Flask instance with running app as arg
app = Flask(__name__)

# Specifies and creates db connection
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine

# Creates db connection session item
DBSession = sessionmaker(bind=engine)
session = DBSession()


## Login & Session Handling
# Create anti-forgery token
# Store it in the session for later validation
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("You are now logged in as %s" % login_session['username'])
    print "Done!"
    return render_template('welcome.html', userinfo=login_session)


# Disconnect - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

# Facebook Connect Handlers
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("You are now logged in as %s" % login_session['username'])
    print "Done!"
    return render_template('welcome.html', userinfo=login_session)

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('restaurants'))
    else:
        flash("You were not logged in")
        return redirect(url_for('restaurants'))



## User Handling
def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user.id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Making API Endpoints (GET Request)
@app.route('/restaurants/JSON/')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])


@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[item.serialize for item in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>/JSON/')
def menuItemJSON(restaurant_id, menuitem_id):
    item = session.query(MenuItem).filter_by(id=menuitem_id).one()
    return jsonify(MenuItem=[item.serialize])


# Decorator that wraps app into flask route function
# decorators can get stacked on top of each other
@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/new/', methods = ['GET', 'POST'])
def newRestaurant():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newRestaurant = Restaurant(
            name = request.form['name'], user_id=login_session['user_id'])
        session.add(newRestaurant)
        session.commit()
        flash('New restaurant created!')
        return redirect(url_for('restaurants'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    user_id = getUserID(login_session['email'])
    if request.method == 'POST':
        if user_id == restaurant.user_id:
            restaurant.name = request.form['name']
            session.add(restaurant)
            session.commit()
            flash('Restaurant edited!')
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        else:
            flash('You are not authorized to do that!')
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        if user_id == restaurant.user_id:
            return render_template('editrestaurant.html', restaurant=restaurant)
        else:
            flash('You are not authorized to do that!')
            return redirect(url_for('restaurants'))


@app.route('/restaurants/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    user_id = getUserID(login_session['email'])
    if request.method == 'POST':
        if user_id == restaurant.user_id:
            session.delete(restaurant)
            for item in items:
                session.delete(item)
            session.commit()
            flash('Restaurant deleted!')
            return redirect(url_for('restaurants'))
        else:
            flash('You are not authorized to do that!')
            return redirect(url_for('restaurants'))
    else:
        if user_id == restaurant.user_id:
            return render_template('deleterestaurant.html', restaurant=restaurant)
        else:
            flash('You are not authorized to do that!')
            return redirect(url_for('restaurants'))


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    user_id = getUserID(login_session['email'])
    if user_id == restaurant.user_id:
        return render_template('menu.html', restaurant=restaurant, items=items)
    else:
        return render_template('publicmenu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    user_id = getUserID(login_session['email'])
    if request.method == 'POST':
        if user_id == restaurant.user_id:
            newItem = MenuItem(
                name=request.form['name'],
                description = request.form['description'],
                price = request.form['price'],
                restaurant_id = restaurant_id,
                user_id = restaurant.user_id
                )
            session.add(newItem)
            session.commit()
            flash('New menu item created!')
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        else:
            flash('You are not authorized to do that!')
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        if user_id == restaurant.user_id:
            return render_template('newmenuitem.html', restaurant=restaurant)
        else:
            flash('You are not authorized to do that!')
            return redirect(url_for('restaurants'))


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menuitem_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menuitem_id).one()
    user_id = getUserID(login_session['email'])
    if request.method == 'POST':
        if user_id == restaurant.user_id:
            item.name = request.form['name']
            item.description = request.form['description']
            item.price = request.form['price']
            item.id = item.id
            session.add(item)
            session.commit()
            flash('Menu item edited!')
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        else:
            flash('You are not authorized to do that!')
            return redirect(url_for('restaurants'))
    else:
        if user_id == restaurant.user_id:
            return render_template('editmenuitem.html', item=item, restaurant_id=restaurant_id)
        else:
            flash('You are not authorized to do that!')
            return redirect(url_for('restaurants'))


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menuitem_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menuitem_id).one()
    user_id = getUserID(login_session['email'])
    if request.method == 'POST':
        if user_id == restaurant.user_id:
            session.delete(item)
            session.commit()
            flash('Menu item deleted!')
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        else:
            flash('You are not authorized to do that!')
            return redirect(url_for('restaurants'))
    else:
        if user_id == restaurant.user_id:
            return render_template('deletemenuitem.html', item=item, restaurant_id=restaurant_id)
        else:
            flash('You are not authorized to do that!')
            return redirect(url_for('restaurants'))


# Script only runs when directly run in python
# and not imported as module
if __name__ == '__main__':
    app.secret_key = 'very_secret_key'
    # Reloads server on code change
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)