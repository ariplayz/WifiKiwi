/* SPDX-License-Identifier: GPL-3.0-or-later */
#include "ili9488.h"
#include "esp_log.h"
static const char *TAG = "ili9488";
esp_err_t ili9488_init(const ili9488_config_t *cfg)
{
    (void)cfg;
    ESP_LOGI(TAG, "init (stub)");
    return ESP_OK;
}
esp_err_t ili9488_set_brightness(uint8_t pct)
{
    if (pct > 100) pct = 100;
    ESP_LOGI(TAG, "brightness %u%% (stub)", pct);
    return ESP_OK;
}
