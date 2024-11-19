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