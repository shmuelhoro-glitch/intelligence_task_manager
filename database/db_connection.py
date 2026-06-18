import mysql.connector

class DB_connection:
    def __init__(self):
        self.conn = None
    def get_connection(self):
        if self.conn is None or not self.conn.is_connected():
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "1234",
                database = "Intelligence_db")
            return conn
        else:
            return self.conn

    def create_database(self):
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "1234"
        )
        cursor = conn.cursor()
        try:
            cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")
            cursor.execute("USE Intelligence_db")
            return {"message":"Successfully completed"}
        except:
            raise {"message":"error creating the database"}

        finally:
            cursor.close()
            conn.close()

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS agents(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(50) NOT NULL,
                       specialty VARCHAR(100) NOT NULL,
                       is_active BOOLEAN DEFAULT TRUE NOT NULL,
                       completed_missions INT NOT NULL DEFAULT 0 ,
                       failed_missions INT NOT NULL DEFAULT 0,
                       agent_rank ENUM("Junior","Senior","Commander")
                       )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS missions(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       title VARCHAR(100) NOT NULL ,
                       description TEXT NOT NULL,
                       location VARCHAR(100) NOT NULL,
                       difficulty INT CHECK(difficulty BETWEEN 1 AND 10) NOT NULL,
                       importance INT CHECK(importance BETWEEN 1 AND 10) NOT NULL,
                       status ENUM("NEW","ASSIGNED","IN_PROGRESS","COMPLETED","FAILED","CANCELLED") NOT NULL DEFAULT 'NEW',
                       risk_level VARCHAR(50) NOT NULL,
                       assigned_agent_id INT DEFAULT NULL
                       )""")
        cursor.close()
        conn.close()



db = DB_connection()
db.create_database()
db.create_tables()