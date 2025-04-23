import flask
import server

@server.application.route("/api/v1/carousel/", methods=["GET"])
def get_carousel_items():
    """
    Get all carousel items from the database.
    """
    cursor = server.model.Cursor()
    cursor.execute("SELECT * FROM carousel_items", {})
    items = cursor.fetchall()
    
    return flask.jsonify(items)
