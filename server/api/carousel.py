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

@server.application.route("/api/v1/carousel/", methods=["PUT"])
def put_carousel_items():
    """
    Update carousel items in the database.
    """
    try:
        body = flask.request.get_json()
        cursor = server.model.Cursor()
        
        # First, clear existing items
        cursor.execute("DELETE FROM carousel_items", {})
        
        # Then insert new items
        for item in body:
            cursor.execute(
                """
                INSERT INTO carousel_items (title, description, image_src, href)
                VALUES (%(title)s, %(description)s, %(image_src)s, %(href)s)
                """,
                {
                    "title": item.get("title", ""),
                    "description": item.get("description", ""),
                    "image_src": item.get("imageSrc", ""),
                    "href": item.get("href")
                }
            )
        
        return flask.jsonify({"message": "Carousel items updated successfully"}), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500
