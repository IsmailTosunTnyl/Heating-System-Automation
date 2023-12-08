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

        return  df
    
    
        
        
    def get_last_row(self):
        # return average of last 10 records
        query = "SELECT temp, humidity FROM Temperature ORDER BY id DESC LIMIT 10"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        
        avg_temp = 0
        avg_humidity = 0
        for temp, humidity in data:
            avg_temp += temp
            avg_humidity += humidity
        
        avg_temp /= len(data)
        avg_humidity /= len(data)
        
        return avg_temp, avg_humidity
        
    
    
        
print("DB file Runned")     
        
if __name__ == "__main__":
    db = Database()

    print(db.get_last_row())
    print(db.get_last_24_hours())
    print("DB file Runned")