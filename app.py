import streamlit as st
import dht11
import time,os,subprocess,json
from db import Database
from threading import Thread
from switch import Switch
from streamlit_super_slider import st_slider



dht11_sensor = dht11.DHT11()
db = Database()
saved_temp=22


def read_temp_from_json():
    with open('temp.json', 'r') as file:
        data = json.load(file)
        return data["temp"]

saved_temp = read_temp_from_json()

def save_temp_to_db(db):
    while True:
        print("Sıcaklık kayıt")
        try:
            while True:
                temp, hum = dht11_sensor.get_temp_humidity()
                if temp is not None and hum is not None:
                    db.insert(temp, hum)
                    print("Sıcaklık kayıt Başarılı")
                    break
                time.sleep(5)
        except:
            print("DB kayıt başarısız")
        finally:
            time.sleep(60*5)


def main():

    slider_value = st_slider(15,30,saved_temp)
    # write slider value to json file
    with open('temp.json', 'w') as file:
        json.dump({"temp": slider_value}, file)
    

    def check_temp():
        
 
        while True:
            t = read_temp_from_json()
            try:
                while True:
                    temp, hum = dht11_sensor.get_temp_humidity()
                    print("Sıcaklık kontrolü yapılıyor")
                    if temp is not None:
                        break
                    else:
                        print("Sıcaklık kontrolü başarısız")
                        time.sleep(5)
                    
                print(temp, hum, t)  # Corrected print statement
                if temp < t:
                    sw.open_switch()
                else:
                    sw.close_switch()
            except Exception as e:
                print("Sıcaklık kontrolü başarısız")
                print(e)
            finally:
                time.sleep(60*1)
    
    
    
    @st.cache_resource
    def get_switch_instance():
        Thread(target=save_temp_to_db, args=(db,), daemon=True).start()
        Thread(target=check_temp, daemon=True).start()
        sw = Switch()
        return sw
    
    sw = get_switch_instance()
    
   
    
    last_temp, last_hum = db.get_last_row() if db else (None, None)

    if last_temp is None or last_hum is None:
        st.warning("Sıcaklık ve Nem değerlerine ulaşılamıyor.")
    else:
        st.title("Sıcaklık ve Nem")
        col1, col2 = st.columns(2)
        while True:
            temp, hum = dht11_sensor.get_temp_humidity()
            if temp is not None:
                break
            else:
                time.sleep(5)
            print(temp, hum,"temp, hum")
        
        if temp is not None or hum is not None:
            if temp < slider_value:
                sw.open_switch()
            else:
                sw.close_switch()
        
        temp_delta = f"{temp - last_temp:.1f} °C" if last_temp is not None else None
        hum_delta = f"{hum - last_hum:.1f} %" if last_hum is not None else None

        col1.metric("Sıcaklık", f"{temp} °C", delta=temp_delta)
        col2.metric("Nem", f"{hum} %", delta=hum_delta)
        
    if sw.status:
        st.success("Kombi açık")
    else:
        st.error("Kombi kapalı")
    
    df=db.get_last_24_hours()
    col1, col2 = st.columns(2)
    col1.subheader("Sıcaklık")
    col1.line_chart(df[["date", "temp"]].set_index("date"))
    col2.subheader("Nem")
    col2.line_chart(df[["date", "humidity"]].set_index("date"))


if __name__ == "__main__":
    
    main()
