from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import database_service
from urlparse import parse_qs

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>Hello World"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say? </h2>"
                output += "<input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>&#161Hola <a href='/hello'>Back to Hello</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say? </h2>"
                output += "<input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Restaurant</h1>"
                restaurants = database_service.GetAllRestaurant()
                for restaurant in restaurants:
                    output += "<a href='/menuitem?rid=%s'> %s </a> &nbsp&nbsp&nbsp&nbsp&nbsp" %(restaurant.id,restaurant.name)
                    output += "<a href='/restaurant/%s/edit'>Edit</a> &nbsp&nbsp&nbsp " %(restaurant.id)
                    output += "<a href='/restaurant/%s/delete'>Delete</a>" %(restaurant.id)
                    output += "</br>"
                output += "</br>"
                output += "</br>"
                output += "</br>"
                output += "<a href='/restaurant/new'>Add a new restaurant</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data'>"
                output += "<h2>What is your restaurant's name? </h2>"
                output += "<input name='r_name' type='text' placeholder='New Restaurant Name'>"
                output += "<input type='submit' value='Create'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                rid = self.path.split("/")[2]
                restaurant = database_service.GetRestaurant(rid)
                
                if restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Edit Restaurant</h1>"
                    output += "<form method='POST' enctype='multipart/form-data'>" %rid
                    output += "<input name='r_name' type='text' placeholder='%s'>" %restaurant.name
                    output += "<input type='submit' value='Rename'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return

            if self.path.endswith("/delete"):
                rid = self.path.split("/")[2]
                restaurant = database_service.GetRestaurant(rid)

                if restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s</h1>" %restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete'>" %rid
                    output += "<input type='submit' value='Delete'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return
                

            if self.path.endswith("/menuitem"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                restaurant_id = parse_qs(urlparse(self.path).query).get('rid',None)
                output = ""
                output += "<html><body>"
                output += "<h1>Menu</h1>"
                menuitems = database_service.GetMenuItem(restaurant_id)
                for item in menuitems:
                    output += " <h2> %s </h2> " %(item.name)
                    output ++ " <h3> %s </h3> " %(item.price)
                    output += "</br>"
                    output += "<p> %s </p>" %(item.description)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404,"File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('r_name')
                rid = self.path.split("/")[2]
                database_service.DelRestaurant(rid)
                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurant')
                self.end_headers()
                return
            
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('r_name')
                rid = self.path.split("/")[2]
                database_service.EditRestaurant(rid,messagecontent[0])
                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurant')
                self.end_headers()
                return
            
            if self.path.endswith('/restaurant/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('r_name')
                
            database_service.NewRestaurant(messagecontent[0])
            self.send_response(301)
            self.send_header('Content-type','text/html')
            self.send_header('Location','/restaurant')
            self.end_headers()
            return
            
        except:
            pass
   
def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
        
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()
