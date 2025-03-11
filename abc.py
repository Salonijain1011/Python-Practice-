# import mysql.connector

# print("helloo")

# class DatabaseConnection:
#     def __init__(self):
#         self.connection = mysql.connector.connect(
#             host="localhost",
#             user='root',
#             password = 'Saloni@2025f',
#             database="temp"
#         )
#         self.cursor = self.connection.cursor()
        
# a = DatabaseConnection()
# # query = 'select * from temp1'
# # a.cursor.execute(query)
# # res = a.cursor.fetchall()
# # print(res)
# print("helloo")
# # print(a)
import sqlite3

def connect_db():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    # Create books table
    cur.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('Available', 'Issued')),
                    issued_to TEXT DEFAULT NULL
                )''')

    # Create students table (optional, for tracking students)
    cur.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    student_id TEXT UNIQUE NOT NULL
                )''')

    conn.commit()
    conn.close()

connect_db()  # Call it once to create the database
