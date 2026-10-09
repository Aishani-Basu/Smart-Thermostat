import urequests as requests
import time
from moon_token import moon_token

validate_url = "http://moonhub.moonpreneur.com/LMSService/api/IOT/ValidateDeviceDetails"
api_url="http://moonhub.moonpreneur.com/LMSService/api/IOTDevice/GetComponentStatus"
bearer_token = moon_token("anurag.mscint230301001", "an@12345")
gmail = "nilesh.t+1@moonpreneur.com"

def validate(bearer_token, device_token, gmail):
    """Validates the device once."""
    url = "http://moonhub.moonpreneur.com/LMSService/api/IOT/ValidateDeviceDetails"
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
            response = requests.post(url, json=payload, headers=headers)
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

def moon_device_status(component_id, device_token, user_token):
    #validate(bearer_token, device_token, gmail)
    url = f"{api_url}?device_component_id={component_id}&device_token={device_token}"
    headers = {
        'user-token': user_token,
        'device-token': device_token,
        'Content-Type': 'application/json'
    }

    retries = 3
    while retries > 0:
        try:
            response = requests.get(url, headers=headers)
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")
            print(url)
            print(user_token)
           
            if response.status_code == 200:
                data = response.json()
                if data.get("statusCode") == 200 and "result" in data and len(data["result"]) > 0:
                    device_status = data["result"][0].get("device_status", "").lower()
                    device_value = data["result"][0].get("component_desc", "").lower()
                    return device_status == "true", device_value  # Convert "true" to boolean True
                else:
                    print(f"Error in API response: {data}")
                    return False
            else:
                print(f"Failed to get LED state. Status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"HTTP Request Error: {e}")
            retries -= 1
            time.sleep(2)
            if retries == 0:
                return False