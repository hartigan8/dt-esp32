# import the necessary parts of the bluepy library
from bluepy.btle import Scanner, DefaultDelegate
import json
import time
import subprocess
import requests

ssid = "Zyxel_4A61"
password = "QXLYLP83ML"
unit_kg = '2'
json_data = {}
url = "https://deudtchronicillness.eastus2.cloudapp.azure.com/weight"
token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbkBhZG1pbi5jb20iLCJpYXQiOjE3MDI4Mzk3MjUsImV4cCI6MjMwMjgzOTY2NX0.7JiVID9sT-IOkXo5d6UEtlquxvv0pyERHhY3zwk54u0"

def connect_wifi(ssid, password):
    try:
        # Connect to WiFi using nmcli on Linux
        subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "password", password], check=True)
        print(f"Connected to WiFi network: {ssid}")
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to WiFi: {e}")

def raw_data_kg(data):
    kg = data[4:8]
    decimal_value = int(kg, 16)
    string_kg = str(decimal_value)
    last_char = string_kg[-1]
    string_kg = string_kg[:-1] + "." + last_char
    return float(string_kg)

def unit_of_measure(data):
    unit = data[16]

    if unit == unit_kg:
        return "kg"
    else:
        return "pound"

def measure_done(data):
    measured = int(data[17])
    return measured

# create a delegate class to receive the BLE broadcast packets
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    # when this python script discovers a BLE broadcast packet, print a message with the device's MAC address
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr == "0c:95:41:00:00:23":
            manufacturer_data_type = 0xFF
            for (adtype, desc, value) in dev.getScanData():
                if adtype == manufacturer_data_type:
                    print(f"Manufacturer Data: {value}")
                    if measure_done(value) == 1:
                        json_data["measure"] = raw_data_kg(value)
                        json_data["unit"] = unit_of_measure(value)
                        json_data["date"] = 321321321
                        json_string = json.dumps(json_data, indent=2)  # 'indent' is optional for pretty-printing
                        print(json_string)
                        headers = {
                            'Content-Type': 'application/json',
                            'Authorization': f'Bearer {token}'
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


# create a scanner object that sends BLE broadcast packets to the ScanDelegate
scanner = Scanner().withDelegate(ScanDelegate())

# start the scanner and keep the process running
scanner.start()
while True:
    print("Still running...")
    scanner.process()

