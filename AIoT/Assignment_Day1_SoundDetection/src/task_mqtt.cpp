#include "main.h"
#include "task_mqtt.h"
#include "net_mqtt.h"

// constants
#define TAG             "task_mqtt"

// static variables
StaticJsonDocument<128> evt_doc;

static char evt_buf[128];

// static function prototypes
static void task_mqtt_fcn(void* arg);

// task initialization
void task_mqtt_init(mqtt_callback_t mqtt_callback) {
    xTaskCreate(
        task_mqtt_fcn,          /* Task function. */
        "MQTT Task",            /* String with name of task. */
        4096,                   /* Stack size in bytes. */
        (void*)mqtt_callback,   /* Parameter passed as input of the task */
        TASK_MQTT_PRIO,         /* Priority of the task. */
        NULL);                  /* Task handle. */
    ESP_LOGI(TAG, "task_mqtt created at %d", millis());
}

// task function
void task_mqtt_fcn(void* arg) {
    // task initialization
    Serial.print("START TASK");
    net_mqtt_init();
    net_mqtt_connect(MQTT_DEV_ID, MQTT_CMD_TOPIC, (mqtt_callback_t)arg);
    while(1) {
        static evt_msg_t evt_msg;
        // task function
        xQueueReceive(evt_queue, &evt_msg, portMAX_DELAY);
        ESP_LOGI(TAG, "task_mqtt run at %d", millis());
        
        evt_doc.clear();  
        //Prepare Data
        switch (evt_msg.type)
        {
            case TASK_MIC_TYPE:
                evt_doc["ID"] = MQTT_DEV_ID;
                evt_doc["timestamp"] = evt_msg.timestamp;
                evt_doc["sound"] = evt_msg.soundOrIspress;
                evt_doc["duration"] = evt_msg.duration;
                serializeJson(evt_doc, evt_buf);
                net_mqtt_publish(MQTT_MIC_EVT_TOPIC, evt_buf);
                ESP_LOGW(TAG, "Send Data Mic:%s with duration %d...", evt_msg.soundOrIspress ? "YESS" : "no", evt_msg.duration);
                break;
            
            case TASK_BUTTON_TYPE:  
                evt_doc["ID"] = MQTT_DEV_ID;
                evt_doc["timestamp"] = evt_msg.timestamp;
                evt_doc["pressed"] = evt_msg.soundOrIspress;
                serializeJson(evt_doc, evt_buf);
                net_mqtt_publish(MQTT_BUTTON_EVT_TOPIC, evt_buf);
                break;
            
            default:
                ESP_LOGW(TAG, "Unknown event type %d", evt_msg.type);
                break;
        }
        
   }
}