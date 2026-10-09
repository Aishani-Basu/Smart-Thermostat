import time 
from dht_module import DHTModule
from moon_device_status import moon_device_status 
from wifi_connect import connect_to_wifi
from machine import Pin
import dht

# User-defined details
ssid = "PandoraBox"
wifi_password = "atithinarayan"
user_token = "19D043F5-D69B-45A2-96CD-5E1138684B26"
device_token = "36B42BEC-4330-4A96-95F2-A14B9F83AB91"
temp_component_id = 429
fan_component_id = 430 
TEMP_THRESHOLD = 32 # Temperature threshold (in Celsius)

dht = DHTModule(pin = 12, component_id = temp_component_id, user_token = user_token, device_token = device_token)
IN1 = Pin(15, Pin.OUT)
IN2 = Pin(2, Pin.OUT)

def turn_on_fan():
    IN1.value(1)
    IN2.value(0)
    print("FAN ON")

def turn_off_fan():
    IN1.value(0)
    IN2.value(1)
    print("FAN OFF")

toggle_status = False

def read_temperature():
    try:
        temperature, humidity = dht.read_sensor()
        if temperature is not None:
            print("Temperature: ", temperature, '°C')
            return temperature
        else:
            print("Failed to read temperature")
            return None
    except Exception as e:
        print("Error Reading Temperature")
        return None

def get_toggle_status():
    global toggle_status
    values_toggle = moon_device_status(fan_component_id, user_token, device_token)
    if values_toggle[0] == 'True':
        toggle_status = True
    elif values_toggle[0] == 'False':
        toggle_status = False
    else:
        toggle_status = int(values_toggle[0]) == 1
        print("Togggle Status", toggle_status)

def main():
    try:
        connect_to_wifi(ssid, wifi_password, device_token)
        while True:
            dht.send_data()
            time.sleep(1)

            get_toggle_status()
            print("Checking temperature sensor")
            temperature = read_temperature()
            if  temperature is not None:
                if temperature >= TEMP_THRESHOLD:
                    print("Temperature is above threshold")
                    if toggle_status: 
                        turn_on_fan()
                    else:
                        turn_off_fan()
                else:
                    print("Temperature is below threshold")
                    turn_off_fan()
                time.sleep(1)
    except Exception as e:
        print("An error occured", e)

    if __name__ == "__main__":
        main()
    