/* SPDX-License-Identifier: GPL-3.0-or-later */
#include "spf5189.h"
#include "esp_log.h"
static const char *TAG = "spf5189";

esp_err_t spf5189_init(spf5189_id_t id, const spf5189_pins_t *pins)
{
    (void)pins;
    ESP_LOGI(TAG, "init id=%d (stub)", id);
    return ESP_OK;
}
esp_err_t spf5189_set_enabled(spf5189_id_t id, bool enabled)
{
    ESP_LOGI(TAG, "lna[%d] %s (stub)", id, enabled ? "ON" : "off");
    return ESP_OK;
}
esp_err_t spf5189_set_bypass(spf5189_id_t id, bool bypass)
{
    ESP_LOGI(TAG, "lna[%d] bypass=%d (stub)", id, bypass);
    return ESP_OK;
}
