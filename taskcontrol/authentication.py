# decide package
import sqlite3

# Inherit shared and logging

# TODO: Do later
# https://docs.python.org/3/library/sqlite3.html
# https://docs.python.org/3/library/pickle.html


class AuthenticationBase():
    """
    Description of AuthenticationBase

    Attributes:
        attr1 (str): Description of 'attr1'

    """

    def __init__(self):
        self.get_conn, self.set_conn, self.get_pconn, self.set_pconn = self.auth_closure()

    def auth_closure(self):
        db_connections = {}
        pickle_connections = {}

        def init_db(self, path, name):
            c = sqlite3.connect(path + name + '.db')
            return c

        def init_tables(self, conn):
            pass

        def init_superuser(self, conn):
            pass

        def init_pickle(self, path, name):
            out = open(path + name + ".pickle", "wb")
            return out

        def init_ptables(self, conn):
            pass

        def init_psuperuser(self, conn):
            pass

        def get_dbconn(names):
            if type(names) == str:
                cdb = sqlite3.connect(db_connections.get(names))
                conn = cdb.cursor()
                return conn
            if type(names) == list:
                conn = {}
                for name in names:
                    if name in db_connections:
                        cdb = sqlite3.connect(db_connections.get(name))
                        conn = cdb.cursor()
                        conn.update({name: conn})
                return conn
            return None

        def set_dbconn(name, options):
            # options
            #
            if type(name) == str and type(options) == dict:
                db_connections.update({name: options})
                return {name: options}
            return None

        def db_execute(query):
            pass

        def db_close(conn):
            conn.close()

        def get_pconn(names):
            # pickle_connections
            # example_dict = pickle.load(pickle_in)
            pass

        def set_pconn(name, options):
            # options
            #
            # pickle_connections
            pass

        def p_dump(query):
            # pickle.dump(example_dict, pickle_out)
            pass

        def p_close(conn):
            # pickle_out.close()
            pass

        return {
            "get_conn": get_dbconn,
            "set_conn": set_dbconn,
            "get_pconn": get_pconn,
            "set_pconn": set_pconn
        }

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
