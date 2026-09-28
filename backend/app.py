from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #This allows the front end to call this file

todos = []
next_id = 1

@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def add_todo():
    global next_id
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "title is required"}), 400

    todo = {"id": next_id, "title": data["title"], "done": False}
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201

@app.route("/todos/<int:todo_id>", methods=["PUTS"])
def update_todo(todo_id):
    data = request.get_json()

    for todo in todos:
        if todo["id"] == todo_id:
            todo["title"] = data.get("title", todo["title"])
            todo["done"] = data.get("done", todo["done"])

            return jsonify(todo)

    return jsonify({"error": "Todo not found"}), 404

@app.route("/todos/<int:todo_id>", methods=["Delete"])
def delete_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return jsonify({"message": "Detected"})

    return jsonify({"error": "Todo not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
    