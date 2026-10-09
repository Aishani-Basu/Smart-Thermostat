import urequests
from machine import Pin
import dht
import time

server_url = "http://moonhub.moonpreneur.com/LMSService/api/IOTDevice/UpdateComponentStatus"

class DHTModule:
    def __init__(self, pin, component_id, user_token, device_token, threshold=40):
        self.sensor = dht.DHT22(Pin(pin))
        self.component_id = component_id
        self.user_token = user_token
        self.device_token = device_token
        self.threshold = threshold

    def read_sensor(self):
        """Read temperature and humidity values from DHT sensor."""
        try:
            self.sensor.measure()
            temperature = self.sensor.temperature()
            humidity = self.sensor.humidity()
            return temperature, humidity
        except Exception as e:
            print("Error reading sensor:", e)
            return None, None

    def prepare_payload(self, temperature, humidity):
        """Prepare payload in the format expected by the Flutter app."""
        component_text = f"{temperature},{humidity},{self.threshold}"
        return {
            "device_component_id": self.component_id,
            "device_token": self.device_token,
            "status": True,
            "component_desc": "DHT",
            "component_text": component_text
        }

    def send_data(self):
        """Send DHT sensor data to the server."""
        temperature, humidity = self.read_sensor()
        if temperature is not None and humidity is not None:
            payload = self.prepare_payload(temperature, humidity)
            headers = {
                "Content-Type": "application/json",
                "user-token": self.user_token,
                "device-token": self.device_token
            }
            try:
                response = urequests.post(server_url, json=payload, headers=headers)
                print("DHT Response:", response.text)
                response.close()
            except Exception as e:
                print("Error sending DHT data:", e)
        else:
            print("Invalid DHT readings, skipping upload.")

