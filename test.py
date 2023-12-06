import dht11

dth11 = dht11.DHT11()
temp, hum = dth11.get_temp_humidity()
print(temp, hum)