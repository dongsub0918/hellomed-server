import flask
import server
from datetime import datetime, date
from zoneinfo import ZoneInfo

@server.application.route("/api/v1/check-in/", methods=["POST"])
def post_check_in():
    '''
    Intake body from POST request and insert into database.
    '''
    body = flask.request.json
    cursor = server.model.Cursor()
    cursor.execute(
        '''
        INSERT INTO check_ins (
        name, 
        birthDate, 
        phone, 
        email, 
        hearAboutUs, 
        address,
        zipcode,
        medicationAllergy, 
        preferredPharmacy, 
        homeMedication, 
        reasonForVisit, 
        exposures, 
        recentTests, 
        recentVisits)
        VALUES (
        %(name)s, 
        %(birthDate)s, 
        %(phone)s, 
        %(email)s, 
        %(hearAboutUs)s, 
        %(address)s, 
        %(zipcode)s,
        %(medicationAllergy)s, 
        %(preferredPharmacy)s, 
        %(homeMedication)s, 
        %(reasonForVisit)s, 
        %(exposures)s, 
        %(recentTests)s, 
        %(recentVisits)s)
        ''',
        body
    )
    inserted_check_in_id = cursor.lastrowid()

    # For real-time updates, emit the new check-in to the client
    cursor.execute(
        '''
        SELECT
        id,
        name,
        birthDate,
        email,
        reasonForVisit,
        created_at,
        viewed
        FROM check_ins
        WHERE id = %(id)s
        ''',
        {
            'id': inserted_check_in_id
        }
    )
    check_in_to_emit = cursor.fetchone()
    
    if check_in_to_emit:
        # Handle birthDate (datetime.date object)
        if isinstance(check_in_to_emit['birthDate'], date):
            # Convert to datetime (assuming midnight as the time)
            birth_date_dt = datetime.combine(check_in_to_emit['birthDate'], datetime.min.time())
            
            # Make timezone-aware (assuming UTC)
            birth_date_dt = birth_date_dt.replace(tzinfo=ZoneInfo("UTC"))
            
            # Format with timezone info
            check_in_to_emit['birthDate'] = birth_date_dt.strftime('%Y-%m-%d %Z')

        # Handle created_at (datetime.datetime object)
        if isinstance(check_in_to_emit['created_at'], datetime):
            if check_in_to_emit['created_at'].tzinfo is None:
                check_in_to_emit['created_at'] = check_in_to_emit['created_at'].replace(tzinfo=ZoneInfo("UTC"))
            check_in_to_emit['created_at'] = check_in_to_emit['created_at'].strftime('%Y-%m-%d %H:%M:%S %Z')

    server.sio.emit('new-checkin', check_in_to_emit)

    return flask.jsonify({"id": inserted_check_in_id}), 200

@server.application.route("/api/v1/check-in/", methods=["GET"])
def get_check_ins():
    '''
    Get submitted check-ins by page and size. Size per page is defaulted to 20.
    '''
    # Initialize flask request arguments
    size = flask.request.args.get(
        "size",
        default=15,
        type=int
    )
    page = flask.request.args.get(
        "page",
        default=0,
        type=int
    )

    # Sanity check for appropriate flask request arguments
    if page < 0:
        return flask.jsonify({'error': 'invalid pagination args'}), 400

    # Fetch check-ins from the database with proper pagination
    cursor = server.model.Cursor()
    cursor.execute(
        '''
        SELECT
        id,
        name,
        birthDate,
        email,
        reasonForVisit,
        created_at,
        viewed
        FROM check_ins 
        ORDER BY id DESC LIMIT %(limit)s OFFSET %(offset)s
        ''',
        {
            'limit': size,
            'offset': page * size
        }
    )
    check_ins = cursor.fetchall()

    # If no check-ins are found for the requested page
    if not check_ins:
        return flask.jsonify({'error': 'No check-ins in requested page'}), 404
    
    # Fetch row count of check_ins
    cursor.execute('SELECT COUNT(*) AS total_count FROM check_ins', {})
    total_count = cursor.fetchone()['total_count']
    
    response = {
        'checkIns': check_ins,
        'totalCheckIns': total_count
    }

    # Return the paginated results
    return flask.jsonify(response), 200

@server.application.route("/api/v1/check-in/<int:id>/", methods=["GET"])
def get_check_in(id):
    cursor = server.model.Cursor()
    cursor.execute(
        '''
        SELECT * FROM check_ins 
        WHERE id = %(id)s
        ''',
        {
            'id': id
        }
    )
    check_in = cursor.fetchone()

    # If check-in is found and not viewed, update viewed to 1
    if check_in and not check_in['viewed']:
        cursor.execute(
            '''
            UPDATE check_ins
            SET viewed = 1
            WHERE id = %(id)s
            ''',
            {
                'id': id
            }
        )


    return flask.jsonify(check_in), 200