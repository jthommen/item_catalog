# Imports basic http webserver and common gateway interface modules
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

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


## HANDLER SECTION
## Specifies which code to execute
class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):

                restaurants = session.query(Restaurant).all()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<!DOCTYPE html>"
                output += "<html><body>"
                output += "<h1>Restaurant List</h1>"
                output += "<p><a href='/restaurants/new'>Create New Restaurant</a></p>"
                for restaurant in restaurants:
                    output += "<strong>%s</strong><br>" % restaurant.name
                    output += "%s<br>" % restaurant.id
                    output += "<a href='/restaurants/%s/edit'>Edit</a><br>" % restaurant.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "<br><br>"
                output += "</body></html>"

                self.wfile.write(output)
                return

            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<!DOCTYPE html>"
                output += "<html><body>"
                output += "<h1>Add A New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='RestaurantName' placeholder='Type Restaurant Name Here' type='text'>"
                output += "<input type='submit' value='Submit'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                return

            if self.path.endswith('/edit'):
                restaurantID = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id=restaurantID).one()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<!DOCTYPE html>"
                output += "<html><body>"
                output += "<h1>Edit A Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurant.id
                output += "<input name='RestaurantName' value='%s' type='text'>" % restaurant.name
                output += "<input type='submit' value='Edit'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                return

            if self.path.endswith('/delete'):
                restaurantID = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id=restaurantID).one()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<!DOCTYPE html>"
                output += "<html><body>"
                output += "<h1>Edit A Restaurant</h1>"
                output += "<p>Are you sure you want to delete: %s?" % restaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurant.id
                output += "<input type='submit' value='Delete'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found %s' % self.path)


    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    RestaurantName = fields.get('RestaurantName')

                    # Create new Restaurant Class
                    newRestaurant = Restaurant(name=RestaurantName[0])
                    session.add(newRestaurant)
                    session.commit()

                    # Create redirect to /restaurants
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    RestaurantName = fields.get('RestaurantName')[0]
                    restaurantID = self.path.split('/')[2]

                    # Update Restaurant
                    restaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                    if restaurant != []:
                        restaurant.name = RestaurantName
                        session.add(restaurant)
                        session.commit()

                        # Create redirect to /restaurants
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith('/delete'):
                    restaurantID = self.path.split('/')[2]

                    # Delete Restaurant
                    restaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                    if restaurant != []:
                        session.delete(restaurant)
                        session.commit()

                        # Create redirect to /restaurants
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

        except:
            pass


## MAIN SECTION
# Instantiate server, specifies port
def main():
    try:
        # Specifies port, no address and default handler
        port = 8080
        server = HTTPServer(('', port), WebserverHandler)
        print 'Web server running on port %s' % port

        # Keeps server running & waiting for requests
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C entered, stopping web server...'
        # Shuts down web server
        server.socket.close()

if __name__ == '__main__':
    main()