import flask
import server
import MySQLdb
import re

@server.application.route("/api/v1/log/", methods=["POST"])
def post_log():
    '''
    Log anything noteworthy onto the database.
    '''
    cursor = server.model.Cursor()
    body = flask.request.json
    cursor.execute(
        '''
        INSERT INTO logs (type, context, message)
        VALUES (%(type)s, %(context)s, %(message)s)
        ''',
        {
            'type': body['type'],
            'context': body['context'],
            'message': body['message']

        }
    )
    return flask.jsonify({"success": True}), 200