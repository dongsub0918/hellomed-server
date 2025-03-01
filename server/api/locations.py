import flask
import server
from ..utils import convert_est_to_utc

@server.application.route("/api/v1/locations/", methods=["GET"])
def get_locations_info():
    '''
    Get all location related information.
    '''
    cursor = server.model.Cursor()
    cursor.execute(
        '''
        SELECT * FROM locations
        ''',
        {}
    )
    locations = cursor.fetchall()
    return flask.jsonify(locations), 200

@server.application.route("/api/v1/locations/", methods=["PUT"])
def put_locations_info():
    '''
    Update location related information.
    '''
    body = flask.request.json

    # Convert holiday_start and holiday_end to UTC
    for location in body:
        location["holiday_start"] = convert_est_to_utc(location["holiday_start"])
        location["holiday_end"] = convert_est_to_utc(location["holiday_end"])

    cursor = server.model.Cursor()
    for location in body:
        cursor.execute(
            '''
            UPDATE locations
            SET
            title = %(title)s,
            address = %(address)s,
            holiday_start = %(holiday_start)s,
            holiday_end = %(holiday_end)s,
            holiday_message = %(holiday_message)s,
            mon = %(mon)s,
            tue = %(tue)s,
            wed = %(wed)s,
            thu = %(thu)s,
            fri = %(fri)s,
            sat = %(sat)s,
            sun = %(sun)s,
            lunch_break = %(lunch_break)s,
            open = %(open)s
            WHERE code = %(code)s
            ''',
            location
        )
    return flask.jsonify({"Success": True}), 200