#ifndef __MAIN_H__
#define __MAIN_H__

// include files
#include <Arduino.h>
#include <ArduinoJson.h>
#include <FreeRTOS.h>
#include <Esp.h>
#include <esp_log.h>

// constants
#define TASK_MIC_PRIO        5
#define TASK_BUTTON_PRIO     4
#define TASK_MOCK_PRIO       3
#define TASK_MQTT_PRIO       2

#define MOCK_ENABLE        0

#define TASK_MIC_TYPE       0
#define TASK_BUTTON_TYPE    1

#define MQTT_DEV_ID     30


#define MQTT_BUTTON_EVT_TOPIC  "tgr2023-WATERRRR/See-it2023/evt"
#define MQTT_MIC_EVT_TOPIC  "tgr2023-WATERRRR/See-it2023/mic" // -WATERRRR for security
#define MQTT_CMD_TOPIC  "tgr2023-WATERRRR/See-it2023/cmd"

// type definitions
typedef struct evt_msg_t {
    int type;
    uint32_t timestamp;
    bool soundOrIspress;
    uint32_t duration;
} evt_msg_t;

// shared variables
extern xQueueHandle evt_queue;
extern bool enable_flag;

// public function prototypes

#endif 