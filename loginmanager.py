import sqlite3
import bcrypt
from config import *

class LoginManager:
    def __init__(self):
        self.conn = None
        if self.conn is not None:
            self.init_database()
        
        
    def init_database(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS userdata (
            id INTEGER PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
            )           
        """)
        print("Initialised.")
        
        print(cur.rowcount)
        
        self.conn.commit()
        

    def connect(self):
        self.conn = sqlite3.connect(DATABASE)
        
    
    def disconnect(self):
        self.conn.close()
        
    
    def database_query(self, query : str, argument=()):
        """
        Allows a funtion to be called whenever data is requested from database.

        Args:
            query (str): request for db.
        """

        self.connect()
        
        cur = self.conn.cursor()
        cur.execute(query, argument)
        rdata = cur.fetchall()
        cur.close()
        
        self.disconnect()
        print(rdata)
        
        return (rdata)
    
    
    def validate_password(self, email : str, password : str) -> bool:
        """
        Check that the email and password matches in the db.
        """
        rdata = self.database_query("SELECT id FROM userdata WHERE email = ? AND password = ?", (email, password))

        


    
    def unique_account(self, username: str, email : str) -> bool:
        """
        Checks whether the credentials given are unique or if they already exist.

        Args:
            username (str): username to be used with the account.
            email (str): email used to create account.

        Returns:
            bool: returns False if account is unique.
        """
    
    
    def input_credentials(self, username : str, email : str, password : str) -> bool:
        """
        Inputs the new credentials into the db.
        
        Args:
            username (str): username to be added to database.
            email (str): email to be added to database.
            password (str): unhashed password to add to database.
        """
        
        self.connect()
        cur = self.conn.cursor()
        cur.execute("INSERT INTO userdata (email, username, password) VALUES (?, ?, ?)", (email, username, password))
        cur.fetchall()
        cur.close()
        self.disconnect()


        
if __name__ == "__main__":
    lm = LoginManager()
    lm.connect()
    lm.init_database()
    lm.input_credentials(username="testUsername", email="tyranids1234@gmail.com", password="testPassword")
    lm.validate_password(email="tyranids1234@gmail.com", password="testPassword")