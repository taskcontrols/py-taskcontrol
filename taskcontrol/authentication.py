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
# TODO: Refactor getters and setters and make code simpler

from .interfaces import AuthenticationBase, SQLBase
from .sharedbase import ClosureBase


class SQLORM(SQLBase):

    def create(self, conn, options):
        try:
            sql = """INSERT INTO """ + str(options.get("table"))
            for i in options.get("columns"):
                sql += """ (""" + str(i) + """, """
            sql += """) VALUES ( """

            for j in options.get("values"):
                sql += str(j) + """, """

            sql += """);"""
            conn.execute(sql)
            conn.commit()
            print(options.get("table"), " created successfully")
        except Exception as e:
            raise Exception("Error with options provided", e)
        return True

    def find(self, conn, options):
        try:
            sql = """SELECT """
            for i in options.get("columns"):
                sql += str(i) + """, """
            sql += """ FROM """ + str(options.get("table")) + """ WHERE """
            sql += options.get("conditions")

            # TODO
            # Extend later with all filters, joins, and nested
            # Priority get this working

            # filters = options.get("filters")
            # if type(filters) == str:
            #     sql += filters + """;"""
            # elif type(filters) == dict:
            #     # TODO:
            #     # Make this nested for joins, nested statements, and with all operators
            #     # Currently keeping it only for string and single statements
            #     #
            #     # Not priority
            #     # Reason:
            #     # Let users work on their own DB based systems
            #     #       for other activities in plugin by extending
            #     # Handle only user authentication for small
            #     #       apps and let users scale with their db
            #     # Put SQLITE and Pickle data into memory for every instance
            #     # Make writes to memory and DB to persist
            #     pass

            conn.execute(sql)
            conn.commit()
            print(options.get("table"), " find successfully")
        except Exception as e:
            raise Exception("Error with options provided", e)
        return True

    def update(self, conn, options):
        try:
            sql = """UPDATE """ + options.get("table")
            sql += """ SET """
            # UPDATE STATEMENTS
            sql += options.get("statements")
            sql += """ WHERE """
            # UPDATE CONDITION STATEMENTS

            # Applying conditions
            con = options.get("conditions")
            if con and type(con) == str:
                sql += con

            # filters = options.get("filters")
            sql += """;"""
            conn.execute(sql)
            conn.commit()
            print(options.get("table"), " updated successfully")
        except Exception as e:
            raise Exception("Error with options provided", e)
        return True

    def delete(self, conn, options):
        try:
            sql = """DELETE FROM """
            sql += str(options.get("table")) + """ WHERE """

            # Applying conditions
            con = options.get("conditions")
            if con and type(con) == str:
                sql += con
            # filters = options.get("filters")
            # if type(filters) == str:
            #     sql += filters + """;"""
            # elif type(filters) == dict:
            #     # TODO:
            #     # Make this nested for joins, nested statements, and with all operators
            #     # Currently keeping it only for string and single statements
            #     #
            #     # Not priority
            #     # Reason:
            #     # Let users work on their own DB based systems
            #     #       for other activities in plugin by extending
            #     # Handle only user authentication for small
            #     #       apps and let users scale with their db
            #     # Put SQLITE and Pickle data into memory for every instance
            #     # Make writes to memory and DB to persist
            #     pass
            conn.execute(sql)
            conn.commit()
            print(options.get("table"), " deleted successfully")
        except Exception as e:
            raise Exception("Error with options provided", e)
        return True


class AuthBase(AuthenticationBase, ClosureBase):

    def __init__(self, **kwargs):
        if self.verify_kwargs_structure(**kwargs):
            self.getter, self.setter, self.deleter = self.class_closure(
                dbs={}, pickles={})
        if kwargs.get("sql_orm"):
            self.sql = kwargs.get("sql_orm")()
        else:
            self.sql = SQLORM()

    def verify_kwargs_structure(self, **kwargs):
        if not kwargs.get("get_dbconn") or not kwargs.get("set_dbconn") or not kwargs.get("db_execute") or not kwargs.get("db_close") or not kwargs.get("get_pconn") or not kwargs.get("set_pconn") or not kwargs.get("p_dump") or not kwargs.get("p_close"):
            raise Exception("Authentication Base Arguments Not Correct")
        return True

    def verify_options_structure(self, options):
        # id or username, password
        # action, user
        if type(options) != dict:
            raise TypeError("Options structure wrong")
        return True

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

    def update_permissions(self, conn, options):
        self.verify_options_structure(options)

    def delete_permissions(self, conn, options):
        self.verify_options_structure(options)

    def get_permissions(self, conn, options):
        self.verify_options_structure(options)

    def create_role(self, conn, options):
        self.verify_options_structure(options)
        # role

    def update_role(self, conn, options):
        self.verify_options_structure(options)

    def delete_role(self, conn, options):
        self.verify_options_structure(options)

    def get_role(self, conn, options):
        self.verify_options_structure(options)

    def get_user_permissions(self, conn, options):
        # user, role, action, permissions
        self.verify_options_structure(options)
        return False

    def has_permissions(self, conn, options):
        # user, role, action, permissions for action/user
        self.verify_options_structure(options)
        # get_user_permissions
        return False

    def is_loggedin(self, conn, options):
        # id or username, password
        self.verify_options_structure(options)

        id = options.get("id")
        username = options.get("username")
        password = options.get("password")

        # check loggedin
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
