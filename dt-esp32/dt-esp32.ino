
#include <NimBLEDevice.h>
#include <WiFiClientSecure.h>
#include <Arduino_JSON.h>

#define SENSOR 27

NimBLEScan* pBLEScan;

//wifi name
const char* ssid = "Zyxel_4A61";
const char* unit_kg="2";

//wifi password
const char* password = "QXLYLP83ML";
const char* server = "deudtchronicillness.eastus2.cloudapp.azure.com";
const int httpsPort = 443;

// Your root CA certificate
const char* test_root_ca= \
  "-----BEGIN CERTIFICATE-----\n" \
  "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\n" \
  "-----END CERTIFICATE-----\n"; 

WiFiClientSecure client;
long currentMillis = 0;
long previousMillis = 0;
int interval = 1000;
float calibrationFactor = 50;
volatile byte pulseCount;
byte pulse1Sec = 0;
float flowRate;
unsigned int flowMilliLitres;
int totalMilliLitres;
bool flows = false;
uint32_t value = 0;



void IRAM_ATTR pulseCounter() {
  pulseCount++;
}

String payloadToString(const uint8_t* payload, size_t length) {
    String result = "";
    for (size_t i = 0; i < length; i++) {
        char hex[3];
        sprintf(hex, "%02X", payload[i]);
        result += hex;
    }
    return result;

}

float rawDataKG(String data){
  String kg = data.substring(8,12);
  long decimalValue = strtol(kg.c_str(), NULL, 16);
  char* point = ".";
  String stringKg = String(decimalValue);
  char lastChar = stringKg.charAt(stringKg.length() - 1);
  stringKg =   stringKg.substring(0,stringKg.length()-1) + point + lastChar;
  return stringKg.toInt();
}

String unitOfMeasure(String data){
  String unit = data.substring(20,21);
  if(unit.equals(unit_kg)){
    return "kg";
  }
  else{
    return "pound";
  }

}

int measureDone(String data){
  String measured = data.substring(21,22);
  return measured.toInt();
}

void sendAPI(String data, String endPoint){

        client.setCACert(test_root_ca);

      if (!client.connect(server, httpsPort)) {
        Serial.println("Connection failed!");

      } else {
        Serial.println("Connected to server!");


        // Create HTTP POST request
        client.println("POST /"+endPoint+ " HTTP/1.1");
        client.println("Host: deudtchronicillness.eastus2.cloudapp.azure.com");
        client.println("Content-Type: application/json");
        client.print("Content-Length: ");
        client.println(data.length());
        client.println();
        client.println(data);
        // Wait for the server's response
        while (client.connected()) {
          String line = client.readStringUntil('\n');
          if (line == "\r") {
            Serial.println("Headers received");
            break;
          }
        }

        // Read the server's response
        while (client.available()) {
          char c = client.read();
          Serial.write(c);
        }
        client.stop();
      }



}

class MyAdvertisedDeviceCallbacks : public NimBLEAdvertisedDeviceCallbacks {
    void onResult(NimBLEAdvertisedDevice* advertisedDevice) {
       if (advertisedDevice->haveName() &&
            advertisedDevice->getName() == "OMIYA-C39-HW" &&
            advertisedDevice->getAddress().equals(NimBLEAddress("0c:95:41:00:00:23"))) { 
            String rawData = payloadToString(advertisedDevice->getPayload(), advertisedDevice->getPayloadLength());
            


        JSONVar weightjson;

        if(measureDone(rawData) == 1 ){
            //jsonDoc["device_name"] =  "OMIYA-C39-HW"; //advertisedDevice->getName();
              weightjson["id"] = 1;
              weightjson["measure"] = rawDataKG(rawData);
              weightjson["unit"] = unitOfMeasure(rawData);
              weightjson["time"] = 12321321;
            String weightjsonString = JSON.stringify(weightjson);
            Serial.print(weightjsonString);
   
           // sendAPI(jsonData,"weight");

    }

            }
        }
    }; 

void setup() {
  Serial.begin(115200);


  delay(100);
  

  NimBLEDevice::setScanFilterMode(CONFIG_BTDM_SCAN_DUPL_TYPE_DEVICE);

  NimBLEDevice::setScanDuplicateCacheSize(200);

  NimBLEDevice::init("");

  pBLEScan = NimBLEDevice::getScan(); //create new scan
  //Set the callback for when devices are discovered, no duplicates.
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks(), false);
  pBLEScan->setActiveScan(true); // Set active scanning, this will get more data from the advertiser.
  pBLEScan->setInterval(97); // How often the scan occurs / switches channels; in milliseconds,
  pBLEScan->setWindow(37);  // How long to scan during the interval; in milliseconds.
  pBLEScan->setMaxResults(0); // do not store the scan results, use callback only.


  pinMode(SENSOR, INPUT_PULLUP);

  pulseCount = 0;
  flowRate = 0.0;
  flowMilliLitres = 0;
  totalMilliLitres = 0;
  previousMillis = 0;
  attachInterrupt(digitalPinToInterrupt(SENSOR), pulseCounter, FALLING);



  WiFi.begin(ssid, password);
  Serial.print("Attempting to connect to SSID: ");
  Serial.println(ssid);

  while (WiFi.status() != WL_CONNECTED);

  Serial.print("Connected to ");
  Serial.println(ssid);


}

void loop() {
  currentMillis = millis();

   if(pBLEScan->isScanning() == false) {
      // Start scan with: duration = 0 seconds(forever), no scan end callback, not a continuation of a previous scan.
      pBLEScan->start(0, nullptr, false);
  }

  if (currentMillis - previousMillis > interval) {

    pulse1Sec = pulseCount;
    pulseCount = 0;

    // Because this loop may not complete in exactly 1 second intervals we calculate
    // the number of milliseconds that have passed since the last execution and use
    // that to scale the output. We also apply the calibrationFactor to scale the output
    // based on the number of pulses per second per units of measure (litres/minute in
    // this case) coming from the sensor.
    flowRate = ((1000.0 / (millis() - previousMillis)) * pulse1Sec) / calibrationFactor;
    previousMillis = millis();

    // Divide the flow rate in litres/minute by 60 to determine how many litres have
    // passed through the sensor in this 1 second interval, then multiply by 1000 to
    // convert to millilitres.
    flowMilliLitres = (flowRate / 60) * 1000;

    // Add the millilitres passed in this second to the cumulative total
    // Using sensor data to decide user is drinking water 
    if(flowMilliLitres != 0 && !flows){
      // water is starting to flow
      flows = true;
    }

    // flow ended
    else if(1){

        // Prepare your JSON data
        JSONVar myObject;
        myObject["id"] = 1;
        myObject["time"] = 21312310;
        myObject["volume"] = 12121;
        String jsonObject = JSON.stringify(myObject);
      
        sendAPI(jsonObject, "water");
   /*     client.setCACert(test_root_ca);

      if (!client.connect(server, httpsPort)) {
        Serial.println("Connection failed!");
      } else {
        Serial.println("Connected to server!");



        // Create HTTP POST request
        client.println("POST /water HTTP/1.1");
        client.println("Host: deudtchronicillness.eastus2.cloudapp.azure.com");
        client.println("Content-Type: application/json");
        client.print("Content-Length: ");
        client.println(jsonObject.length());
        client.println();
        client.println(jsonObject);

        // Wait for the server's response
        while (client.connected()) {
          String line = client.readStringUntil('\n');
          if (line == "\r") {
            Serial.println("Headers received");
            break;
          }
        }

        // Read the server's response
        while (client.available()) {
          char c = client.read();
          Serial.write(c);
        }

        client.stop();
      }*/
       
    }

    totalMilliLitres += flowMilliLitres;

  }
}
