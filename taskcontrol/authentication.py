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
    """
    Description of AuthenticationBase

    Attributes:
        attr1 (str): Description of 'attr1'

    """

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
            sql = '''
                CREATE TABLE users (
                    id INT AUTOINCREMENT NOT NULL PRIMARY KEY,
                    username NOT NULL VARCHAR(255),
                    password NOT NULL VARCHAR(255),
                );
                CREATE TABLE roles (
                    id INT AUTOINCREMENT PRIMARY KEY,
                    user_id NOT NULL VARCHAR(255),
                    role NOT NULL VARCHAR(255),
                    activity NOT NULL VARCHAR(255),
                    permission NOT NULL VARCHAR(255),
                );
            '''
            conn.execute(sql)
            print("Tables created successfully")
            conn.commit()
        except:
            return False
        return True

    def init_superuser(self, conn, username, password, role, activity, permission):
        try:
            sql = '''
                insert into users (username, password) values (str({0}), str({1}));
            '''.format(str(username), str(password))
            conn.execute(sql)
            print("User created successfully")
            conn.commit()
            # get user_id
            
            rolesql = '''
                insert into roles (user_id, role, activity, permission) values ({0}, {1}, {2}, {3});
            '''.format(str(user_id), str(role), str(activity), str(permission))
            conn.execute(rolesql)
            print("Role created successfully")
            conn.commit()
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

    def create_user(self):
        pass

    def update_user(self):
        pass

    def delete_user(self):
        pass

    def get_user(self):
        pass

    def change_password(self):
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

    def get_role(self):
        pass

    def get_user_permissions(self, user):
        # user, role, action, permissions
        pass

    def is_authenticated(self):
        # true/false
        pass
