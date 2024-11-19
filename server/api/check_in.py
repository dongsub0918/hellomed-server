import flask
import server

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
    return flask.jsonify({"message": "check-in submitted successfully"}), 200

@server.application.route("/api/v1/check-in/", methods=["GET"])
def get_check_ins():
    '''
    Get submitted check-ins by page and size. Size per page is defaulted to 20.
    '''
    # Initialize flask request arguments
    size = flask.request.args.get(
        "size",
        default=20,
        type=int
    )
    page = flask.request.args.get(
        "page",
        default=0,
        type=int
    )

    # Sanity check for appropriate flask request arguments
    if size not in [10, 20, 30] or page < 0:
        return flask.jsonify({'error': 'invalid pagination args'}), 400

    # Fetch check-ins from the database with proper pagination
    cursor = server.model.Cursor()
    cursor.execute(
        '''
        SELECT * FROM check_ins 
        ORDER BY id DESC
        LIMIT %(limit)s OFFSET %(offset)s
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

    # Return the paginated results
    return flask.jsonify(check_ins), 200