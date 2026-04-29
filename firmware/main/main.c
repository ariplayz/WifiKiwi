/* SPDX-License-Identifier: GPL-3.0-or-later
 *
 * WifiKiwi firmware entry point.
 *
 * Boots the ESP32-C5, initialises NVS, brings up the display, mounts the
 * filesystem, and hands off to the UI app dispatcher.
 *
 * Copyright (c) 2026 The WifiKiwi contributors.
 */

#include <stdio.h>

#include "esp_log.h"
#include "esp_system.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "nvs_flash.h"

#include "rf_safety.h"

static const char *TAG = "wifikiwi";

void app_main(void)
{
    ESP_LOGI(TAG, "WifiKiwi booting on %s", CONFIG_IDF_TARGET);

    esp_err_t err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES || err == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        err = nvs_flash_init();
    }
    ESP_ERROR_CHECK(err);

    // Mute every TX path until the UI explicitly enables one.
    rf_safety_init();
    rf_safety_all_off();

    // TODO(fw-skeleton): bring up display + LVGL + UI dispatcher here.
    ESP_LOGW(TAG, "UI not yet implemented; idling.");

    while (true) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
