import os
import sqlite3

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #This allows the front end to call this file

#Database connection
DATABASE =  os.path.json(os.path.dirname(__file__), "todos.db")

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute(
        """
        Create Table if Not exists todos(
        id integer primary key Autoincrement,
        title Text Not Null
        done Integer not null Default 0
        )
        """
    )

    conn.commit()
    conn.close()

def row_to_dict(row):
    """Convert database row into dictionary we can send as JSON.
    We turn done form 0/1 int False/True so the fron end gets a real boolean."""
    return {"id": row ["id"], "title": row["title"], "done": bool(row["done"])}

init_db()

todos = []
next_id = 1


#Grabbing an exsisting todo
@app.route("/todos", methods=["GET"])
def get_todos():
    conn = get_db()

    
    return jsonify(todos)

#Creating a new todo
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

#Deleting a todo
@app.route("/todos/<int:todo_id>", methods=["Delete"])
def delete_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return jsonify({"message": "Detected"})

    return jsonify({"error": "Todo not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
