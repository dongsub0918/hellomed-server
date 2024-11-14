import flask
import server

@server.application.route("/api/v1/test/")
def chat_test():
    query = "Does the clinic treat colds and flus?"
    chatbot = server.model.Chatbot()
    response = chatbot.chatbot_response(query)

    # Return a JSON response indicating success
    return flask.jsonify(response), 200