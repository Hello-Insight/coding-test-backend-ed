import bcrypt

class User:

    def __init__(self, id_user, email, password, first_name, last_name):
        self.id_user = id_user
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def insert_sql(self):
        return 'insert into main.USER (EMAIL, PASSWORD_HASH, FIRST_NAME, LAST_NAME) values (?, ?, ?, ?)'

    def insert_user_tuple(self):
        hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        return (self.email, hashed, self.first_name, self.last_name)

    def update_sql(self):
        return 'update main.USER set EMAIL = ?, PASSWORD_HASH = ?, FIRST_NAME = ?, LAST_NAME = ? where ID = ?'

    def update_user_tuple(self):
        hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        return (self.email, hashed, self.first_name, self.last_name, self.id_user)
