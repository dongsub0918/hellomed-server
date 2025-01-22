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
        SELECT
        id,
        name,
        birthDate,
        email,
        reasonForVisit,
        created_at
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
    return flask.jsonify(check_in), 200

# @server.application.route("/api/v1/check-in/<int:id>/", methods=["DELETE"])
# def delete_check_in(id):
#     cursor = server.model.Cursor()
#     cursor.execute(
#         '''
#         DELETE FROM check_ins
#         WHERE id = %(id)s
#         ''',
#         {
#             'id': id
#         }
#     )
#     check_in = cursor.fetchone()
#     return flask.jsonify(check_in), 201