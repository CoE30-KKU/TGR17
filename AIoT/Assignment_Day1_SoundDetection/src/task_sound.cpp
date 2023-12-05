#include "main.h"
#include "task_sound.h"
#include "net_mqtt.h"

// constants
const i2s_port_t I2S_PORT = I2S_NUM_0;
#define I2S_SCK_PIN 41
#define I2S_WS_PIN 42
#define I2S_DOUT_PIN 2

#define DMA_BUF_COUNT 4
#define DMA_BUF_LENGTH 256

#define TAG "Task_Mic"
#define DELAY_PERIOD 100
#define SAMPLE_RATE 16000
#define NUM_SAMPLES 160
#define THRESHOLD 25
#define NEGATIVE_THRESHOLD -25
#define DELAY_THRESHOLD 5
#define REST_THRESHOLD 1
static unsigned int num_samples = NUM_SAMPLES;
#define SCALE 100000 // 1e5 (Depend on the microphone)
static int32_t samples[NUM_SAMPLES];

#define BTN_PIN     0 

bool state_is_scream = false;
int startTimeScream = 0;
int delayScream = DELAY_THRESHOLD;
int restScream = REST_THRESHOLD;

// static function prototypes
static void task_mic_fcn(void* arg);

// task initialization
void task_mic_init() {
    hw_mic_init(SAMPLE_RATE);
    xTaskCreate(
        task_mic_fcn,    /* Task function. */
        "Periodic Task",    /* String with name of task. */
        2048,               /* Stack size in bytes. */
        NULL,               /* Parameter passed as input of the task */
        TASK_MIC_PRIO,   /* Priority of the task. */
        NULL);              /* Task handle. */
    ESP_LOGI(TAG, "task_period created at %d", millis());
}

// task function
void task_mic_fcn(void* arg) {
    // task initialization
    while(1) {
        if(enable_flag){
            hw_mic_read(samples, &num_samples);
            float sample_avg = 0;
            for (int i = 0; i < num_samples; i++)
            {
                sample_avg += samples[i] / SCALE;
            }

            //Serial.println(sample_avg / num_samples);
            float sound_threshold = sample_avg / num_samples;
            if (sound_threshold >= THRESHOLD || sound_threshold <= NEGATIVE_THRESHOLD)
            {
                if(restScream > 0)restScream--;
                if (!state_is_scream && restScream == 0) {
                    state_is_scream = true;
                    evt_msg_t evt_msg_t = {
                    .timestamp = millis() ,
                    .soundOrIspress = true,
                    .duration = 0};
                    startTimeScream = millis();
                    xQueueSend(evt_queue, &evt_msg_t, portMAX_DELAY);
                }
                if(state_is_scream) Serial.print("#");
                delayScream = DELAY_THRESHOLD;
            }
            else
            {
                restScream = REST_THRESHOLD;
                if(state_is_scream) Serial.print(".");
                if(delayScream > 0) delayScream--;
                if(state_is_scream && delayScream == 0) {
                    state_is_scream = false;
                    evt_msg_t evt_msg_t = {
                    .timestamp = millis(),
                    .soundOrIspress = false,
                    .duration = millis() - startTimeScream + DELAY_PERIOD * REST_THRESHOLD
                    };
                    xQueueSend(evt_queue, &evt_msg_t, portMAX_DELAY);
                }
            }
        }
        vTaskDelay(DELAY_PERIOD);
    }
}

// initialize microphone
esp_err_t hw_mic_init(unsigned int sample_rate)
{
    esp_err_t err = ESP_OK;

    const i2s_config_t i2s_config = {
        .mode = i2s_mode_t(I2S_MODE_MASTER | I2S_MODE_RX), // Receive, not transfer
        .sample_rate = sample_rate,                        // 11.025/16/22.05/44.1 KHz
        .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,      // only work with 32bits
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,       // left channel
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1, // Interrupt level 1
        .dma_buf_count = DMA_BUF_COUNT,           // number of buffers
        .dma_buf_len = DMA_BUF_LENGTH,
        .use_apll = false,
        .tx_desc_auto_clear = true,
        .fixed_mclk = 0,
        .mclk_multiple = I2S_MCLK_MULTIPLE_256,
    };
    const i2s_pin_config_t pin_config = {
        .bck_io_num = I2S_SCK_PIN,  // BCKL
        .ws_io_num = I2S_WS_PIN,    // LRCL
        .data_out_num = -1,         // not used (only for speakers)
        .data_in_num = I2S_DOUT_PIN // DOUT
    };
    err = i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
    if (err != ESP_OK)
    {
        ESP_LOGE(TAG, "Failed installing driver: %d", err);
        return err;
    }
    err = i2s_set_pin(I2S_PORT, &pin_config);
    if (err != ESP_OK)
    {
        ESP_LOGE(TAG, "Failed setting pin: %d", err);
        return err;
    }
    i2s_zero_dma_buffer(I2S_NUM_0); // flush DMA buffer
    return err;
}

// read microphone
esp_err_t hw_mic_read(int32_t *samples, unsigned int *num_samples)
{
    esp_err_t err = ESP_OK;
    size_t bytes_read = 0;
    err = i2s_read(I2S_PORT, (char *)samples, (*num_samples) * 4, &bytes_read, portMAX_DELAY);
    if (err != ESP_OK)
    {
        ESP_LOGE(TAG, "Failed reading I2S: %d", err);
        *num_samples = 0;
        return err;
    }
    *num_samples = bytes_read / 4;
    return err;
}
