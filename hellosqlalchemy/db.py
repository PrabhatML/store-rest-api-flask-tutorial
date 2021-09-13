import sqlite3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Connection:
    connection = None
    cursor = None

    @classmethod
    def set_connection(cls):
        cls.connection = sqlite3.connect("data.db")
        return cls.connection

    @classmethod
    def get_cursor(cls):
        cls.cursor = cls.set_connection().cursor()
        return cls.cursor     

    @classmethod
    def close_connection(cls):
        cls.connection.close()

    @classmethod
    def commit_close_connection(cls):
        cls.connection.commit()
        cls.connection.close()