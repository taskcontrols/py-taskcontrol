# decide package
import sqlite3

# Inherit shared and logging

# RESOURCES for later
# https://docs.python.org/3/library/sqlite3.html
# https://docs.python.org/3/library/pickle.html


from taskcontrol.lib.interfaces import AuthsInterface
from taskcontrol.lib.utils import UtilsBase
from taskcontrol.lib.orm import SQLORMBase


# TODO
# Consider making this an interface that can be extended later
# Which will make it compatible to any DB and Authentication ways

# TODO: Make all AuthBase functions ORM based


class AuthenticationBase(UtilsBase, AuthsInterface):

    def __init__(self, orm=SQLORMBase, **kwargs):
        self.getter, self.setter, self.deleter = self.class_closure(
            dbs={}, pickles={})
        self.orm = orm()

    def init_db(self, path, name):
        conn = sqlite3.connect(path + name + '.db')
        # add connection to db_connections
        return conn

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
                #  pType      TEXT CHECK( pType IN ('M','R','H') )   NOT NULL DEFAULT 'M',
                sql = """
                    CREATE TABLE roles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        userid VARCHAR(255) NOT NULL,
                        role VARCHAR(255) NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        type VARCHAR(255) CHECK( type IN ('PLUGIN', 'TASK', 'MIDDLEWARE') ) NOT NULL DEFAULT 'TASK',
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
            # encryption needed here
            u = options.get("username")
            p = options.get("password")

            if u and p:
                conn.execute(sql, (u, p))
                conn.commit()
                print("User created successfully")
            else:
                raise ValueError("Username, Password not provided")

            # get userid
            conn.execute(
                """SELECT userid FROM tasks WHERE username = {0} AND password = {1}""", (u, p))
            rows = conn.fetchall()
            if len(rows) == 1:
                for row in rows:
                    rolesql = """
                        INSERT INTO roles (userid, role, activity, permission) values ({0}, {1}, {2}, {3}, {4});
                    """
                    role = options.get("role")
                    name = options.get("name")
                    type = options.get("type")
                    activity = options.get("activity")
                    permission = options.get("permission")
                    if role or name or type or activity or permission:
                        conn.execute(
                            rolesql, (role, name, type, activity, permission))
                        conn.commit()
                        print("Role created successfully")
                    else:
                        raise ValueError("Issue with roles entry values")
            else:
                raise ValueError("Too many related ids")
        except Exception as e:
            return False
        return True

    def init_pickle(self, path, name):
        out = open(path + name + ".pickle", "wb")
        return out

    def init_ptables(self, conn):
        pass

    def init_psuperuser(self, conn):
        pass

    def create_user(self, conn, options):
        self.verify_options_structure(options)

    def update_user(self, conn, options):
        self.verify_options_structure(options)

    def delete_user(self, conn, options):
        self.verify_options_structure(options)

    def get_user(self, conn, options):
        self.verify_options_structure(options)

    def change_password(self, conn, options):
        self.verify_options_structure(options)

    def create_permissions(self, conn, options):
        # user/role, action, permissions
        self.verify_options_structure(options)
        return False

    def update_permissions(self, conn, options):
        self.verify_options_structure(options)
        return False

    def delete_permissions(self, conn, options):
        self.verify_options_structure(options)
        return False

    def get_permissions(self, conn, options):
        self.verify_options_structure(options)
        return {}

    def create_role(self, conn, options):
        self.verify_options_structure(options)
        # create role from db

    def update_role(self, conn, options):
        self.verify_options_structure(options)
        # update role from db

    def delete_role(self, conn, options):
        self.verify_options_structure(options)
        # delete role from db

    def get_role(self, conn, options):
        self.verify_options_structure(options)
        # get role from db

    def get_user_permissions(self, conn, options):
        # user, role, action, permissions
        self.verify_options_structure(options)
        permissions = self.get_permissions(conn, options)
        if permissions:
            return permissions
        return False

    def has_permissions(self, conn, options):
        # user, role, action, permissions for action/user
        self.verify_options_structure(options)
        # get_user_permissions
        if self.get_user_permissions(conn, options):
            return True
        return False

    def is_loggedin(self, conn, options):
        # id or username, password
        self.verify_options_structure(options)

        id = options.get("id")
        username = options.get("username")
        password = options.get("password")

        # check loggedin
        if self.get_user(conn, options):
            return True
        return False

    def is_authenticated(self, conn, options):
        # id or username, password
        # action, user
        self.verify_options_structure(options)

        # is_loggedin
        role = self.is_loggedin(conn, options)
        if role:
            options.update({"role": role})
            # has_permissions
            if self.has_permissions(conn, options):
                return True
        return False


if __name__ == "__main__":
    auth = AuthenticationBase()


__all__ = ["AuthenticationBase"]
