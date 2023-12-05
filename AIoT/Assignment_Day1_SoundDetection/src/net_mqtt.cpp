#include "net_mqtt.h"

// constants
#define TAG         "net_mqtt"

#define MQTT_BROKER "192.168.1.2"
#define MQTT_PORT   1883
#define MQTT_USER   "TGR_GROUP30"
#define MQTT_PASS   "NJ485O"

#define WIFI_SSID       "TGR17_2.4G"
#define WIFI_PASSWORD   ""
const IPAddress WIFI_STATIC_IP(192, 168, 1, 97);
const IPAddress WIFI_GATEWAY(192, 168, 1, 1);
const IPAddress subnet(255, 255, 255, 0);

// static variables
static WiFiClient wifi_client;
static PubSubClient mqtt_client(wifi_client);

// connect WiFi and MQTT broker
void net_mqtt_init() {
     // initialize WiFi
    WiFi.disconnect(true);
    WiFi.mode(WIFI_STA);
    WiFi.config(WIFI_STATIC_IP, WIFI_GATEWAY, subnet);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    ESP_LOGI(TAG, "Connecting to %s...", WIFI_SSID);
    while(WiFi.status() != WL_CONNECTED) {
        vTaskDelay(10);
    }
    ESP_LOGI(TAG, "Connected to %s", WIFI_SSID);
    

    // initialize MQTT
    mqtt_client.setServer(MQTT_BROKER, MQTT_PORT);
}

// connect and subscribe to topic
void net_mqtt_connect(unsigned int dev_id, char *topic, mqtt_callback_t msg_callback) {
    String client_id = "tgr2023_" + String(dev_id);
    mqtt_client.setCallback(msg_callback);
    mqtt_client.connect(client_id.c_str(), MQTT_USER, MQTT_PASS);
    mqtt_client.subscribe(topic);
}

// publish message to topic
void net_mqtt_publish(char *topic, char *payload) {
    mqtt_client.publish(topic, payload);
}

// maintain MQTT connection
void net_mqtt_loop(void) {
    mqtt_client.loop();
}