import board
import adafruit_dht
import psutil

class DHT11:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            for proc in psutil.process_iter():
                if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
                    proc.kill()
            cls._instance.sensor = adafruit_dht.DHT11(board.D23)
        return cls._instance

    def get_temp_humidity(self):
        try:
            temp = self.sensor.temperature
            humidity = self.sensor.humidity
            return temp, humidity
        except RuntimeError as error:
            print(error.args[0])
            return None, None
        except Exception as error:
            self.sensor.exit()
            self.sensor = adafruit_dht.DHT11(board.D23)
            raise error
