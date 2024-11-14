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
        birthdate, 
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
        recenVisits)
        VALUES (
        %(name)s, 
        %(birthdate)s, 
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
        %(recenVisits)s)
        ''',
        body
    )
    return flask.jsonify({"message": "check-in submitted successfully"}), 200