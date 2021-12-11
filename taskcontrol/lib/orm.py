# Inherit shared and logging

# RESOURCES for later
# https://docs.python.org/3/library/sqlite3.html
# https://docs.python.org/3/library/pickle.html

# TODO
# Consider making this an interface that can be extended later
# Which will make it compatible to any DB and Authentication ways

from taskcontrol.lib.interfaces import SQLInterface, AuthsInterface
from taskcontrol.lib.utils import UtilsBase


class SQLORMBase(UtilsBase, SQLInterface):
    """
    `SQLORMBase` class is a Base for the inbuilt mini SQL ORM which can be redefined as per their own needs using an `SQLInterface` using a different `ORM` that plugs into the application as a `Plugin` \n

    ##### Instance Methods

    @`has_sql` \n
    @`row_insert` \n
    @`row_find` \n
    @`row_update` \n
    @`row_delete` \n
    @`db_create` \n
    @`db_alter` \n
    @`db_delete` \n
    @`db_find` \n
    @`table_create` \n
    @`table_alter` \n
    @`table_delete` \n
    @`table_find` \n

    """
    def __init__(self, dbs={}):
        self.v = ["name"]
        super().__init__("orms", validations={"add": self.v, "create": self.v,
                                              "update": self.v, "delete": ["name"]}, dbs=dbs)

    def has_sql(self, options, run="check", action="search"):
        """
        """
        sql = options.get("sql")
        if action == "check":
            if type(sql) == str and len(sql) > 0:
                return True
            return False
        else:
            if type(sql) == str and len(sql) > 0:
                # TODO: Make this logger
                print(sql, " {0}ed successfully".format(action))
            else:
                print(options.get("table"),
                      " {0}ed successfully".format(action))

    def row_insert(self, conn, options):
        """
        """
        try:
            if self.has_sql(options, run="check"):
                sql = options.get("sql")
            else:
                sql = """INSERT INTO """ + str(options.get("table"))
                for i in options.get("columns"):
                    sql += """ (""" + str(i) + """, """
                sql += """) VALUES ( """

                for j in options.get("values"):
                    sql += str(j) + """, """

                sql += """);"""

            conn.execute(sql)
            if options.get("commit") == True:
                conn.commit()
            self.has_sql(options, run="print", action="create")
        except Exception as e:
            raise Exception("Error with options provided", e)
        return True

    def row_find(self, conn, options):
        """
        """
        try:
            if self.has_sql(options, run="check"):
                sql = options.get("sql")
            else:
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
            if options.get("commit") == True:
                conn.commit()
            self.has_sql(options, run="print", action="search")
        except Exception as e:
            raise Exception("Error with options provided", e)
        return True

    def row_update(self, conn, options):
        """
        """
        try:
            if self.has_sql(options, run="check"):
                sql = options.get("sql")
            else:
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
            if options.get("commit") == True:
                conn.commit()
            self.has_sql(options, run="print", action="update")
        except Exception as e:
            raise Exception("Error with options provided", e)
        return True

    def row_delete(self, conn, options):
        """
        """
        try:
            if self.has_sql(options, run="check"):
                sql = options.get("sql")
            else:
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
            if options.get("commit") == True:
                conn.commit()
            self.has_sql(options, run="print", action="delete")
        except Exception as e:
            raise Exception("Error with options provided", e)
        return True

    def db_create(self, conn, options):
        """
        """
        pass

    def db_alter(self, conn, options):
        """
        """
        pass

    def db_delete(self, conn, options):
        """
        """
        pass

    def db_find(self, conn, options):
        """
        """
        pass

    def table_create(self, conn, options):
        """
        """
        pass

    def table_alter(self, conn, options):
        """
        """
        pass

    def table_delete(self, conn, options):
        """
        """
        pass

    def table_find(self, conn, options):
        """
        """
        pass


class AuthenticationBase(UtilsBase, AuthsInterface):
    """
    `AuthenticationBase` class can be used to authenticate and authorize users within the application \n
    Implements an ORM not as a Inheritance but as an class instance variable. \n
    The Default ORM is `SQLORMBase`. However, you can use any orm and `AuthsInterface` to implement and use your own implementation \n
    
    ##### Instance Methods
    
    @`init_db` \n
    @`init_tables` \n
    @`init_superuser` \n
    @`init_pickle` \n
    @`init_ptables` \n
    @`init_psuperuser` \n
    @`create_user` \n
    @`update_user` \n
    @`delete_user` \n
    @`get_user` \n
    @`change_password` \n
    @`create_permissions` \n
    @`update_permissions` \n
    @`delete_permissions` \n
    @`get_permissions` \n
    @`create_role` \n
    @`get_user_permissions` \n
    @`has_permissions` \n
    @`is_loggedin` \n
    @`is_authenticated` \n

    """

    def __init__(self, orm=SQLORMBase, **kwargs):
        super().__init__(object_name="", validations={}, dbs=kwargs.get("dbs", {}), pickles=kwargs.get("pickles", {}))
        self.orm = orm()

    def init_db(self, path, name):
        """
        
        """
        conn = sqlite3.connect(path + name + '.db')
        # add connection to db_connections
        return conn

    def init_tables(self, conn):
        """
        
        """
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
        """
        
        """
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
        """
        
        """
        out = open(path + name + ".pickle", "wb")
        return out

    def init_ptables(self, conn):
        """
        
        """
        pass

    def init_psuperuser(self, conn):
        """
        
        """
        pass

    def create_user(self, conn, options):
        """
        
        """
        self.verify_options_structure(options)

    def update_user(self, conn, options):
        """
        
        """
        self.verify_options_structure(options)

    def delete_user(self, conn, options):
        """
        
        """
        self.verify_options_structure(options)

    def get_user(self, conn, options):
        """
        
        """
        self.verify_options_structure(options)

    def change_password(self, conn, options):
        """
        
        """
        self.verify_options_structure(options)

    def create_permissions(self, conn, options):
        """
        
        """
        # user/role, action, permissions
        self.verify_options_structure(options)
        return False

    def update_permissions(self, conn, options):
        """
        
        """
        self.verify_options_structure(options)
        return False

    def delete_permissions(self, conn, options):
        """
        
        """
        self.verify_options_structure(options)
        return False

    def get_permissions(self, conn, options):
        """
        
        """
        self.verify_options_structure(options)
        return {}

    def create_role(self, conn, options):
        """
        
        """
        self.verify_options_structure(options)
        # create role from db

    def update_role(self, conn, options):
        """
        
        """
        self.verify_options_structure(options)
        # update role from db

    def delete_role(self, conn, options):
        """
        
        """
        self.verify_options_structure(options)
        # delete role from db

    def get_role(self, conn, options):
        """
        
        """
        self.verify_options_structure(options)
        # get role from db

    def get_user_permissions(self, conn, options):
        """
        
        """
        # user, role, action, permissions
        self.verify_options_structure(options)
        permissions = self.get_permissions(conn, options)
        if permissions:
            return permissions
        return False

    def has_permissions(self, conn, options):
        """
        
        """
        # user, role, action, permissions for action/user
        self.verify_options_structure(options)
        # get_user_permissions
        if self.get_user_permissions(conn, options):
            return True
        return False

    def is_loggedin(self, conn, options):
        """
        
        """
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
        """
        
        """
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


__all__ = ["SQLORMBase", "AuthenticationBase"]
