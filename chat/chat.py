import socket
import threading
import sys

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen(1)

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connection in connections:
                connection.send(data)
            if not data:
                break

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self):
        self.sock.connect((address, 10000))

        
if (len(sys.argv) > 1):
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()
    
while True:
    c, a = sock.accept()
    cThread = threading.Thread(target=handler, args=(c, a))
    cThread.daemon = True
    cThread.start()
    connections.append(c)
    print(connections)

# from flask import Flask, render_template
# import datetime

# app = Flask(__name__)

# @app.template_filter()
# def datetimefilter(value, format='%Y/%m/%d %H:%M'):
#     """convert a datetime to a different format."""
#     return value.strftime(format)

# app.jinja_env.filters['datetimefilter'] = datetimefilter

# @app.route("/")
# def template_test():
#     return render_template('template.html', my_string="Wheeeee!", 
#         my_list=[0,1,2,3,4,5], title="Index", current_time=datetime.datetime.now())

# @app.route("/home")
# def home():
#     return render_template('template.html', my_string="Foo", 
#         my_list=[6,7,8,9,10,11], title="Home", current_time=datetime.datetime.now())

# @app.route("/about")
# def about():
#     return render_template('template.html', my_string="Bar", 
#         my_list=[12,13,14,15,16,17], title="About", current_time=datetime.datetime.now())

# @app.route("/contact")
# def contact():
#     return render_template('template.html', my_string="FooBar"
#         , my_list=[18,19,20,21,22,23], title="Contact Us", current_time=datetime.datetime.now())


# if __name__ == '__main__':
#     app.run(debug=True)