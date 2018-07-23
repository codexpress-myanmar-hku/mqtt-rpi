#Logging server 
try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except:
    print("Library not present")
try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except:
    print("Library not present")

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open('logs.log', 'rb') as file: 
            self.wfile.write(file.read())
            
myServer = HTTPServer(('0.0.0.0', 8080), MyServer)
myServer.serve_forever()


