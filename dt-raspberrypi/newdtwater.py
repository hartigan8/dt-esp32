import time
import json
import requests
import RPi.GPIO as GPIO

SENSOR_PIN = 17
BUTTON_PIN = 18  # Assuming the button is connected to GPIO pin 18
current_millis = 0
previous_millis = 0
interval = 1000  # seconds
calibration_factor = 50
pulse_count = 0
pulse_1_sec = 0
flow_rate = 0.0
flow_milliliters = 0
total_milliliters = 0
flows = False
json_data = {}
url_login = "https://deudthealthcare.eastus.cloudapp.azure.com/auth/login"
url_water = "https://deudthealthcare.eastus.cloudapp.azure.com/water"
login_data = {
    "email": "patient@patient.com",
    "password": "pwd"
}


GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(SENSOR_PIN, GPIO.FALLING, callback=lambda x: pulse_counter(), bouncetime=10)

def pulse_counter():
    global pulse_count
    pulse_count += 1

while True:
    current_millis = int(round(time.time() * 1000))

    if current_millis - previous_millis > interval:
        pulse_1_sec = pulse_count
        pulse_count = 0

        flow_rate = ((1000.0 / (current_millis - previous_millis)) * pulse_1_sec) / calibration_factor
        previous_millis = current_millis

        flow_milliliters = (flow_rate / 60) * 1000

        button_state = GPIO.input(BUTTON_PIN)

        if flow_milliliters != 0 and not flows and button_state == GPIO.HIGH:
            flows = True
        elif flow_milliliters == 0 and flows and button_state == GPIO.LOW:
            flows = False
            json_data["volume"] = total_milliliters
            json_data["date"] = time.time()*1000
            json_string = json.dumps(json_data, indent=2)
            response = requests.post(url_login, json=login_data)
            response_json = response.json()
            access_token = response_json.get('access_token')
            #print("Access Token:", access_token)
            print(json_string)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }

            response = requests.post(url, json=json_data, headers=headers)
            try:
                response_json = response.json()
                if response.status_code == 200:
                    print("Request was successful!")
                    print("Response JSON:", response_json)
                else:
                    print(f"Request failed with status code {response.status_code}")
                    print("Response content:", response_json)
            except json.JSONDecodeError:
                print(f"Error decoding JSON. Response content: {response.text}")


        total_milliliters += flow_milliliters
