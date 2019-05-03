import json
import sqlite3
from flask import Flask, request, g
from user import User
app = Flask(__name__)

DATABASE = 'src/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().cursor()
    cur.execute(query, args)
    get_db().commit();
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return 'Server Works!'

@app.route('/user', methods = ['POST'])
def postUser():

    content = request.get_json()
    update = True
    id_user = 0
    status = "500"
    message = "Error"

    try:
        content["id"]
    except KeyError as e:
        update = False

    if update:
        usr = User(content["id"], 
                   content["email"], 
                   content["password"], 
                   content["first_name"], 
                   content["last_name"]) 
        query_db(usr.update_sql(), usr.update_user_tuple())
        id_user = str(content["id"])
        status = "200"
        message = "The user was updated successfully"
    else:
        usr = User("", 
                   content["email"], 
                   content["password"], 
                   content["first_name"], 
                   content["last_name"]) 
        query_db(usr.insert_sql(), usr.insert_user_tuple())
        q = query_db("select max(ID) 'm' from main.USER", (), True)
        id_user = str(q["m"])
        status = "200"
        message = "The user was created successfully"

    result = {
        "status": status,
        "message": message,
        "id": id_user
    }

    return json.dumps(result)
