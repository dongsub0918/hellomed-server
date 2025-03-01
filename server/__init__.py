"""HELLOMED package initializer."""

import flask
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_socketio import SocketIO

# index page texts
header_text = '''
    <html>\n<head> <title>HELLOMED server API</title> </head>\n<body>'''
footer_text = '</body>\n</html>'

# instructions for the API goes here
instructions = '''
    <p>This is the production API server for the HELLOMED website.
    Instructions are to be implemented. Still in development.</p>\n
    '''

# EB looks for an 'application' callable by default.
application = flask.Flask(__name__)
application.config.from_object('server.config')
cors_whitelist = [
    "http://localhost:3000",
    "https://www.hello-med.com",
    "https://hellomed-client-owf8yuo46-dongsub-kims-projects-75b81901.vercel.app"
]

db = MySQL(application)
CORS(application, origins=cors_whitelist)
sio = SocketIO(application, cors_allowed_origins=cors_whitelist)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    instructions + footer_text))

import server.api
import server.model