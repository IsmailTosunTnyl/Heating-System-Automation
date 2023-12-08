from dotenv import load_dotenv
import os
import mysql.connector
import pandas as pd
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
        print("Insert")
        self.db.commit()
    
    def get_last_24_hours(self):
        self.cursor.execute("SELECT * FROM Temperature ORDER BY id DESC LIMIT 30")
        data = self.cursor.fetchall()
        df = pd.DataFrame(data, columns=["id", "temp", "humidity", "date"])
        # format date to hh:mm dd/mm/yyyy
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d/%m %H:%M")

        
        #print last date
        print(df["date"].iloc[-1])
        return  df
    
    
        
        
    def get_last_row(self):
        self.cursor.execute("SELECT * FROM Temperature ORDER BY id DESC LIMIT 1")
        data = self.cursor.fetchone()
        return data[1], data[2]
        
    
    
        
print("DB file Runned")     
        
if __name__ == "__main__":
    db = Database()

    print(db.get_last_row())
    print(db.get_last_24_hours())
    print("DB file Runned")