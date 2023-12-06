from dotenv import load_dotenv
import os
import mysql.connector
env=load_dotenv(".env")

class Database:
    def __init__(self):
        user = os.getenv("USERDB")
        password = os.getenv("PASSWORD")
        host = os.getenv("HOST")
        port = os.getenv("PORT")
        

        
        self.db = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            port=port
        )
        
        # Create database if not exists
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS HomeDB")
        
        # Create table if not exists
        self.cursor.execute("USE HomeDB")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Temperature (id INT AUTO_INCREMENT PRIMARY KEY, temp FLOAT, humidity FLOAT, date DATETIME)")
        self.db.commit()
    
    
    def insert(self, temp, humidity):
        self.cursor.execute("INSERT INTO Temperature (temp, humidity, date) VALUES (%s, %s, NOW())", (temp, humidity))
        self.db.commit()
    
    def get_last_24_hours(self):
        self.cursor.execute("SELECT * FROM Temperature WHERE date >= NOW() - INTERVAL 1 DAY")
        return self.cursor.fetchall()
        
        
    def get_last_row(self):
        self.cursor.execute("SELECT * FROM Temperature ORDER BY id DESC LIMIT 1")
        return self.cursor.fetchone() 
        
    
    
        
print("DB file Runned")     
        
if __name__ == "__main__":
    db = Database()
    db.insert(25, 50)
    print(db.get_last_row())
    print(db.get_last_24_hours())
    print("DB file Runned")