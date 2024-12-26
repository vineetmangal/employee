import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def get_connection(self):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection


class Employee:
    def __init__(self, id, first_name, last_name, email, department, hire_date):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.department = department
        self.hire_date = hire_date