
import RPi.GPIO as GPIO

class Switch:
    def __init__(self) -> None:

        self.status=False
        print("Switch file Runned")
    
    def open_switch(self):
        self.setup()
        GPIO.output(24, GPIO.HIGH)
        self.status=True
    
    def close_switch(self):
        self.setup()
        GPIO.output(24, GPIO.LOW)
        GPIO.cleanup()
        self.status=False
    
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(24, GPIO.OUT)



if __name__ == "__main__":
    import time
    sw = Switch()
    sw.open_switch()
    
    print(sw.status)
    time.sleep(5)
    sw.close_switch()
    print(sw.status)
    time.sleep(5)
    sw.open_switch()
    time.sleep(5)
    sw.close_switch()
    print("Switch file Runned")  




