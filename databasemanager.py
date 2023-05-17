import sqlite3
from sqlite3 import Error
import bcrypt
from config import *
from email_validator import validate_email, EmailNotValidError

class DatabaseManager:
    def __init__(self):
        self.conn = None
        if self.conn is not None:
            self.init_database()
        
        
    def init_database(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS userdata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
            )           
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS best_times (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            easy VARCHAR(255) NOT NULL,
            medium VARCHAR(255) NOT NULL,
            hard VARCHAR(255) NOT NULL,
            expert VARCHAR(255) NOT NULL
            )
        """)
        try:
            self.conn.commit()
            print("Initialisation successful.")
        except Error as e:
            print(f"The error {e} occcured.")
        

    def connect(self):
        try:
            self.conn = sqlite3.connect(DATABASE)
            print("Connection to DATABASE Successful")
        except Error as e:
            print(f"The error {e} occured")
        
    
    def disconnect(self):
        self.conn.close()
        
    
    def display_table(self):
        self.connect()
        
        cur = self.conn.cursor()
        cur.execute('SELECT id, username, email, password FROM userdata')
        
        print(cur.fetchall())
        cur.execute("SELECT id, easy, medium, hard, expert FROM best_times")
        
        print(cur.fetchall())
        
        self.disconnect()
        
        
    def delete_account(self, id):
        self.connect()
        
        cur = self.conn.cursor()
        cur.execute('DELETE FROM userdata WHERE id = ?', id)
        cur.execute('DELETE FROM best_times WHERE id = ?', id)
        self.conn.commit()
        
        self.disconnect()
        
    
    def database_query(self, query : str, argument=()):
        """
        Allows a funtion to be called whenever data is requested from database.

        Args:
            query (str): request for db.
        """

        self.connect()
        
        cur = self.conn.cursor()
        cur.execute(query, argument)
        rdata = cur.fetchone()
        cur.close()
        
        self.disconnect()
        
        return (rdata)
    
    def validate_password(self, email : str, password : str) -> bool:
        """
        Check that the email and password matches in the db.
        """
        print("Validating...")
        rdata = self.database_query("SELECT id, username, password FROM userdata WHERE email = ?", (email, ))
        print(rdata)
        
        id, username, securePass = rdata

        print(id, username, securePass)
        
        password = password.encode('utf-8')
        
        if bcrypt.checkpw(password, securePass):
            account_information = [id, username]
        else:
            print("Incorret Password")
            account_information = None
            
        return account_information


    
    def unique_account(self, email : str) -> bool:
        """
        Checks whether the credentials given are unique or if they already exist.

        Args:
            email (str): email used to create account.

        Returns:
            bool: returns True if account is unique.
        """
        existing = False
        try:
            existing_account = self.database_query("SELECT id, username, password FROM userdata WHERE email = ?", (email, ))
            existing = False
            if existing_account:
                existing = True
        except Error as e:
            print(f"Error {e} found.")
        
        return existing
        
    
    def encrypt_password(self, password : str) -> str:
        """_summary_

        Args:
            password (str): unhashed password

        Returns:
            password: hashed password
        """
        
        encrypted_password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(encrypted_password, bcrypt.gensalt())
        
        
        return hashed_password
    
    
    def validate_email(self, email : str) -> bool:
        """_summary_

        Args:
            email (str): Email that the person is trying to use to login.

        Returns:
            bool: returuns True if the email given is an invalid email.
        """
        invalid_email = False
        try:
            emailinfo = validate_email(email, check_deliverability=True)
            email = emailinfo.email
        except EmailNotValidError as e:
            print(str(e))
            invalid_email = True
            
        return invalid_email
    
    def input_credentials(self, username : str, email : str, password : str) -> bool:
        """
        Inputs the new credentials into the db.
        
        Args:
            username (str): username to be added to database.
            email (str): email to be added to database.
            password (str): unhashed password to be hashed
        """
        if self.unique_account(email) or self.validate_email(email): # Throws an error back to the user alerting them.
            print("NOT UNIQUE") 
        
        else: # Only runs if the accounts email is not in database.
            hashed_password = self.encrypt_password(password)
            
            self.connect()
            cur = self.conn.cursor()
            cur.execute("INSERT INTO userdata (email, username, password) VALUES (?, ?, ?)", (email, username, hashed_password))
            cur.execute("INSERT INTO best_times (easy, medium, hard, expert) VALUES (?, ?, ?, ?)", ("00:00", "00:00", "00:00", "00:00"))
            self.conn.commit()
            print("Record inserted successfully into userdata database table", cur.rowcount)
            cur.close()
            self.disconnect()
            print("INSERTED")
            
            
    def return_best_times(self, id : str):
        best_times = self.database_query("SELECT easy, medium, hard, expert FROM best_times WHERE id = ?", str(id))
        
        return list(best_times)
    
    def update_best_times(self, id, times):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("UPDATE best_times SET easy = ?, medium = ?, hard = ?, expert = ? WHERE id = ?", (times[0], times[1], times[2], times[3], id))
        self.conn.commit()
        cur.close()
        self.disconnect()
        print("Times Updated")
        
    
    def update_username(self, id, new_username):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("UPDATE userdata SET username = ? WHERE id = ?", (new_username, id))
        self.conn.commit()
        cur.close()
        self.disconnect()
        print("username changed")
        




        
if __name__ == "__main__":
    db = DatabaseManager()
    db.connect()
    db.init_database()
    db.display_table()
    
    