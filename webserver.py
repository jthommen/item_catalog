from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

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
                output += "<html><body>Hello!</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found %s' % self.path)


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