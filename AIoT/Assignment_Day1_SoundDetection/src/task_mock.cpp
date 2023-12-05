#include "main.h"
#include "task_mock.h"
#include "net_mqtt.h"

// constants
#define TAG         "task_mock_up"

#define BTN_PIN     0 

// static function prototypes
static void task_mock_fcn(void* arg);

// task initialization
void task_mock_init() {
    xTaskCreate(
        task_mock_fcn,    /* Task function. */
        "Periodic Task",    /* String with name of task. */
        2048,               /* Stack size in bytes. */
        NULL,               /* Parameter passed as input of the task */
        TASK_MOCK_PRIO,   /* Priority of the task. */
        NULL);              /* Task handle. */
    ESP_LOGI(TAG, "task_period created at %d", millis());
}

// task function
void task_mock_fcn(void* arg) {
    // task initialization
    uint32_t period_ms = *((uint32_t*)arg);
    while(1) {
        // task function
        if(MOCK_ENABLE) {
            evt_msg_t evt_msg = {
                .timestamp = millis(),
                .soundOrIspress = (bool)(esp_random() % 2),
                .duration = esp_random(),
            };
            ESP_LOGI(TAG, "Mockup run at %d", millis());
            xQueueSend(evt_queue, &evt_msg, portMAX_DELAY);
        }
        vTaskDelay(esp_random() % 3000 + 2000);
    }
}
