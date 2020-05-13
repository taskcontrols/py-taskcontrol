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

from dataclasses import dataclass
import abc


@dataclass(frozen=True)
class AuthenticationBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def init_db(self, path, name):
        raise NotImplementedError

    @abc.abstractmethod
    def init_tables(self, conn):
        raise NotImplementedError

    @abc.abstractmethod
    def init_superuser(self, conn):
        raise NotImplementedError

    @classmethod
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

    @abc.abstractmethod
    def create_user(self):
        raise NotImplementedError

    @abc.abstractmethod
    def update_user(self):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_user(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self):
        raise NotImplementedError

    @abc.abstractmethod
    def change_password(self):
        raise NotImplementedError

    @abc.abstractmethod
    def create_permissions(self, options):
        # user/role, action, permissions
        raise NotImplementedError

    @abc.abstractmethod
    def update_permissions(self, options):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_permissions(self, options):
        raise NotImplementedError

    @abc.abstractmethod
    def get_permissions(self, options):
        raise NotImplementedError

    @abc.abstractmethod
    def create_role(self, options):
        # role
        raise NotImplementedError

    @abc.abstractmethod
    def update_role(self, options):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_role(self, options):
        raise NotImplementedError

    @abc.abstractmethod
    def get_role(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_permissions(self, user):
        # user, role, action, permissions
        raise NotImplementedError

    @abc.abstractmethod
    def is_authenticated(self):
        # true/false
        raise NotImplementedError


class AuthBase(AuthenticationBase):
    """
    Description of AuthenticationBase

    Attributes:
        attr1 (str): Description of 'attr1'

    """

    def __init__(self):
        self.get_dbconn, self.set_dbconn, self.db_execute, self.db_close, self.get_pconn, self.set_pconn, self.p_dump, self.p_close = self.auth_closure()

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

    def auth_closure(self):
        db_connections = {}
        pickle_connections = {}

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

