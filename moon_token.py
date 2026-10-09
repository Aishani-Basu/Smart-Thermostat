import urequests as requests

token_url = "http://moonhub.moonpreneur.com/LMSService/api/Account/getUserToken"
security_key="IOI2R-RO1WTR-PMQWRT-PRS70-L2TPN"
ip_address="127.0.0.1"
bearer_token = None  # Global variable to cache the token

def moon_token(username, password):
    global bearer_token
    if bearer_token:
        # If we already have the bearer token cached, return it
        return bearer_token

    headers = {'Content-Type': 'application/json', 'Security-key': security_key}
    payload = {
        "userName": username,
        "password": password,
        "ipAddress": ip_address
    }
   
    try:
        response = requests.post(token_url, json=payload, headers=headers)
        print(f"Token response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data["statusCode"] == 200 and len(data["result"]) > 0:
                bearer_token = data["result"][0]["token"]
                print(f"Bearer token received: {bearer_token}")
                return bearer_token
            else:
                print(f"Failed to get token: {data}")
                return None
        else:
            print(f"Error in token API call: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching token: {e}")
        return None