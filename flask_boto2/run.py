# test-server configuration

from app import app

host = app.config['HOST']
port = app.config['PORT']
debug = app.config['DEBUG']

print("Server running on host " + host + " in port " + str(port))


app.run(host, port, debug)
