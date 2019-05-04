import bcrypt

class User:

    def __init__(self, id_user, email, password, first_name, last_name):
        self.id_user = id_user
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def max_sql(self):
        return "select max(ID) 'm' from main.USER"

    def insert_sql(self):
        return 'insert into main.USER (EMAIL, PASSWORD_HASH, FIRST_NAME, LAST_NAME) values (?, ?, ?, ?)'

    def insert_tuple(self):
        hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        return (self.email, hashed, self.first_name, self.last_name)

    def update_sql(self):
        return 'update main.USER set EMAIL = ?, PASSWORD_HASH = ?, FIRST_NAME = ?, LAST_NAME = ? where ID = ?'

    def update_tuple(self):
        pw_hash = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        return (self.email, pw_hash, self.first_name, self.last_name, self.id_user)

    def login_sql(self):
        return "select PASSWORD_HASH 'pw_hash', FIRST_NAME 'first', LAST_NAME 'last' from main.USER where EMAIL = ?"

    def login_tuple(self):
        return (self.email, )

    def check_pw(self, pw_hash):
        return bcrypt.checkpw(self.password.encode('utf-8'), pw_hash)
