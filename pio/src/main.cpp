#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

#define DHTPIN 13
#define DHTTYPE DHT11
#define LED_BUILTIN 2
DHT dht(DHTPIN, DHTTYPE);
float temp, hum;
StaticJsonDocument<200> jsonDoc;
TaskHandle_t Task0;

// Deklarasi Variable dan Konstanta
String wifiSSID = "eduroom";
String wifiPassword = "dilanarsidah";
String broker = "broker.hivemq.com";
WiFiClient client;
PubSubClient mqtt(client);
String command = "";
String jsonVal;
bool conn_state;
String topic_sub = "rifki-mqtt/command";
String topic_pub = "rifki-mqtt/datapub";
// Deklarasi Fungsi
void connectWifi();
void connectMqtt();
String getDHT();
void readMessage(char *topic, byte *msg, unsigned int msgLength);
void mqttPublish(const String &jsonString);
void mqttTask(void *pvParameters);
bool checkConnection();
void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  dht.begin();
  connectWifi();
  mqtt.setServer(broker.c_str(), 1883);
  mqtt.setCallback(readMessage);
  xTaskCreatePinnedToCore(mqttTask, "Task0", 10000, NULL, 1, &Task0, 0);
  delay(1000);
}

void loop()
{
  if (!checkConnection())
  {
    connectWifi();
  }
  jsonVal = getDHT();
  // Serial.print("Main Task running on core: ");
  // Serial.println(xPortGetCoreID());
  delay(200);
}

void mqttTask(void *pvParameters)
{
  while (true)
  {
    // Serial.print("MQTT Task running on core: ");
    // Serial.println(xPortGetCoreID());
    if (checkConnection()){
      connectMqtt();
      mqttPublish(jsonVal);
      mqtt.loop();
    }
    vTaskDelay(200/portTcbMemoryCaps);
  }
}

String getDHT()
{
  // temp = dht.readTemperature();
  // hum = dht.readHumidity();
  temp = random(10, 100);
  hum = random(10, 100);
  jsonDoc.clear();
  jsonDoc["temp"] = "temperature";
  jsonDoc["temp_value"] = temp;
  jsonDoc["hum"] = "humidity";
  jsonDoc["hum_value"] = hum;

  char jsonString[200];
  serializeJson(jsonDoc, jsonString);

  // Serial.println("Data Sended : " + String(jsonString));
  return String(jsonString);
}

void mqttPublish(const String &jsonString)
{
  mqtt.publish(topic_pub.c_str(), jsonString.c_str());
  Serial.println("Data sent: " + jsonString);
}

void connectMqtt()
{
  while (!mqtt.connected())
  {
    Serial.println("Connecting MQTT...");
    if (mqtt.connect("esp32"))
    {
      Serial.println("MQTT Connected");
      mqtt.subscribe(topic_sub.c_str());
    }
  }
}
void connectWifi()
{
  Serial.println("Connecting To Wifi");
  WiFi.begin(wifiSSID.c_str(), wifiPassword.c_str());
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }

  Serial.println("Wifi Connected");
  Serial.println(WiFi.SSID());
  Serial.println(WiFi.RSSI());
  Serial.println(WiFi.macAddress());
  Serial.println(WiFi.localIP());
  Serial.println(WiFi.gatewayIP());
  Serial.println(WiFi.dnsIP());
  Serial.println(xPortGetCoreID());
}

bool checkConnection()
{
  if (WiFi.status() == WL_CONNECTED)
  {
    conn_state = true;
    // Serial.println("Wifi connected");
  }
  else if (WiFi.status() != WL_CONNECTED)
  {
    conn_state = false;
    // Serial.println("Wifi not connected");
  }
  else if(!mqtt.connected()){
    conn_state = false;
    // Serial.println("MQTT not connected");
  }
  return conn_state;
}

void readMessage(char *topic, byte *msg, unsigned int msgLength) {
  Serial.print("Running on Core: ");
  Serial.println(xPortGetCoreID());

  // Check if the received topic matches the expected topic
  if (String(topic) == topic_sub) {
    // Create a buffer for the payload
    char payload[200]; // +1 for null terminator

    // Copy the payload bytes to the payload buffer
    for (int i = 0; i < msgLength; i++) {
      payload[i] = (char)msg[i];
    }
    payload[msgLength] = '\0'; // Null terminator
    Serial.println(String(payload));
    // Deserialize JSON directly from the payload buffer
    deserializeJson(jsonDoc, payload);

    // Extract data from the JSON
    const char* command = jsonDoc["command"];
    int com_value = jsonDoc["com_value"];

    if (String(command) == "LED" && com_value == 1){
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else if (String(command) == "LED" && com_value == 0){
      digitalWrite(LED_BUILTIN, LOW);
    }

    // Print the received data
    Serial.println("Command: "+String(command));
    Serial.println("Command Value: " + String(com_value));
  }
}