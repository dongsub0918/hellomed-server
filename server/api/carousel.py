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
    Update carousel items in the database and clean up unused images.
    """
    try:
        body = flask.request.get_json()
        cursor = server.model.Cursor()
        
        # First, clear existing items
        cursor.execute("DELETE FROM carousel_items", {})
        
        # Then insert new items
        for item in body["carouselItems"]:
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
        
        # Delete unused images from S3
        aws_client = server.model.AWSClient()
        for key in body["keysToDelete"]:
            aws_client.delete_object(key, public=True)
        
        return flask.jsonify({"message": "Carousel items updated successfully"}), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500
