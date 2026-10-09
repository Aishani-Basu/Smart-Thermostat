import network
import time
import urequests as requests
from moon_token import moon_token

# Define your URLs and tokens
validate_url = "http://moonhub.moonpreneur.com/LMSService/api/IOT/ValidateDeviceDetails"
api_url = "http://moonhub.moonpreneur.com/LMSService/api/IOTDevice/GetComponentStatus"
bearer_token = moon_token("anurag.mscint230301001", "an@12345")
gmail = "nilesh.t+1@moonpreneur.com"

def validate(bearer_token, device_token, gmail):
    """Validates the device once."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + str(bearer_token)
    }

    payload = {
        "device_token": device_token,
        "user_email": gmail
    }

    retries = 3
    while retries > 0:
        try:
            response = requests.post(validate_url, json=payload, headers=headers)
            print("HTTP Response Code:", response.status_code)

            if response.status_code == 200:
                print("Validation successful")
                return True  # Exit if validation is successful
            else:
                print(f"Failed validation, Status code: {response.status_code}, Message: {response.text}")
                
                retries -= 1

        except Exception as e:
            print(f"Exception occurred: {e}")
            retries -= 1
            time.sleep(2)

    return False  # If validation failed after all retries

def connect_to_wifi(ssid, password, device_token):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    retries = 5
    while not wlan.isconnected() and retries > 0:
        print(f"Connecting to WiFi '{ssid}'...")
        wlan.connect(ssid, password)
        time.sleep(2)
        retries -= 1
    if wlan.isconnected():
        print("WiFi connected:", wlan.ifconfig())
        # Call validate function after successful connection
        if not validate(bearer_token, device_token, gmail):
            raise ConnectionError("Validation failed.")
    else:
        print("Failed to connect to WiFi.")
        raise ConnectionError("Unable to connect to WiFi.")