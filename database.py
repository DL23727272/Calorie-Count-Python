import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.con = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.con.cursor()

    
    def signup(self, username, password):
        try:
            insert_user_query = "INSERT INTO users(username, password) VALUES(%s, %s)"
            self.cursor.execute(insert_user_query, (username, password))
            self.con.commit()
            return True
        except mysql.connector.IntegrityError:
            return False
        
    def check_user(self, username, password):
        check_user_query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(check_user_query, (username, password))
        user = self.cursor.fetchone()
        if user:
            return True
        else:
            return False

    def close_db_connection(self):
        self.con.close()

   