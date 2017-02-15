from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## HANDLER SECTION
## Specifies which code to execute
class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2>What would you like me to say?</h2>"
                output += "<input name='message' type='text/html'>"
                output += "<input type='submit' value='Submit'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161Hola!<br><a href='/hello'>Go Hello!</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2>What would you like me to say?</h2>"
                output += "<input name='message' type='text/html'>"
                output += "<input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
            output += "<h2>What would you like me to say?</h2>"
            output += "<input name='message' type='text/html'>"
            output += "<input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output)
            print output

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