# decide package
import sqlite3

# Inherit shared and logging

# TODO: Do later
class AuthenticationBase():
    """
    Description of AuthenticationBase

    Attributes:
        attr1 (str): Description of 'attr1' 

    """

    def __init__(self):
        self.get_conn, self.set_conn = self.auth_closure()

    def init_db(self, path, name):
        c = sqlite3.connect(path + name + '.db')
        conn = c.cursor()
        return conn
    
    def init_tables(self, conn):
        pass

    def init_superuser(self, conn):
        pass

    def auth_closure(self):
        connection = {}

        def get_dbconn(names):
            if type(names) == str:
                return connection.get(names)
            if type(names) == list:
                conn = {}
                for name in names:
                    if name in connection:
                        conn.update({name: connection.get(name)})
                return conn
            return {}

        def set_dbconn(name, conn):
            if type(name) == str and type(conn) == dict:
                connection.update({name: conn})
                return {name: conn}
            return None

        return {"get_conn": get_dbconn, "set_conn": set_dbconn}
    
    def is_authenticated(self):
        pass

    def create_user(self):
        pass

    def update_user(self):
        pass

    def delete_user(self):
        pass

    def change_pass(self):
        pass

