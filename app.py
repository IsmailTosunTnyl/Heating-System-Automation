import streamlit as st
import dht11
import time
from db import Database
from threading import Thread




dth11 = dht11.DHT11()


temp, hum = dth11.get_temp_humidity()
db = None

def get_temp_humidity(db):
    global temp, hum
 
    while True:
        temp, hum = dth11.get_temp_humidity()
        if temp is not None and hum is not None:
            db.insert(temp, hum)
        
        print(temp, hum)
        time.sleep(10)

@st.cache_resource
def startThereads():
    global db
    db = Database()
    
    Thread(target=get_temp_humidity,args=(db,), daemon=True).start()

startThereads()

if temp is None or hum is None:
    st.warning("Sıcaklık ve Nem değerlerine ulaşılamıyor.")
else:
    st.title("Sıcaklık ve Nem")
  
    col1, col2,  = st.columns(2)
    col1.metric("Sıcaklık", f"{temp} °C")
    col2.metric("Nem", f"{hum} %",0)


