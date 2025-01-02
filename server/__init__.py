"""HELLOMED package initializer."""

import flask
from flask_cors import CORS
from flask_mysqldb import MySQL

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
db = MySQL(application)
CORS(application, origins=["http://localhost:3000", "https://hello-med.com"])

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    instructions + footer_text))

import server.api
import server.model