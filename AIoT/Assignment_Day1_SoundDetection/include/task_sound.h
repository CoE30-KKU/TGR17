// #ifndef __TASK_SOUND_H__
// #define __TASK_SOUND_H__

// // include files
// #include <Arduino.h>
// #include <FreeRTOS.h>
// #include <esp_log.h>
// #include "main.h"
// #include <driver/i2s.h>

// // shared variables

// // public function prototypes
// void task__init(void);

// #endif // __TASK_BUTTON_H__
#ifndef __TASK_SOUND_H__
#define __TASK_SOUND_H__

// include files
#include <Arduino.h>
#include <driver/i2s.h>
#include <esp_log.h>

// shared variables

// public function prototypes
void task_mic_init(void);
esp_err_t hw_mic_init(unsigned int sample_rate);
esp_err_t hw_mic_read(int32_t *samples, unsigned int *num_samples);

#endif // __HW_MIC_H__