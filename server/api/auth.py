import flask
import server
import MySQLdb
import re

@server.application.route("/api/v1/auth/<string:email>/", methods=["GET"])
def get_admin(email):
    '''
    Check if the given email is an admin.
    '''
    cursor = server.model.Cursor()
    cursor.execute(
        '''
        SELECT email FROM admin WHERE email = %(email)s
        ''',
        {
            'email': email
        }
    )
    isAdmin = cursor.fetchone()
    if isAdmin:
        return flask.jsonify({"isAdmin": True}), 200
    else:
        return flask.jsonify({"isAdmin": False}), 200
    
@server.application.route("/api/v1/auth/", methods=["GET"])
def get_admins():
    '''
    Check if the given email is an admin.
    '''
    cursor = server.model.Cursor()
    cursor.execute(
        '''
        SELECT email FROM admin
        ''',
        {}
    )
    admins = cursor.fetchall()
    return flask.jsonify(admins), 200
    
@server.application.route("/api/v1/auth/<string:email>/", methods=["POST"])
def post_admin(email):
    '''
    Add a new admin.
    '''
    if email.split('@')[1] != 'hello-med.com':
        return flask.jsonify({"error": "Email must use @hello-med.com domains."}), 400
    try:
        cursor = server.model.Cursor()
        cursor.execute(
            '''
            INSERT INTO admin (email) VALUES (%(email)s)
            ''',
            {'email': email}
        )
        return flask.jsonify({"success": True}), 200

    except MySQLdb.OperationalError:
        return flask.jsonify({"error": "Input is not in email form."}), 500

    except MySQLdb.IntegrityError:
        return flask.jsonify({"error": "Email already exists."}), 409

    except Exception as e:
        return flask.jsonify({"error": "Unexpected error"}), 500
    
@server.application.route("/api/v1/auth/<string:email>/", methods=["DELETE"])
def delete_admin(email):
    '''
    Delete an admin.
    '''
    cursor = server.model.Cursor()
    cursor.execute(
        '''
        DELETE FROM admin WHERE email = %(email)s
        ''',
        {
            'email': email
        }
    )
    return flask.jsonify({"success": True}), 200