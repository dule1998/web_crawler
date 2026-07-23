import mysql.connector


class DB:
    __conn = None

    @staticmethod
    def connect():
        if DB.__conn is None:
            DB.__conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='********',
                database='abcd'
            )

    @staticmethod
    def get_connection():
        DB.connect()
        return DB.__conn
