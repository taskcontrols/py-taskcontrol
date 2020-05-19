import sqlite3

conn = sqlite3.connect('./name' + '.db')

# sql = '''
#         CREATE TABLE users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username VARCHAR(255) NOT NULL,
#             password VARCHAR(255) NOT NULL
#         );
#     '''
# c = conn.execute(sql)
# print("Table users created successfully")
# conn.commit()
# sql = '''
#         CREATE TABLE roles (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id VARCHAR(255) NOT NULL,
#             role VARCHAR(255) NOT NULL,
#             activity VARCHAR(255) NOT NULL,
#             permission VARCHAR(255) NOT NULL
#         );
#     '''
# c = conn.execute(sql)
# print("Table roles created successfully")
# conn.commit()

sql = """
        INSERT INTO users (username, password) VALUES ({0}, {1});
    """.format('admin', 'password')
conn.execute(sql)
print("User created successfully")
conn.commit()
conn.close()
