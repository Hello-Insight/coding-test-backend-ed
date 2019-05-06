import json
import sqlite3
import datetime
from flask import Flask, session, request, g
from flask_cors import CORS
from flask_jwt import JWT, jwt_required
from user import User
from comic import Comic

app = Flask(__name__)
CORS(app, resources = {r"/*": {"origins": "*"}})
app.secret_key = 's3cr3t_k3y!!!'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=1)
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

class Usr(object):
    def __init__(self, id):
        self.id = id

def authenticate(username, password):
    usr = User("", username, password, "", "")
    q = query_db(usr.login_sql(), usr.login_tuple(), True)

    try:
        pw_hash = q["pw_hash"]
        if usr.check_pw(pw_hash):
            user = Usr(id=q["id"])
            return user
    except TypeError:
        None

def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}

jwt = JWT(app, authenticate, identity)

@app.route('/')
def index():
    return 'Server Works!'

@app.route('/user', methods = ['POST'])
def post_user():
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
        query_db(usr.update_sql(), usr.update_tuple())
        id_user = str(content["id"])
        status = "200"
        message = "The user was updated successfully"
    else:
        usr = User("", content["email"], 
                   content["password"], 
                   content["first_name"], 
                   content["last_name"]) 
        query_db(usr.insert_sql(), usr.insert_tuple())
        q = query_db(usr.max_sql(), (), True)
        id_user = str(q["m"])
        status = "200"
        message = "The user was created successfully"

    result = {
        "status": status,
        "message": message,
        "id": id_user
    }

    return json.dumps(result)

@app.route('/user/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        email = request.args.get('email', '')
        usr = User("", email, "", "", "")
        q = query_db(usr.id_sql(), usr.login_tuple(), True)
        id_user = q["id"]
        
        result = {
            "id": id_user
        }
        
        return json.dumps(result)
        
    content = request.get_json()
    status = "401"
    message = "Please check your credentials"
    usr = User("", content["email"], 
               content["password"], "", "")
    q = query_db(usr.login_sql(), usr.login_tuple(), True)

    try:
        pw_hash = q["pw_hash"]
        if usr.check_pw(pw_hash):
            session["first"] = q["first"]
            session["last"] = q["last"]
            status = "200"
            message = "User logged in successfully"
    except TypeError:
        None

    result = {
        "status": status,
        "message": message
    }

    return json.dumps(result)

@app.route('/user/logout', methods = ['POST'])
def logout():
    session.pop('first', None)
    session.pop('last', None)

    result = {
        "status": "200",
        "message": "User logged out successfully"
    }

    return json.dumps(result)

@app.route('/comic/', methods = ['GET', 'POST'])
def comic():
    if request.method == 'GET':
        tag = request.args.get('tag', '').lower()
        com = Comic("", "", "", "", "", "", "", "", "", "", "", "")
        q = query_db(com.search_sql(), ('%{}%'.format(tag), 
                                        '%{}%'.format(tag)))
        result = []

        for comic in q:
            com = Comic(str(comic['ID']), comic['MONTH'], 
                        str(comic['NUM']), comic['LINK'], 
                        comic['YEAR'], comic['NEWS'], 
                        comic['SAFE_TITLE'], comic['TRANSCRIPT'], 
                        comic['ALT'], comic['IMG'], 
                        comic['TITLE'], comic['DAY'])
            dictionary = com.to_dict()
            dictionary['id'] = dictionary.pop('id_comic')
            result.append(dictionary)

        return json.dumps(result)

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
        com = Comic(content["id"], content["month"], 
                    content["num"], content["link"], 
                    content["year"], content["news"], 
                    content["safe_title"], content["transcript"], 
                    content["alt"], content["img"], 
                    content["title"], content["day"])
        query_db(com.update_sql(), com.update_tuple())
        id_comic = str(content["id"])
        status = "200"
        message = "The comic was updated successfully"
    else:
        com = Comic("", content["month"], 
                    content["num"], content["link"], 
                    content["year"], content["news"], 
                    content["safe_title"], content["transcript"], 
                    content["alt"], content["img"], 
                    content["title"], content["day"])
        query_db(com.insert_sql(), com.insert_tuple())
        q = query_db(com.max_sql(), (), True)
        id_comic = str(q["m"])
        status = "200"
        message = "The comic was created successfully"

    result = {
        "status": status,
        "message": message,
        "id": id_comic
    }

    return json.dumps(result)

@app.route('/comic/<int:id_comic>', methods = ['DELETE'])
@jwt_required()
def delete(id_comic):
    com = Comic(str(id_comic), 
                "", "", "", "", "", "", "", "", "", "", "")
    q = query_db(com.delete_sql(), com.delete_tuple())

    result = {
        "status": "200",
        "message": "The comic was deleted successfully",
        "id": str(id_comic)
    }

    return json.dumps(result)
