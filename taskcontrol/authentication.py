# decide package
import sqlite3
import pickle

# Inherit shared and logging

# RESOURCES for later
# https://docs.python.org/3/library/sqlite3.html
# https://docs.python.org/3/library/pickle.html

# TODO
# Consider making this an interface that can be extended later
# Which will make it compatible to any DB and Authentication ways

from .interfaces import AuthenticationBase


class AuthBase(AuthenticationBase):

    def __init__(self, **kwargs):
        if self.verify_structure(**kwargs):
            self.get_dbconn, self.set_dbconn, self.db_execute, self.db_close, self.get_pconn, self.set_pconn, self.p_dump, self.p_close = self.auth_closure(
                **kwargs)

    def verify_structure(self, **kwargs):
        if not kwargs.get("get_dbconn") or not kwargs.get("set_dbconn") or not kwargs.get("db_execute") or not kwargs.get("db_close") or not kwargs.get("get_pconn") or not kwargs.get("set_pconn") or not kwargs.get("p_dump") or not kwargs.get("p_close"):
            return False
        return True

    def init_db(self, path, name):
        c = sqlite3.connect(path + name + '.db')
        return c

    def init_tables(self, conn):
        try:
            try:
                sql = """
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(255) UNIQUE,
                        password VARCHAR(255) NOT NULL
                    );
                """
                conn.execute(sql)
                print("Table users created successfully")
                conn.commit()
            except:
                raise Exception("Unable to create Users Table")
            
            try:
                sql = """
                    CREATE TABLE roles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        userid VARCHAR(255) NOT NULL,
                        role VARCHAR(255) NOT NULL,
                        activity VARCHAR(255) NOT NULL,
                        permission VARCHAR(255) NOT NULL
                    );
                """
                conn.execute(sql)
                print("Table roles created successfully")
                conn.commit()
            except:
                raise Exception("Unable to create Roles Table")
            try:
                sql = """
                    CREATE TABLE sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        userid VARCHAR(255) NOT NULL,
                        sessionid VARCHAR(255) NOT NULL,
                        time VARCHAR(255) NOT NULL,
                        loggedin BOOLEAN NOT NULL
                    );
                """
                conn.execute(sql)
                print("Table sessions created successfully")
                conn.commit()
            except:
                raise Exception("Unable to create Sessions Table")
        except:
            return False
        return True

    def init_superuser(self, conn, options):
        # username, password, role, activity, permission
        try:
            # error here on string format?
            sql = """
                INSERT INTO users (username, password) VALUES (?, ?);
            """
            u = options.get("username")
            p = options.get("password")
            if u and p:
                conn.execute(sql, (u, p))
                print("User created successfully")
                conn.commit()
            else:
                raise ValueError("Username, Password not provided")

            # get userid
            # conn.execute("""SELECT userid FROM tasks WHERE username = {0} AND password = {1}""".format(str(username), str(password)))
            # rows = conn.fetchall()
            # if len(rows) == 1:
            #     for row in rows:
            #         rolesql = '''
            #             insert into roles (userid, role, activity, permission) values ({0}, {1}, {2}, {3});
            #         '''.format(str(row), str(role), str(activity), str(permission))
            #         conn.execute(rolesql)
            #         print("Role created successfully")
            #         conn.commit()
        except:
            return False
        return True

    def init_pickle(self, path, name):
        out = open(path + name + ".pickle", "wb")
        return out

    def init_ptables(self, conn):
        pass

    def init_psuperuser(self, conn):
        pass

    def auth_closure(self, get_dbconn=None, set_dbconn=None, db_execute=None, db_close=None,
                     get_pconn=None, set_pconn=None, p_dump=None, p_close=None):
        db_connections = {}
        pickle_connections = {}

        if get_dbconn != None and type(get_dbconn) == callable:
            def fn_1(conn, names):
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
            get_dbconn = fn_1

        if set_dbconn != None and type(set_dbconn) == callable:
            def fn_2(name, options):
                # options
                #
                if type(name) == str and type(options) == dict:
                    db_connections.update({name: options})
                    return {name: options}
                return None
            set_dbconn = fn_2

        if db_execute != None and type(db_execute) == callable:
            def fn_3(query):
                pass
            db_execute = fn_3

        if db_close != None and type(db_close) == callable:
            def fn_4(conn):
                conn.close()
            db_close = fn_4

        if get_pconn != None and type(get_pconn) == callable:
            def fn_5(names):
                # pickle_connections
                # example_dict = pickle.load(pickle_in)
                pass
            get_pconn = fn_5

        if set_pconn != None and type(set_pconn) == callable:
            def fn_6(name, options):
                # options
                #
                # pickle_connections
                pass
            set_pconn = fn_6

        if p_dump != None and type(p_dump) == callable:
            def fn_7(query):
                # pickle.dump(example_dict, pickle_out)
                pass
            p_dump = fn_7

        if p_close != None and type(p_close) == callable:
            def fn_8(conn):
                # pickle_out.close()
                pass
            p_close = fn_8

        return (
            get_dbconn, set_dbconn, db_execute, db_close,
            get_pconn, set_pconn, p_dump, p_close
        )

    def create_user(self, options):
        pass

    def update_user(self, options):
        pass

    def delete_user(self, options):
        pass

    def get_user(self, options):
        pass

    def change_password(self, options):
        pass

    def create_permissions(self, options):
        # user/role, action, permissions
        pass

    def update_permissions(self, options):
        pass

    def delete_permissions(self, options):
        pass

    def get_permissions(self, options):
        pass

    def create_role(self, options):
        # role
        pass

    def update_role(self, options):
        pass

    def delete_role(self, options):
        pass

    def get_role(self, options):
        pass

    def get_user_permissions(self, options):
        # user, role, action, permissions
        return False

    def has_permissions(self, options):
        # get_user_permissions
        return False

    def is_loggedin(self, options):
        # id or username, password
        id = options.get("id")
        username = options.get("username")
        password = options.get("password")
        # check loggedin
        return False

    def is_authenticated(self, options):
        # returns true/false
        # is_loggedin
        if self.is_loggedin(options):
            # has_permissions
            if self.has_permissions(options):
                return True
        return False
