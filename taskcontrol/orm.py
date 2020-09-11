# Inherit shared and logging

# RESOURCES for later
# https://docs.python.org/3/library/sqlite3.html
# https://docs.python.org/3/library/pickle.html

# TODO
# Consider making this an interface that can be extended later
# Which will make it compatible to any DB and Authentication ways
# TODO: Refactor getters and setters and make code simpler

from .interfaces import SQLBase
from .sharedbase import ClosureBase


class SQLORM(SQLBase):

    def has_sql(self, options, run="check", action="search"):
        if action == "check":
            sql = options.get("sql")
            if type(sql) == str and len(sql) > 0:
                return True
            else:
                return False
        else:
            if type(sql) == str and len(sql) > 0:
                print(options.get("sql"),
                      " {0}ed successfully".format(action))
            else:
                print(options.get("table"),
                      " {0}ed successfully".format(action))

    def create(self, conn, options):
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
            conn.commit()
            self.has_sql(options, run="print", action="create")
        except Exception as e:
            raise Exception("Error with options provided", e)
        return True

    def find(self, conn, options):
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
            conn.commit()
            self.has_sql(options, run="print", action="search")
        except Exception as e:
            raise Exception("Error with options provided", e)
        return True

    def update(self, conn, options):
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
            conn.commit()
            self.has_sql(options, run="print", action="update")
        except Exception as e:
            raise Exception("Error with options provided", e)
        return True

    def delete(self, conn, options):
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
            conn.commit()
            self.has_sql(options, run="print", action="delete")
        except Exception as e:
            raise Exception("Error with options provided", e)
        return True
