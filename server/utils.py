import flask
import jwt
import os
from functools import wraps
from datetime import datetime, timedelta

def convert_est_to_utc(est_datetime_str: str) -> str:
    if not est_datetime_str: return ""

    # Parse the EST datetime string (assumes format 'YYYY-MM-DDTHH:MM')
    try:
        est_datetime = datetime.strptime(est_datetime_str, "%Y-%m-%dT%H:%M")
    except:
        est_datetime = datetime.strptime(est_datetime_str, "%m/%d/%Y, %I:%M %p")

    # Convert EST (UTC-5) to UTC by adding 5 hours
    utc_datetime = est_datetime + timedelta(hours=5)

    # Format as MySQL-compatible datetime string
    return utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

def token_required(func):
    @wraps(func)
    def token_test(*args, **kwargs):
        token = flask.request.headers.get('Authorization')
        if not token:
            return flask.jsonify({'message': 'Missing token'}), 401
        secret_key = os.getenv("SECRET_KEY")
        try:
            token = token.split(' ')[1]
            jwt.decode(token, secret_key, algorithms='HS256')
            return func(*args, **kwargs)
        except Exception as error:
            print(error)
            return flask.jsonify({'error': 'Decode failed'}), 401
    return token_test