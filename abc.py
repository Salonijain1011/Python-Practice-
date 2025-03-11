import mysql.connector

print("helloo")

class DatabaseConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user='root',
            password = 'Saloni@2025f',
            database="temp"
        )
        self.cursor = self.connection.cursor()
        
a = DatabaseConnection()
# query = 'select * from temp1'
# a.cursor.execute(query)
# res = a.cursor.fetchall()
# print(res)
print("helloo")
# print(a)